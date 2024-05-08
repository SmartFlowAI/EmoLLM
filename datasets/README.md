# EmoLLM数据集

* 数据集按用处分为两种类型：**General** 和 **Role-play**
* 数据按格式分为两种类型：**QA** 和 **Conversation**
* 数据汇总：General（**8个数据集**）；Role-play（**5个数据集**）

## 数据集类型

* **General**：通用数据集，包含心理学知识、心理咨询技术等通用内容
* **Role-play**：角色扮演数据集，包含特定角色对话风格数据等内容

## 数据类型

* **QA**：问答对
* **Conversation**：多轮对话

## 数据集汇总

|   Category  |        Dataset        |     Type     |  Total  |
| :---------: | :-------------------: | :----------: | :-----: |
|  *General*  |         data          | Conversation |  5600+  |
|  *General*  |       data_pro        | Conversation | 36,500+ |
|  *General*  | multi_turn_dataset_1  | Conversation | 36,000+ |
|  *General*  | multi_turn_dataset_2  | Conversation | 27,000+ |
|  *General*  | single_turn_dataset_1 |      QA      | 14,000+ |
|  *General*  | single_turn_dataset_2 |      QA      | 18,300+ |
|  *General*  | self_cognition_EmoLLM |      QA      |   85+   |
|  *General*  |      ruozhiba_raw     |      QA      |   240+  |
| *Role-play* |         aiwei         | Conversation |  4000+  |
| *Role-play* |       SoulStar        |      QA      | 11,200+ |
| *Role-play* |        tiangou        | Conversation |  3900+  |
| *Role-play* |        mother         | Conversation | 40,300+ |
| *Role-play* |       scientist       | Conversation | 28,400+ |
|     ……      |          ……           |      ……      |   ……    |

## 数据集来源

### **General**

* 数据集 `data` 来自本项目
* 数据集 `data_pro` 来自本项目
* 数据集 `multi_turn_dataset_1` 来源 [Smile](https://github.com/qiuhuachuan/smile)
* 数据集 `multi_turn_dataset_2` 来源 [CPsyCounD](https://github.com/CAS-SIAT-XinHai/CPsyCoun)
* 数据集 `single_turn_dataset_1` 来自本项目
* 数据集 `single_turn_dataset_2` 来自本项目
* 数据集 `self_cognition_EmoLLM` 来自本项目
* 数据集 `ruozhiba_raw` 来源[COIG-CQIA](https://huggingface.co/datasets/m-a-p/COIG-CQIA/viewer/ruozhiba)

### **Role-play**

* 数据集 `aiwei` 来自本项目
* 数据集 `tiangou` 来自本项目
* 数据集 `SoulStar` 来源 [SoulStar](https://github.com/Nobody-ML/SoulStar)
* 数据集 `mother` 来自本项目
* 数据集 `scientist` 来自本项目

## 数据集去重

结合绝对匹配以及模糊匹配(Simhash)算法，对数据集进行去重以提升微调模型的效果。在确保数据集的高质量的同时，通过调整阈值减少因错误匹配而丢失重要数据的风险。

### **Simhash算法介绍**

Simhash（相似性哈希）是一种用于检测大量数据中相似或重复项的算法。它通过将文本转换为一组数值指纹来工作，这些指纹对相似的文本具有高度的相似性。Simhash算法对于处理文本数据特别有效，尤其是在处理大量数据时。详细介绍可见 [Simhash](https://algonotes.readthedocs.io/en/latest/Simhash.html).

### **Simhash实现步骤**

* 文本预处理：将文本数据转换为适合Simhash处理的格式。这可能包括分词、去除停用词、词干提取等。
* 生成Simhash指纹：对预处理后的文本应用Simhash算法，生成一组数值指纹。每个指纹代表文本内容的一个哈希值。
* 比较指纹：通过比较哈希值的相似性来识别重复或相似的记录。Simhash的特点是即使在文本有少量差异时，生成的哈希值也具有较高的相似性。
* 确定阈值：设置一个相似性阈值，只有当两个指纹的相似度超过这个阈值时，才认为它们代表相似或重复的记录。
* 处理相似记录：对于被标记为相似的记录，可以进一步人工审查或自动合并，以消除重复。

### deduplicate.py用法

`deduplicate.py` 用于将datasets中以模型命名的(例如：'datasets/qwen').json数据进行去重，输出去重后的数据到 `datasets/qwen/dedup` 文件夹下。代码见 `datasets/processed` 文件夹。
