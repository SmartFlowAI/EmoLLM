# 🧠 An AI assistant with extensive knowledge in psychology, and my name is Care.

## 🚀 Overview
This model is finetuned on deepseek-r1. If this repo helps you, star and share it ❤️. This repo will be continuously merged into EmoLLM.

<td colspan="3" align="center" style="background-color: transparent;">
    <img src="assets\careyou.png" alt="占位图" style="width: 100%; height: auto;">
</td>

## ✨ Functions
✅Provide an interactive chat interface for psychological consultation seekers.

✅Integrate knowledge retrieval 

✅Integrate web searching

✅two customized tts (ISSUE: more voice models)

❌Virtual mental companion 

## ⚠️ issue status
- 2025.4.29 fix bug of clearing and stopping op.
- 2025.5.3 web search supports.
- 2025.5.5 rag supports. (demo code, needs to be checked)
- 2025.5.7 fix bug of rag.
- 2025.5.9 tts supports.
- 2025.5.10 two voice models.
- 2025.5.16 merge into EmoLLM.

## 🤖 How to run
The code can be directly run on modelscope gpu. If you do not have this resource, please modify some details to run it on your local server.
- step1: create a repo named careyou in modelscope and copy all the files under `careyou` to the repo.
- step2: obtain langsearch API key (free) and set it as an env var `LANGSEARCH_API_KEY`.
- step3: run the application through modelscope platform.

## 🙏 Acknowledgments
We are grateful to Modelscope for supporting this project with resources.

The rag codes are based on [EmoLLM](https://github.com/SmartFlowAI/EmoLLM)

## 🤝 Contributing
Feel free to contribute to this project via our [github repo](https://github.com/HaiyangPeng/careyou). Grow together!