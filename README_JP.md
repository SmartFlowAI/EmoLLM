<div align="center"> 

# EmoLLM - メンタルヘルスのための大規模言語モデル

</div>

<p align="center">
  <a href="https://github.com/SmartFlowAI/EmoLLM/">
    <img src="assets/EmoLLM_transparent.png" alt="Logo" width="50%">
  </a>

<div align="center">

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![OpenXLab_App][OpenXLab_App-image]][OpenXLab_App-url]
[![OpenXLab_Model][OpenXLab_Model-image]][OpenXLab_Model-url] 
[![MIT License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]

</div>

<h3 align="center">EmoLLM</h3>

  <p align="center">
  <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a> | 日本語
    <br />
    <br />
    <a href="https://github.com/SmartFlowAI/EmoLLM"><strong>このプロジェクトのドキュメントを探索する »</strong></a>
    <br />
    <br />
    <a href="https://openxlab.org.cn/apps/detail/Farewell1/EmoLLMV2.0">EmoLLM 2.0 デモ</a>
    ·
    <a href="https://github.com/SmartFlowAI/EmoLLM/issues">バグを報告する</a>
    ·
    <a href="https://github.com/SmartFlowAI/EmoLLM/issues">新機能を提案する</a>
  </p>

</p>

<!-- 本篇README.md面向开发者 -->

**EmoLLM** は、メンタルヘルスカウンセリングにおいて顧客を理解し、サポートし、助けるために設計された大規模言語モデルのシリーズです。LLMの指示から微調整されています。スターをいただけると嬉しいです~⭐⭐。オープンソースの構成は以下の通りです：

<div align="center">

|         モデル         |       タイプ       | ファイルリンク  | モデルリンク  |
| :-------------------: | :------: | :------------------------------------------------------------------------------------------------------: |:------: |
|   Deepseek-R1_14b_int4   |  QLoRA   |  unsloth | [ModelScope](https://www.modelscope.cn/models/haiyangpengai/careyou_7b_16bit_v3_2_qwen14_4bit) |
|   InternLM2_5_7B_chat   |  全量微調整   |  [internlm2_5_chat_7b_full.py](./xtuner_config/internlm2_5_chat_7b_full.py) | [OpenXLab](https://openxlab.org.cn/models/detail/chg0901/EmoLLM_V3.0), [ModelScope](https://modelscope.cn/models/chg0901/EmoLLMV3.0) |
|   InternLM2_5_7B_chat   |  QLoRA   |  [internlm2_5_chat_7b_qlora_oasst1_e3.py](./xtuner_config/internlm2_5_chat_7b_qlora_oasst1_e3.py) |[ModelScope](https://www.modelscope.cn/models/z342994309/emollm_interlm2_5/)  |
|   InternLM2_7B_chat   |  QLoRA   |  [internlm2_7b_chat_qlora_e3.py](./xtuner_config/internlm2_7b_chat_qlora_e3.py) | [ModelScope](https://modelscope.cn/models/aJupyter/EmoLLM/files) |
|   InternLM2_7B_chat   | 全量微調整 | [internlm2_chat_7b_full.py](./xtuner_config/internlm2_chat_7b_full.py)  | [OpenXLab](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full) |
|   InternLM2_7B_base   |  QLoRA   | [internlm2_7b_base_qlora_e10_M_1e4_32_64.py](./xtuner_config/internlm2_7b_base_qlora_e10_M_1e4_32_64.py) |[OpenXLab](https://openxlab.org.cn/models/detail/chg0901/EmoLLM-InternLM7B-base-10e), [ModelScope](https://www.modelscope.cn/models/chg0901/EmoLLM-InternLM7B-base-10e/summary) |
|  InternLM2_1_8B_chat  | 全量微調整 |  [internlm2_1_8b_full_alpaca_e3.py](./xtuner_config/internlm2_1_8b_full_alpaca_e3.py)  | [OpenXLab](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_1_8b_full/tree/main), [ModelScope](https://modelscope.cn/models/aJupyter/EmoLLM_PT_InternLM1.8B-chat/files) |
|  InternLM2_20B_chat   |   LoRA   |[internlm2_20b_chat_lora_alpaca_e3.py](./xtuner_config/internlm2_20b_chat_lora_alpaca_e3.py)| |
|     Qwen_7b_chat      |  QLoRA   |  [qwen_7b_chat_qlora_e3.py](./xtuner_config/qwen_7b_chat_qlora_e3.py) | |
|   Qwen1_5-0_5B-Chat   | 全量微調整 |   [qwen1_5_0_5_B_full.py](./xtuner_config/qwen1_5_0_5_B_full.py) | [ModelScope](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary) |
|  Baichuan2_13B_chat   |  QLoRA   |   [baichuan2_13b_chat_qlora_alpaca_e3.py](./xtuner_config/baichuan2_13b_chat_qlora_alpaca_e3.py) | |
|      ChatGLM3_6B      |   LoRA   |   [chatglm3_6b_lora_alpaca_e3.py](./xtuner_config/chatglm3_6b_lora_alpaca_e3.py)  | |
| DeepSeek MoE_16B_chat |  QLoRA   |  [deepseek_moe_16b_chat_qlora_oasst1_e3.py](./xtuner_config/deepseek_moe_16b_chat_qlora_oasst1_e3.py)    | |
| Mixtral 8x7B_instruct |  QLoRA   | [mixtral_8x7b_instruct_qlora_oasst1_e3.py](./xtuner_config/mixtral_8x7b_instruct_qlora_oasst1_e3.py)    | |
| LLaMA3_8b_instruct    |  QLoRA   | [aiwei_llama3_8b_instruct_qlora_e3.py](./xtuner_config/aiwei_llama3_8b_instruct_qlora_e3.py) | [OpenXLab](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM-LLaMA3_8b_instruct_aiwei/tree/main), [ModelScope](https://modelscope.cn/models/aJupyter/EmoLLM-LLaMA3_8b_instruct_aiwei/files) |
| LLaMA3_8b_instruct    |  QLoRA   | [llama3_8b_instruct_qlora_alpaca_e3_M_ruozhi_scM.py](./xtuner_config/llama3_8b_instruct_qlora_alpaca_e3_M_ruozhi_scM.py)    |[OpenXLab](https://openxlab.org.cn/models/detail/chg0901/EmoLLM-Llama3-8B-Instruct3.0), [ModelScope](https://modelscope.cn/models/chg0901/EmoLLM-Llama3-8B-Instruct3.0/summary) |
|          ……           |    ……    |                                                    ……                                                    | …… |


</div>

🎉このプロジェクトに貢献してくださる方を歓迎します！

🔍LLMの原理や底层実装に興味がある方は、[ThinkLLM](https://github.com/aJupyter/ThinkLLM)に注目してください。大規模モデルの各種コンポーネントをゼロから実装することに注力しています。

---

このモデルは、個人、グループ、社会のメンタルヘルスを完全に理解し、促進することを目的としています。このモデルには通常、以下の主要なコンポーネントが含まれます：

- 認知要因：個人の思考パターン、信念システム、認知バイアス、問題解決能力に関するもの。認知要因は、個人が人生の出来事をどのように解釈し、対応するかに影響を与えるため、メンタルヘルスに大きな影響を与えます。
- 感情要因：感情の調整、感情の表現、感情の経験を含む。感情の健康はメンタルヘルスの重要な部分であり、個人が感情をどのように管理し、表現し、負の感情からどのように回復するかに関与します。
- 行動要因：個人の行動パターン、習慣、対処戦略に関するもの。これには、ストレス管理スキル、社交スキル、自己効力感（自分の能力に対する自信）が含まれます。
- 社会環境：家族、仕事、コミュニティ、文化的背景などの外部要因であり、これらは個人のメンタルヘルスに直接的および間接的な影響を与えます。
- 身体の健康：身体の健康とメンタルヘルスは密接に関連しています。良好な身体の健康はメンタルヘルスを促進し、その逆もまた然りです。
- 心理的レジリエンス：逆境から回復し、適応する個人の能力を指します。心理的レジリエンスが強い人は、挑戦から回復し、それから学び、成長することができます。
- 予防および介入措置：メンタルヘルスの大規模モデルには、心理的問題を予防し、メンタルヘルスを促進するための戦略も含まれます。これには、心理教育、カウンセリング、治療、社会的支援システムが含まれます。
- 評価および診断ツール：メンタルヘルスを効果的に促進するためには、個人の心理状態を評価し、潜在的な心理的問題を診断するための科学的なツールが必要です。

<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td align="center" style="background-color: transparent; width: 50%;">
            <img src="assets\aiwei_demo.gif" alt="占位图" style="width: 100%; height: auto;">
        </td>
        <td align="center" style="background-color: transparent; width: 50%;">
            <img src="assets\aiwei_demo2.gif" alt="占位图" style="width: 100%; height: auto;">
        </td>
    </tr>
    <tr>
        <td align="center" style="background-color: transparent; width: 50%;">
            <img src="assets\aiwei_demo3.gif" alt="占位图" style="width: 100%; height: auto;">
        </td>
        <td align="center" style="background-color: transparent; width: 50%;">
            <img src="assets\aiwei_demo4.gif" alt="占位图" style="width: 100%; height: auto;">
        </td>
    </tr>
    <tr>
        <td colspan="3" align="center" style="background-color: transparent;">
            <img src="careyou\assets\careyou.png" alt="占位图" style="width: 100%; height: auto;">
        </td>
    </tr>
</table>

## 最近の更新
- 【2025.5】[AI心理アシスタント-ディープ思考版（Caryou）](https://github.com/HaiyangPeng/careyou)：EmoLLM-心理デジタルヒューマンセクション（現在は深い思考、Rag、web search、tts機能を完了）は、EmoLLMに統合されており、プロジェクトの最適化と改善にご参加ください。
- 【2025.5】[deepwiki-EmoLLM](https://deepwiki.com/SmartFlowAI/EmoLLM): このプロジェクトに基づいてよりスマートなプロジェクト＆ドキュメント理解を行うことができます。
- 【2025.4】 [ThinkLLM](https://github.com/aJupyter/ThinkLLM/tree/main/LLM) は、大規模言語モデルの軽量で効率的な実装リポジトリであり、BPEトレーニングガイド（EmoLLMをサポート）を提供しています。
- 【2025.3】 InternLM2.5-7B-chat のフルファインチューニングに基づいて、[EmoLLM (GGUF形式、fp16精度)](https://huggingface.co/collections/L0ve1ace/psychology-llm-gguf-67cc766eaf0a3f01c6e39aa6) がリリースされました。操作方法については後日更新されます。@Rycen7822 @Slipstream-Max
- 【2025.2】 最初のメンタルヘルス R1 スティルデータセットを更新しました。[psychology-10k-Deepseek-R1-zh.json](./datasets/psychology-10k-Deepseek-R1-zh.json) @Kedreamix
- 【2024.09.14】 Qwen2-7B-Instruct モデルに基づく Lora ファインチューニングモデルがオープンソース化されました。ファインチューニング設定ファイルアドレス: [Qwen2-7B-Instruct_lora.py](./xtuner_config/Qwen2-7B-Instruct_lora.py)、モデルウェイトリンク: [ModelScope](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen2-7B-Instruct_lora/)
- 【2024.08】 GLM4-9B-chat をベースにした Lora ファインチューニングモデルがオープンソース化されました（Llama-factory 基づく）。詳細は [Fine-tuning Tutorial](./doc/GLM-4-9B-chat%20Lora%20微调（llama-factory）.md) をご覧ください。モデルウェイトリンク: [ModelScope](https://www.modelscope.cn/models/wwewwt/EmoLLM-glm-4-9b-chat/summary)
- 【2024.07.16】 EmoLLM V3.0 を体験していただけます。このモデルは InternLM2.5-7B-Chat モデルに基づくフルファインチューニングバージョンです。ファインチューニング設定ファイルは [internlm2_5_chat_7b_full.py](./xtuner_config/internlm2_5_chat_7b_full.py) で見つけることができます。モデルウェイトは [OpenXLab](https://openxlab.org.cn/models/detail/chg0901/EmoLLM_V3.0)、[ModelScope](https://modelscope.cn/models/chg0901/EmoLLMV3.0) でご利用いただけます。WebDemo は [OpenXLab apps](https://openxlab.org.cn/apps/detail/chg0901/EmoLLMV3.0)、[Zhihu 上のフルファインチューニングチュートリアル](https://zhuanlan.zhihu.com/p/708931911) でご利用いただけます。
- 【2024.7】EmoLLM V2.0の安定版を日常使用および学術研究にご利用ください。モデルの重みリンク：[OpenXLab](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full/tree/main)。
- 【2024.7】InternLM2_5_7B_chatの微調整構成を追加しました。[ModelScope](https://www.modelscope.cn/models/z342994309/emollm_interlm2_5/)。
- 【2024.6】[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)の[GLM4-9B-chat微調整ガイド](./doc/GLM-4-9B-chat%20Lora%20微调（llama-factory）.md)を追加しました。[swiftベースの微調整ガイド](./swift/)を追加しました。論文[ESC-Eval: Evaluating Emotion Support Conversations in Large Language Models](https://arxiv.org/abs/2406.14952)がEmoLLMを引用し、EmoLLMが良好な結果を達成しました。
- 【2024.05.28】EmoLLMが使用するマルチターン対話データセット**CPsyCunD**と**専門評価方法**が公開されました。詳細は2024 ACL findings[《CPsyCoun: A Report-based Multi-turn Dialogue Reconstruction and Evaluation Framework for Chinese Psychological Counseling》](https://arxiv.org/abs/2405.16433)をご覧ください！
- [2024.05.08] EmoLLM**Daddy-like BF V0.1**が[1. **Baidu AppBuilder**](https://appbuilder.baidu.com/s/4cLyw)と[2. **OpenXLab**](https://openxlab.org.cn/apps/detail/chg0901/EmoLLM3.0_Gradio_Llama3-8B-Instruct3.0)で公開されました。ぜひ「いいね」と「コレクション」に追加してください！
- [2024.05.07] [インクリメンタルプレトレーニングガイド](xtuner_config/pt/README.md)
- [2024.05.04] [LLaMA3_8b_instructベースのEmoLLM3.0 OpenXLabデモ](https://st-app-center-006861-9746-jlroxvg.openxlab.space/)が公開されました（[再起動リンク](https://openxlab.org.cn/apps/detail/chg0901/EmoLLM-Llama3-8B-Instruct3.0)）、[LLAMA3微調整ガイド](xtuner_config/README_llama3_8b_instruct_qlora_alpaca_e3_M.md)が更新されました。LLaMA3_8b_instruct-8B QLoRA微調整モデルEmoLLM3.0の重みが[**OpenXLab**](https://openxlab.org.cn/models/detail/chg0901/EmoLLM-Llama3-8B-Instruct3.0)と[**ModelScope**](https://modelscope.cn/models/chg0901/EmoLLM-Llama3-8B-Instruct3.0/summary)プラットフォームで公開されました。
- [2024.04.20] [LLAMA3微調整ガイド](xtuner_config/README_llama3_8b_instruct_qlora_alpaca_e3_M.md)と[LLaMA3_8b_instructのaiwei](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM-LLaMA3_8b_instruct_aiwei)がオープンソース化されました。
- [2023.04.14] [クイックスタート](docs/quick_start_EN.md)とナニー級チュートリアル[BabyEmoLLM](Baby_EmoLLM.ipynb)を追加しました。
- [2024.04.02] Huggingfaceに[Old Mother Counsellor](https://huggingface.co/brycewang2018/EmoLLM-mother/tree/main)をアップロードしました。
- [2024.03.25] [Mother-like Therapist]がHuggingfaceで公開されました（https://huggingface.co/brycewang2018/EmoLLM-mother/tree/main）。
- [2024.03.25] [Daddy-like Boy-Friend]がBaidu Paddle-Paddle AI Studioプラットフォームで公開されました（https://aistudio.baidu.com/community/app/68787）。


<details>
<summary>もっと見る</summary>

- [2024.03.24] **InternLM2-Base-7B QLoRA微調整モデル**が**OpenXLab**と**ModelScope**プラットフォームで公開されました。詳細は[**InternLM2-Base-7B QLoRA**](./xtuner_config/README_internlm2_7b_base_qlora.md)をご覧ください。
- [2024.03.12] [aiwei]がBaidu Paddle-Paddle AI Studioプラットフォームで公開されました（https://aistudio.baidu.com/community/app/63335）。
- [2024.03.11] **EmoLLM V2.0はEmoLLM V1.0と比較して全体的に向上し、心理カウンセリングタスクにおいてRole-playing ChatGPTを上回る能力を持っています！** [EmoLLM V2.0を体験する](https://openxlab.org.cn/apps/detail/Farewell1/EmoLLMV2.0)、[データセットの統計と詳細情報](./datasets/)、[ロードマップ](./assets/Roadmap_ZH.png)を更新しました。
- [2024.03.09] 同時実行機能を追加して[QAペア生成](./scripts/qa_generation/)、[RAGパイプライン](./rag/)を加速しました。
- [2024.03.03] [InternLM2-7B-chat全量微調整バージョンEmoLLM V2.0がオープンソース化されました](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full)、2つのA100*80Gが必要です。専門評価を更新しました。詳細は[evaluate](./evaluate/)をご覧ください。PaddleOCRベースのPDFからtxtへの変換ツールスクリプトを更新しました。詳細は[scripts](./scripts/)をご覧ください。
- [2024.02.29] 客観的評価計算を更新しました。詳細は[evaluate](./evaluate/)をご覧ください。一連のデータセットを更新しました。詳細は[datasets](./datasets/)をご覧ください。
- [2024.02.27] 英語のREADMEと一連のデータセット（リッキングドッグとワンターン対話）を更新しました。
- [2024.02.23] InternLM2_7B_chat_qloraベースの「優しいお姉さん心理カウンセラーAi Wei」をリリースしました。[モデルの重みを取得する](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei)、[構成ファイル](xtuner_config/aiwei-internlm2_chat_7b_qlora.py)、[オンライン体験リンク](https://openxlab.org.cn/apps/detail/ajupyter/EmoLLM-aiwei)。
- [2024.02.23] [いくつかの微調整構成](/xtuner_config/)を更新しました。[data_pro.json](/datasets/data_pro.json)（より多くの量、より包括的なシナリオ、より豊富な内容）と[aiwei.json](/datasets/aiwei.json)（優しいお姉さんのロールプレイ専用、Emoji表現を含む）を追加しました。「優しいお姉さん心理カウンセラーAi Wei」が近日公開予定です。
- [2024.02.18] [Qwen1_5-0_5B-Chat全量微調整バージョンがオープンソース化されました](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary)。計算リソースが限られている方もぜひお試しください。

- [2024.02.06] [Qwen1_5-0_5B-Chat全量微調整バージョンがオープンソース化されました](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary)。計算リソースが限られている方もぜひお試しください。

<p align="center"> 
  <img src="https://github.com/SmartFlowAI/EmoLLM/assets/62385492/7e931682-c54d-4ded-bc67-79130c68d744" alt="モデルダウンロード数">
</p>

- [2024.02.05] プロジェクトが公式WeChatアカウントNLP Engineeringで紹介されました。記事の[リンク](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)はこちらです。皆さんのフォローをお待ちしています！！ 🥳🥳

<p align="center">
  <img src="https://github.com/SmartFlowAI/EmoLLM/assets/62385492/47868d6a-2e91-4aa9-a630-e594c14295b4" alt="公式WeChatアカウントのQRコード">
</p>

- [2024.02.03] [プロジェクトビデオ](https://www.bilibili.com/video/BV1N7421N76X/)がbilibiliで公開されました 😊
- [2024.01.27] データ構築ドキュメント、微調整ガイド、デプロイメントガイド、Readmeなどの関連ドキュメントを完成させました 👏
- [2024.01.25] EmoLLM V1.0がオンラインでデプロイされました https://openxlab.org.cn/apps/detail/jujimeizuo/EmoLLM 😀

</details>

## 栄誉

- プロジェクトは、**2024浦源大模型シリーズチャレンジ春季大会**で**イノベーションとクリエイティビティ賞**を受賞しました。

<p align="center">
   <a href="https://github.com/SmartFlowAI/EmoLLM/">
    <img src="assets/Shusheng.png" alt="チャレンジイノベーションとクリエイティビティ賞">
</p>


- [AI-enabled university programme "National College Tour"](https://mp.weixin.qq.com/s/yyaulQ1wBzKq5cXaGl2Wag)で一等賞を受賞しました。
- プロジェクトは公式WeChatアカウント**NLP Engineering**で紹介されました。記事の[リンク](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)はこちらです。

## ロードマップ

- 🎉以下のメディアおよび友人の皆様に、このプロジェクトの報道とサポートに感謝します（以下、順不同！省略があれば申し訳ありませんが、感謝しています！追加を歓迎します！）：[NLP工程化](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)、[机智流](https://mp.weixin.qq.com/s/_wMCmssRMGd0Oz5OVVkjAA)、[爱可可爱生活](https://mp.weixin.qq.com/s/4WaCg4OpkCWXEuWHuV4r3w)、[阿郎小哥](https://mp.weixin.qq.com/s/_MSMeL1XHP0v5lDi3YaPVw)、[大模型日知路](https://mp.weixin.qq.com/s/FYYibsCXtfU6FFM9TuKILA)、[AI Code](https://mp.weixin.qq.com/s/yDWGY3S4CwCi6U_irsFmqA)など！

- プロジェクトビデオ[EmoLLM](https://www.bilibili.com/video/BV1N7421N76X/)が公開されました。ぜひご覧ください！ 😀

<p align="center">
  <a href="https://github.com/SmartFlowAI/EmoLLM/">
    <img src="assets/Roadmap_EN.png" alt="ロードマップ_EN">
  </a>

## コンテンツ

- [EmoLLM - メンタルヘルスのための大規模言語モデル](#emollm---メンタルヘルスのための大規模言語モデル)
  - [最近の更新](#最近の更新)
  - [栄誉](#栄誉)
  - [ロードマップ](#ロードマップ)
  - [コンテンツ](#コンテンツ)
          - [開発前の構成要件](#開発前の構成要件)
          - [ユーザーガイド](#ユーザーガイド)
    - [🍪クイックスタート](#クイックスタート)
    - [📌データ構築](#データ構築)
    - [🎨微調整ガイド](#微調整ガイド)
    - [🔧デプロイメントガイド](#デプロイメントガイド)
    - [⚙RAG（検索強化生成）](#rag検索強化生成)
    - [🎓評価ガイド](#評価ガイド)
    - [使用されたフレームワーク](#使用されたフレームワーク)
      - [このプロジェクトに参加する方法](#このプロジェクトに参加する方法)
    - [バージョン管理](#バージョン管理)
    - [著者（順不同）](#著者順不同)
    - [著作権表示](#著作権表示)
    - [引用](#引用)
    - [謝辞](#謝辞)
      - [関連プロジェクト](#関連プロジェクト)
      - [人々](#人々)
  - [スター履歴](#スター履歴)
  - [🌟 貢献者](#-貢献者)
  - [コミュニケーショングループ](#コミュニケーショングループ)

###### 開発前の構成要件

- A100 40G（特にInternLM2_7B_chat + qlora微調整 + deepspeed zero2最適化用）

###### ユーザーガイド

1. リポジトリをクローンする

```sh
git clone https://github.com/SmartFlowAI/EmoLLM.git
```

1. 順番に読むか、興味のあるセクションを読む：
   - [クイックスタート](#クイックスタート)
   - [データ構築](#データ構築)
   - [微調整ガイド](#微調整ガイド)
   - [デプロイメントガイド](#デプロイメントガイド)
   - [RAG](#rag検索強化生成)
   - [評価ガイド](#評価ガイド)
   - 詳細を表示


### 🍪クイックスタート
- [クイックスタート](quick_start/quick_start_EN.md)を参照してください。
- クイックコーディング：[Baby EmoLLM](quick_start/Baby_EmoLLM.ipynb)

### 📌データ構築

- [データ構築ガイド](generate_data/tutorial_EN.md)を参照してください。

- この微調整に使用されたデータセットは[datasets](datasets/data.json)にあります。

### 🎨微調整ガイド

詳細は[微調整ガイド](xtuner_config/README_EN.md)を参照してください。

### 🔧デプロイメントガイド

- デモデプロイメント：詳細は[デプロイメントガイド](./demo/README_EN.md)を参照してください。
- [LMDeploy](https://github.com/InternLM/lmdeploy/)に基づく定量デプロイメント：詳細は[deploy](./deploy/lmdeploy_EN.md)を参照してください。

### ⚙RAG（検索強化生成）

- 詳細は[RAG](rag/README_EN.md)を参照してください。

### 🎓評価ガイド

- モデル評価は**一般的な指標評価**と**専門的な指標評価**に分かれています。詳細は[評価ガイド](evaluate/README.md)を参照してください。

<details>
<summary>追加の詳細</summary>

### 使用されたフレームワーク

- [Xtuner](https://github.com/InternLM/xtuner)
- [Transformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)
- [LMDeploy](https://github.com/InternLM/lmdeploy/): 定量デプロイメント用
- [Stremlit](https://streamlit.io/): デモ構築用
- [DeepSpeed](https://github.com/microsoft/DeepSpeed): 並列トレーニング用
- …

#### このプロジェクトに参加する方法

貢献は、オープンソースコミュニティを学習、インスピレーション、創造の素晴らしい場所にします。あなたの貢献は非常に感謝されます。

1. プロジェクトをフォークする
2. フィーチャーブランチを作成する（`git checkout -b feature/AmazingFeature`）
3. 変更をコミットする（`git commit -m 'Add some AmazingFeature'`）
4. ブランチにプッシュする（`git push origin feature/AmazingFeature`）
5. プルリクエストを開く

### バージョン管理

このプロジェクトはバージョン管理にGitを使用しています。現在利用可能なバージョンはリポジトリで確認できます。

</details>

### 著者（順不同）

|                          ユーザー名                          |                     学校/組織                     |                             備考                             |                             貢献                             |
| :----------------------------------------------------------: | :-----------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|           [aJupyter](https://github.com/aJupyter)            |              南開大学、修士課程在籍               |                      DataWhaleメンバー                       |                      プロジェクト発起人                      |
|           [MING-ZCH](https://github.com/MING-ZCH)            |               華中科技大学、学部生                |                  LLM X メンタルヘルス研究者                  |                   プロジェクト共同リーダー                   |
|         [jujimeizuo](https://github.com/jujimeizuo)          |              江南大学、修士課程在籍               |                                                              |                                                              |
| [Smiling-Weeping-zhr](https://github.com/Smiling-Weeping-zhr) |         ハルビン工業大学（威海）、学部生          |                                                              |                                                              |
|             [8baby8](https://github.com/8baby8)              |   PaddlePaddleパイロットチーム地域ディレクター    |                   文心大モデルのコア開発者                   |                                                              |
|             [zxazys](https://github.com/zxazys)              |              南開大学、修士課程在籍               |                                                              |                                                              |
|   [JasonLLLLLLLLLLL](https://github.com/JasonLLLLLLLLLLL)    |               SWUFE（西南財経大学）               |                                                              |                                                              |
|            [MrCatAI](https://github.com/MrCatAI)             |                    AIムーバー                     |                                                              |                                                              |
|             [ZeyuBa](https://github.com/ZeyuBa)              |            自動化研究所、修士課程在籍             |                                                              |                                                              |
|   [aiyinyuedejustin](https://github.com/aiyinyuedejustin)    |         ペンシルベニア大学、修士課程在籍          |                                                              |                                                              |
|          [Nobody-ML](https://github.com/Nobody-ML)           |           中国石油大学（華東）、学部生            |                                                              |                                                              |
|            [chg0901](https://github.com/chg0901)             | [MiniSora](https://github.com/mini-sora/minisora) | [MiniSora](https://github.com/mini-sora/minisora)のメンテナーおよび管理者 | LLMの事前トレーニングと微調整、モデルのアップロード、データのクリーニング、ドキュメントの翻訳 |
|             [Mxoder](https://github.com/Mxoder)              |             北京航空航天大学、学部生              |                                                              |                                                              |
|           [Anooyman](https://github.com/Anooyman)            |            南京理工大学、修士課程在籍             |                                                              |                                                              |
|         [Vicky-3021](https://github.com/Vicky-3021)          |     西安電子科技大学、修士課程在籍（研究年0）     |                                                              |                                                              |
|        [SantiagoTOP](https://github.com/santiagoTOP)         |            太原理工大学、修士課程在籍             |                                                              | データのクリーニング、ドキュメント管理、Baby EmoLLMのメンテナンス |
|        [zealot52099](https://github.com/zealot52099)         |                    個人開発者                     |                                                              |                 データ処理、LLMの微調整とRAG                 |
|            [wwwyfff](https://github.com/wwwyfff)             |              復旦大学、修士課程在籍               |                                                              |                                                              |
|            [jkhumor](https://github.com/jkhumor)             |              南開大学、修士課程在籍               |                                                              |                             RAG                              |
|       [lll997150986](https://github.com/lll997150986)        |              南開大学、修士課程在籍               |                                                              |                            微調整                            |
|          [nln-maker](https://github.com/nln-maker)           |              南開大学、修士課程在籍               |                                                              |              フロントエンドとバックエンドの開発              |
|         [dream00001](https://github.com/dream00001)          |              南開大学、修士課程在籍               |                                                              |              フロントエンドとバックエンドの開発              |
|         [王几行XING](zhihu.com/people/brycewang1898)         |              北京大学、修士課程卒業               |                                                              | データ処理、LLMの微調整、フロントエンドとバックエンドの開発  |
|                            [思在]                            |     北京大学、修士課程卒業（マイクロソフト）      |                                                              |       LLMの微調整、フロントエンドとバックエンドの開発        |
|             [TingWei](https://github.com/wwewwt)             |            電子科技大学、修士課程卒業             |                                                              |                         LLMの微調整                          |
|            [PengYu](https://github.com/hi-pengyu)            |             石河子大学、修士課程在籍              |                                                              |                         LLMの微調整                          |
|          [Kedreamix](https://github.com/Kedreamix)           |              深圳大学、修士課程在籍               |                                                              |             初のメンタルヘルスR1蒸留データセット             |
|          [HaiyangPeng](https://github.com/HaiyangPeng)           |                       AIアルゴリズムエンジニア师                       |                              |      AI心理アシスタントの開発-深思考版       |
### 著作権表示

このプロジェクトはMITライセンスの下でライセンスされています。詳細については、[LICENSE](https://github.com/SmartFlowAI/EmoLLM/blob/master/LICENSE)を参照してください。

### 引用

もしこのプロジェクトがあなたの研究や仕事の助けになれば、以下の形式で引用してください：

```bibtex
@misc{2024EmoLLM,
    title={EmoLLM: Reinventing Mental Health Support with Large Language Models},
    author={EmoLLM Team},
    howpublished={\url{https://github.com/SmartFlowAI/EmoLLM}},
    year={2024}
}
```

#### タスクリスト
以下に EmoLLM を引用した研究・プロジェクトを記載します。（順不同。もし記載漏れがございましたら、ご報告いただけますと幸いです。）
- Yin C, Li F, Zhang S, et al. Mdd-5k: A new diagnostic conversation dataset for mental disorders synthesized via neuro-symbolic llm agents[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2025, 39(24): 25715-25723.
- Gu Q, Li S, Zheng T, et al. Steel-LLM: From Scratch to Open Source--A Personal Journey in Building a Chinese-Centric LLM[J]. arXiv preprint arXiv:2502.06635, 2025.
- Dai C, Hu J, Shi H, et al. Psyche-R1: Towards Reliable Psychological LLMs through Unified Empathy, Expertise, and Reasoning[J]. arXiv preprint arXiv:2508.10848, 2025.
- Wang M, Wang P, Wu L, et al. AnnaAgent: Dynamic Evolution Agent System with Multi-Session Memory for Realistic Seeker Simulation[J]. arXiv preprint arXiv:2506.00551, 2025.
- Feng Y, Wang Q, Liu K, et al. AI PsyRoom: Artificial Intelligence Platform for Segmented Yearning and Reactive Outcome Optimization Method[J]. arXiv preprint arXiv:2506.06740, 2025.


### 謝辞
#### 関連プロジェクト
- [CPsyCoun](https://github.com/CAS-SIAT-XinHai/CPsyCoun)
- [Smile](https://github.com/qiuhuachuan/smile)
- [SoulChat](https://github.com/scutcyr/SoulChat)

#### 人々
- [上海人工知能研究所](https://www.shlab.org.cn/)
- [Vansin](https://github.com/vansin)
- A.bu（心理学修士、北京大学）
- [Sanbuphy](https://github.com/sanbuphy)
- [HatBoy](https://github.com/hatboy)

<!-- links -->

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/in/aJupyter -->

<!-- 太少了，没必要放 -->

## スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=SmartFlowAI/EmoLLM&type=Date)](https://star-history.com/#SmartFlowAI/EmoLLM&Date)

## 🌟 貢献者

[![EmoLLM contributors](https://contrib.rocks/image?repo=SmartFlowAI/EmoLLM&max=50)](https://github.com/SmartFlowAI/EmoLLM/graphs/contributors)

[your-project-path]: SmartflowAI/EmoLLM
[contributors-shield]: https://img.shields.io/github/contributors/SmartflowAI/EmoLLM.svg?style=flat-square
[contributors-url]: https://github.com/SmartflowAI/EmoLLM/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SmartflowAI/EmoLLM.svg?style=flat-square
[forks-url]: https://github.com/SmartflowAI/EmoLLM/network/members
[stars-shield]: https://img.shields.io/github/stars/SmartflowAI/EmoLLM.svg?style=flat-square
[stars-url]: https://github.com/SmartflowAI/EmoLLM/stargazers
[issues-shield]: https://img.shields.io/github/issues/SmartflowAI/EmoLLM.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/SmartflowAI/EmoLLM.svg
[license-shield]: https://img.shields.io/github/license/SmartflowAI/EmoLLM.svg?style=flat-square
[license-url]: https://github.com/SmartFlowAI/EmoLLM/blob/main/LICENSE

[OpenXLab_App-image]: https://cdn-static.openxlab.org.cn/app-center/openxlab_app.svg
[OpenXLab_Model-image]: https://cdn-static.openxlab.org.cn/header/openxlab_models.svg
[OpenXLab_App-url]: https://openxlab.org.cn/apps/detail/Farewell1/EmoLLMV2.0
[OpenXLab_Model-url]: https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full

## コミュニケーショングループ

- 失敗した場合は、Issueセクションに移動してください。

<p align="center">
  <img  width="30%" src="https://github.com/SmartFlowAI/EmoLLM/assets/62385492/55ecd0aa-4832-4269-ad57-4c26f9aa286b" alt="EmoLLM公式コミュニケーショングループ">
</p>
