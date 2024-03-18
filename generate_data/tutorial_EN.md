# EmoLLM fine-tuning data generation tutorial

## **I. Objectives and Background**

In order to have a better representation of our large mental models, we must have high quality datasets. To achieve this goal, we decided to use four powerful AI grand models: **Wenxin Yiyan**, **Tongyi Qianwen**, **Feifei Spark**, and **Zhipu GLM** to generate conversation data. In addition, we will enhance the cognitive depth of the dataset and improve the generalization ability of the model by adding a small number of self-cognitive datasets.

## **II. dataset generation method**

1. **Model selection and data preparation**

   Choose four big language models, namely Wenxin Yiyan, Tongyi Qianwen, IFei Spark and Zhipu GLM, obtain the API to call the corresponding interface, and prepare to generate dialogue data.
   
3. **Single-turn and multi-turn dialogue data generation**

   Using these four models, we generated 10,000 single and multi-turn conversation data. In doing so, we ensure the diversity, complexity and validity of our data.

   Because mental activity is often complex, in order to ensure the diversity of data. We selected a total of 16 * 28 `448` scenarios for dataset generation. For specific scenario names, please refer to the configuration of the two parameters`emotions_list and areas_of_life`in config.yml.

4. **Inclusion of self-perception datasets**

   In order to enhance the cognitive ability of the model, we specially added a part of self-cognitive dataset. These datasets help the model better understand the context and improve the naturalness and coherence of the conversation.

## **III. Practical steps**

### 1. **Initialize**

* Install the required software and libraries

  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
  
* Prepare input data and configuration parameters

  See `config.yml` for annotations

### 2. **Model selection and configuration**

* Select the right model for your needs
  In order to enable everyone to play with the large model, we chose the InterLLM2-7B as our baseline model (consumer graphics cards can also be deployed fine-tuned oh).
  
* Make necessary configurations and adjustments to the model
  Use XTuner for fine-tuning based on our dataset and configuration strategy.

### 3. **Data generation**

#### **Three original methods for data generation**

* 1.Data generation using Tongyi Qianwen 
  
```bash
  # Terminal operation
  bash run_qwen.bash
```

* 2.Data generation using Wenxin Yiyan
  
```bash
  # Terminal operation
  python ernie_gen_data.py
```

* 3.Data generation using IFlystar Fire
  
```bash
  # Terminal operation
  python ./xinghuo/gen_data.py
```

#### **Two improved methods for data generation**

When generating multi-turn dialogues with these two improved methods, the first step is to define the value of the `ai_tool` variable, which represents the LLM model name (`qwen` or `zhipuai`). Based on the value of this `ai_tool` variable, a `{ai_tool}` folder is created. 

Then, all `area` values are traversed, followed by different `emotion` values for generating multi-turn dialogues. The generated dialogues are written to the `./{ai_tool}/{area}/{emotion}.jsonl` file every `save_interval` iterations. This process is repeated `total_num_each_emo_area` times.

* 1.Using the **improved** method for generating data with the Qwen model:
  
```bash
  # Alternatively, you can run it directly without using bash
  python qwen_gen_data_NoBash.py
```

* 2.Using the **improved** method for generating data with the Zhipuai GLM-4 model:

```bash
  # Alternatively, you can run it directly without using bash
  python zhipuai_gen_data.py
```

### 4. **Integration of self-cognition datasets**

* Self-cognition dataset this needs to be manually generated in accordance with the format, the following format can be
  
  ```json
  [
      {
          "conversation": [
              {
                  "input": "请介绍一下你自己",
                  "output": "我是大佬的emo小助手，可以帮助你解决心理上的问题哦"
              }
          ]
      },
      {
          "conversation": [
              {
                  "input": "请做一下自我介绍",
                  "output": "我是大佬的emo小助手，可以帮助你解决心理上的问题哦"
              }
          ]
      }
  ]
  ```

### 5. **Dataset Integration**

#### **Case 1**: Using `python ernie_gen_data.py`, `bash run_qwen.bash`, or `python ./xinghuo/gen_data.py`

* First, use `check.py` to check the data. Before integrating the dataset, we need to check whether the generated data has format errors or type mismatches.
* Then, use `merge_json.py` to consolidate all json files (or use `merge_jsonl.py` to consolidate all jsonl files) into one overall json file.

#### **Case 2**: Using improved generation method: `python qwen_gen_data_NoBash.py` or `python zhipuai_gen_data.py` 

In this case, we need to merge all `{emotion}.jsonl` files in all `{area}` subfolders under the `{data_ai}` folder into `{data_ai}_final_merge.json` after we use two improved generation methods to generate multi-round conversations.

* As we have adopted improved data generation methods and different storage generation dialog structures, we can avoid checking the dataset.
* Then, use `merge_jsonl_r.py` to define `qwen` or `zhipuai` as the `data_ai` variable, and consolidate all jsonl files in all areas (`area`) into one overall json file named `{area}_merge.json`. Finally, generate `{data_ai}_final_merge.json` in the `{data_ai}` folder.
* We can then manually merge `qwen_final_merge.json` and `zhipuai_final_merge.json` into `qwen_zhipuai_final_merge.json`. Note that in the merged json file, there is only one pair of `[]` on the outside, and the multi-round dialogues are wrapped in `{}`.

### 6. **Evaluation and optimization**

* Evaluate the generated dataset using appropriate evaluation metrics
* Make necessary optimizations and adjustments based on the evaluation results

### 7. **Testing and deployment**

* Evaluate the trained model using an independent test set
* Make necessary adjustments and optimizations based on test results
* Deploy the final model into a real application