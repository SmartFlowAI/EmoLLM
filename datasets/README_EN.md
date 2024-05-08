# EmoLLM's datasets

* Category of dataset: **General** and **Role-play**
* Type of data: **QA** and **Conversation**
* Summary: General(**8 datasets**), Role-play(**5 datasets**)

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

## Source

**General**：
* dataset `data` from this repo
* dataset `data_pro` from this repo
* dataset `multi_turn_dataset_1` from [Smile](https://github.com/qiuhuachuan/smile)
* dataset `multi_turn_dataset_2` from [CPsyCounD](https://github.com/CAS-SIAT-XinHai/CPsyCoun)
* dataset `single_turn_dataset_1` from this repo
* dataset `single_turn_dataset_2` from this repo
* dataset `self_cognition_EmoLLM` from this repo
* dataset `ruozhiba_raw` from [COIG-CQIA](https://huggingface.co/datasets/m-a-p/COIG-CQIA/viewer/ruozhiba)

**Role-play**：
* dataset `aiwei` from this repo
* dataset `tiangou` from this repo
* dataset `SoulStar` from [SoulStar](https://github.com/Nobody-ML/SoulStar)
* dataset `mother` from this repo
* dataset `scientist` from this repo

## Dataset Deduplication

Combine absolute matching with fuzzy matching (Simhash) algorithms to deduplicate the dataset, thereby enhancing the effectiveness of the fine-tuning model. While ensuring the high quality of the dataset, the risk of losing important data due to incorrect matches can be reduced by adjusting the threshold.

### Simhash Algorithm Introduction

Simhash is an algorithm used to detect similar or duplicate items in large amounts of data. It works by converting text into a set of numerical fingerprints that have a high degree of similarity for similar text. The Simhash algorithm is particularly effective for processing text data, especially when dealing with large amounts of data. Detailed introduction can be found in[Simhash](https://algonotes.readthedocs.io/en/latest/Simhash.html).

### Simhash realization steps

* Text preprocessing: Convert text data into a format suitable for Simhash processing. This may include word segmentation, stop word removal, stemming, etc.
* Generate Simhash fingerprints: Apply the Simhash algorithm to the preprocessed text to generate a set of numerical fingerprints. Each fingerprint represents a hash of the text content.
* Compare fingerprints: Identify duplicate or similar records by comparing the similarity of hash values. The characteristic of Simhash is that the generated hash values have a high degree of similarity even when the text has a small amount of difference.
* Determine threshold: Set a similarity threshold. Only when the similarity of two fingerprints exceeds this threshold, they are considered to represent similar or duplicate records.
* Process similar records: Records marked as similar can be further manually reviewed or automatically merged to eliminate duplication.

### `deduplicate.py` Usage

`deduplicate.py` is used to deduplicate the .json data named after the model in datasets (for example: 'datasets/qwen'), and output the deduplicated data to the `datasets/qwen/dedup` folder. See the code in the `datasets/processed` folder.

