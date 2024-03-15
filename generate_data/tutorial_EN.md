# EmoLLM fine-tuning data generation tutorial

**I. Objectives and Background**

In order to have a better representation of our large mental models, we must have high quality datasets. To achieve this goal, we decided to use four powerful AI grand models: **Wenxin Yiyan**, **Tongyi Qianwen**, **Feifei Spark**, and **Zhipu GLM** to generate conversation data. In addition, we will enhance the cognitive depth of the dataset and improve the generalization ability of the model by adding a small number of self-cognitive datasets.

**II. dataset generation method**

1. **Model selection and data preparation**

   Choose four big language models, namely Wenxin Yiyan, Tongyi Qianwen, IFei Spark and Zhipu GLM, obtain the API to call the corresponding interface, and prepare to generate dialogue data.
   
3. **Single-turn and multi-turn dialogue data generation**

   Using these four models, we generated 10,000 single and multi-turn conversation data. In doing so, we ensure the diversity, complexity and validity of our data.

   Because mental activity is often complex, in order to ensure the diversity of data. We selected a total of 16 * 28 `448` scenarios for dataset generation. For specific scenario names, please refer to the configuration of the two parameters`emotions_list and areas_of_life`in config.yml.
   
4. **Inclusion of self-perception datasets**

   In order to enhance the cognitive ability of the model, we specially added a part of self-cognitive dataset. These datasets help the model better understand the context and improve the naturalness and coherence of the conversation.

**III. Practical steps**

1. **Initialize**

* Install the required software and libraries

  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
  
* Prepare input data and configuration parameters

  See `config.yml` for annotations

2. **Model selection and configuration**

* Select the right model for your needs
  In order to enable everyone to play with the large model, we chose the InterLLM2-7B as our baseline model (consumer graphics cards can also be deployed fine-tuned oh).
  
* Make necessary configurations and adjustments to the model
  Use XTuner for fine-tuning based on our dataset and configuration strategy.

3. **Data generation**

* Data generation using Tongyi Qianwen
  ```bash
  # Terminal operation
  bash run_qwen.bash
  ```
* Data generation using Wenxin Yiyan
  ```bash
  # Terminal operation
  python ernie_gen_data.py
  ```
* Data generation using Zhipu GLM
  ```bash
  # Terminal operation
  python zhipuai_gen_data.py
  ```
* Data generation using IFlystar Fire
  ```bash
  # Terminal operation
  python ./xinghuo/gen_data.py
  ```

4. **Integration of self-cognition datasets**

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

5. **dataset integration**

Before dataset integration, we need to check whether the generated data has formatting errors, type mismatches, etc. We need check.py to check the data. Finally, merge_json.py is used to combine all the json into one overall json file.

6. **Evaluation and optimization**

* Evaluate the generated dataset using appropriate evaluation metrics
* Make necessary optimizations and adjustments based on the evaluation results

7. **Testing and deployment**

* Evaluate the trained model using an independent test set
* Make necessary adjustments and optimizations based on test results
* Deploy the final model into a real application
* 
