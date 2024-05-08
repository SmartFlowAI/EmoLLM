# Book_QA_process

共两个python文件，分别为Book_QA_process_Step_1.py和Book_QA_process_Step_2.py

### Book_QA_process_Step_1.py

* 该代码是将我们生成的QA对jsonl数据转换为json格式

### Book_QA_process_Step_2.py
* 该代码是将第一步生成的json格式数据转化为可用于指令微调的数据格式，并添加system，即：

  ```json
    {
        "conversation": [
            {
                "system": "你由EmoLLM团队打造的心理健康助手......",
                "input": "Question",
                "output": "Answer"
            }
        ]
    }
```