# EmoLLM's datasets

* Category of dataset: **General** and **Role-play**
* Type of data: **QA** and **Conversation**
* Summary: General(**6 datasets**), Role-play(**3 datasets**)

 ## Category
* **General**: generic dataset, including psychological Knowledge, counseling technology, etc.
* **Role-play**: role-playing dataset, including character-specific conversation style data, etc.

## Type
* **QA**: question-and-answer pair
* **Conversation**: multi-turn consultation dialogue

## Summary

|   Category  |        Dataset        |     Type     |  Total  |
| :---------: | :-------------------: | :----------: | :-----: |
|  *General*  |         data          | Conversation |  5600+  |
|  *General*  |       data_pro        | Conversation | 36500+  |
|  *General*  | multi_turn_dataset_1  | Conversation | 36,000+ |
|  *General*  | multi_turn_dataset_2  | Conversation | 27,000+ |
|  *General*  | single_turn_dataset_1 |      QA      | 14000+  |
|  *General*  | single_turn_dataset_2 |      QA      | 18300+  |
| *Role-play* |         aiwei         | Conversation |  4000+  |
| *Role-play* |       SoulStar        |      QA      | 11200+  |
| *Role-play* |        tiangou        | Conversation |  3900+  |
|     ……      |          ……           |      ……      |   ……    |


## Source
**General**：
* dataset `data` from this repo
* dataset `data_pro` from this repo
* dataset `multi_turn_dataset_1` from [Smile](https://github.com/qiuhuachuan/smile)
* dataset `multi_turn_dataset_2` from [CPsyCounD](https://github.com/CAS-SIAT-XinHai/CPsyCoun)
* dataset `single_turn_dataset_1` from this repo
* dataset `single_turn_dataset_2` from this repo

**Role-play**：
* dataset `aiwei` from this repo
* dataset `tiangou` from this repo
* dataset `SoulStar` from [SoulStar](https://github.com/Nobody-ML/SoulStar)

**Dataset Deduplication**：
Combine absolute matching with fuzzy matching (Simhash) algorithms to deduplicate the dataset, thereby enhancing the effectiveness of the fine-tuning model. While ensuring the high quality of the dataset, the risk of losing important data due to incorrect matches can be reduced via adjusting the threshold.

https://algonotes.readthedocs.io/en/latest/Simhash.html