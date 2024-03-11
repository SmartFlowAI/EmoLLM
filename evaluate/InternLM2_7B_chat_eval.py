from transformers import AutoModelForCausalLM, AutoTokenizer,DataCollatorWithPadding
from qwen_generation_utils import  decode_tokens
import torch
import datasets


model_dir = './model'
tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", padding_side='left',trust_remote_code=True)
# Set `torch_dtype=torch.float16` to load model in float16, otherwise it will be loaded as float32 and might cause OOM Error.
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto",pad_token_id=tokenizer.eos_token_id, trust_remote_code=True, torch_dtype=torch.float16)
# (Optional) If on low resource devices, you can load model in 4-bit or 8-bit to further save GPU memory via bitsandbytes.
  # InternLM 7B in 4bit will cost nearly 8GB GPU memory.
  # pip install -U bitsandbytes
  # 8-bit: model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, load_in_8bit=True)
  # 4-bit: model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, load_in_4bit=True)
model = model.eval()

# # convert data
# import ujson
# def transform_conversation_data(raw_data):
#     try:
#         instruction = '<|im_start|>system\n'+raw_data.get("conversation", "")[0]['system'] + "<|im_end|>\n"

#         conversation = raw_data.get("conversation", [])
#         for i, dialog in enumerate(conversation):
#             instruction += "<|im_start|>user\n来访者：" + dialog["input"]+ "<|im_end|>\n"

#             if i < len(conversation) - 1:
#                 instruction += "<|im_start|>assistant\n医生：" + dialog["output"]+"<|im_end|>\n"

#         response = conversation[-1]["output"] if conversation else ""

#         instruction +="<|im_start|>assistant\n医生："

#         return {"instruction": instruction, "output": response}
    
#     except Exception as e:
#         pass


# with open(f'./data_dir/data.json', 'r', encoding='utf-8') as f1:
#     data = ujson.load(f1)
# with open(f'./data_dir/converted.json', 'w', encoding='utf-8') as f:
#     for j, item in enumerate(data):
#         temp=transform_conversation_data(item)
#         if temp:
#             transformed_data =ujson.dumps(temp, ensure_ascii=False)
#             f.write(transformed_data+'\n')

#set test params


#set test params
test_num=1596 #测试数据条数
batch_size=12


#prepare data and dataloader
dataset = datasets.load_dataset('json', data_files='./data_dir/converted.json',split=f"train[:{test_num}]")
references =dataset['output'][:test_num]

hypotheses = []
def preprocess(data):
    length = list(map(len, data['instruction']))
    model_inputs=tokenizer(data['instruction'], max_length=512, truncation=True )
    labels=tokenizer(data['output'], padding=True,max_length=128, truncation=True )
    model_inputs['labels']=labels['input_ids']
    model_inputs['length'] = length
    return model_inputs
preprocessed_dataset = dataset.map(preprocess, batched=True,remove_columns=['instruction', 'output',])


collator=DataCollatorWithPadding(tokenizer=tokenizer,)
from torch.utils.data import DataLoader

dataloader = DataLoader(preprocessed_dataset, batch_size=batch_size, collate_fn=collator)

#generate responses
stop_word="<|im_end|>"
for batch in dataloader:
    batch_input_ids = torch.LongTensor(batch['input_ids']).to(model.device)
    batch_labels = batch['labels']
    attention_mask = batch['attention_mask']
    length = batch['length']
    batch_out_ids = model.generate(
        batch_input_ids.to(model.device),
        return_dict_in_generate=False,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.1,
        eos_token_id=92542
    )
    
    padding_lens = [batch_input_ids[i].eq(tokenizer.pad_token_id).sum().item() for i in range(batch_input_ids.size(0))]
    batch_response = [
    decode_tokens(
        batch_out_ids[i][padding_lens[i]:],
        tokenizer,
        context_length=0,
        raw_text_len=length[i],
        chat_format="raw",
        verbose=False,
        errors='replace'
    ).replace("医生：","") for i in range(batch_size)]
    hypotheses.extend([r.replace(stop_word," ").split()[0] if stop_word in r else r for r in batch_response])


# Load metric
from metric import compute_metrics

print(compute_metrics((hypotheses,references)))