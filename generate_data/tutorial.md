# EmoLLM 微调数据生成教程

## **一、目标与背景**

为了使我们的心理大模型有更好的表达效果，我们必须要有高质量的数据集。为了达到这一目标，我们决定利用四种强大的中文大模型：文心一言、通义千问、讯飞星火 和 智谱GLM 来生成对话数据。此外，我们还将增强数据集的认知深度，通过加入少量自我认知数据集来提高模型的泛化能力。

## **二、数据集生成方法**

1. **模型选择与数据准备**

   选择文心一言、通义千问、讯飞星火和智谱GLM这四种大语言模型，获取调用相应接口的API，并准备用于生成对话数据。

2. **单轮与多轮对话数据生成**

   利用这四种模型，我们生成了10000条单轮和多轮对话数据。在这一过程中，我们确保了数据的多样性、复杂性和有效性。

   因为心理活动往往是复杂的，为了保证数据的多样性。我们选择了16 * 28 共 `448`个场景进行数据集生成，具体场景名称请参考config.yml中的 `emotions_list 和 areas_of_life`两个参数的配置。

3. **自我认知数据集的加入**

   为了增强模型的认知能力，我们特意加入了一部分自我认知数据集。这些数据集有助于模型更好地理解上下文，提高对话的自然度和连贯性。

## **三、实践步骤**

### 1. **初始化**

* 安装所需的软件和库

  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

* 准备输入数据和配置参数

  可参见 `config.yml`均有注释

### 2. **模型选择与配置**

* 根据需求选择适合的模型
  为了使大家都能够玩上大模型，我们选用InterLLM2-7B作为我们的基线模型（消费级显卡也可部署微调的哦）
* 对模型进行必要的配置和调整
  根据我们的数据集以及配置策略，使用XTuner进行微调

### 3. **数据生成**

#### **三种改进前的数据生成方法**

* 使用通义千问大模型进行数据生成
  
```bash
  # 终端运行
  bash run_qwen.bash
```

* 使用百度文心大模型进行数据生成

```bash
  # 终端运行
  python ernie_gen_data.py
```

* 使用讯飞星火大模型进行数据生成
  
```bash
  # 终端运行
  python ./xinghuo/gen_data.py
```

#### **改进的两种数据生成方法**

采用改进的数据生成方法生成多轮对话时，首先需要定义`ai_tool`变量，该变量表示LLM模型的名称（`qwen`或`zhipuai`）。根据`ai_tool`变量的值，创建一个`{ai_tool}`文件夹。

然后，遍历所有的`area`值，接着根据不同的`emotion`值生成多轮对话。生成的对话会每隔`save_interval`次迭代写入到`./{ai_tool}/{area}/{emotion}.jsonl`文件中。这个过程会重复执行`total_num_each_emo_area`次。

* 使用**改进的**通义千问大模型数据生成方法
  
```bash
   # 或者不使用bash，直接运行
  python qwen_gen_data_NoBash.py
```

* 使用**改进的**智谱GLM大模型数据生成方法
  
```bash
  # 终端运行
  python zhipuai_gen_data.py
```

### 4. **自我认知数据集的整合**

* 自我认知数据集需要按照格式手动生成，如下格式即可

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

### 5. **数据集整合**

#### Case 1: 使用`python ernie_gen_data.py`、`bash run_qwen.bash`或者`python ./xinghuo/gen_data.py`

* 首先使用`check.py`进行数据检查。在进行数据集整合之前，我们要检查生成的数据是否存在格式错误，类型不符合等情况。
* 然后使用`merge_json.py`将所有的json（或者使用`merge_jsonl.py`将所有的jsonl）文件整合为一个总的json文件。

#### Case 2: 使用改进的生成保存方法：`python qwen_gen_data_NoBash.py`或者`python zhipuai_gen_data.py`

在这种情况下，我们需要在使用两种改进的生成方法生成多轮对话后，将`{data_ai}`文件夹下所有`{area}`子文件夹中的所有`{emotion}.jsonl`文件合并为`{data_ai}_final_merge.json`文件。

* 由于采用了改进的数据生成方法和不同的存储生成对话结构，因此我们可以免除对数据集的检查。
* 然后使用`merge_jsonl_r.py`将`qwen`或者`zhipuai`定义为`data_ai`变量，并将其文件夹下所有领域（`area`）下所有的jsonl文件整合为一个总的json文件并取名为`{area}_merge.json`,最终在`{data_ai}`文件夹下生成`{data_ai}_final_merge.json`。
* 然后我们可以手动合成`qwen_final_merge.json`和`zhipuai_final_merge.json`为`qwen_zhipuai_final_merge.json`文件了， 注意合并后的json文件夹中，最外面只有一对`[]`，中间是`{}`包裹的多轮对话。

### 6. **评估与优化**

* 使用适当的评估指标对生成的数据集进行评估
* 根据评估结果进行必要的优化和调整

### 7. **测试与部署**

* 使用独立测试集对训练好的模型进行评估
* 根据测试结果进行必要的调整和优化
* 将最终的模型部署到实际应用中
