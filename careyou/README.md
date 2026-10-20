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
- step2: web search works without a search API key. Existing `LANGSEARCH_API_KEY` settings continue to use LangSearch.
- step3: run the application through modelscope platform.

## Web search

Care uses free [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
(Fast mode) when no search provider is configured. No account or API key is
needed for light use. The current message is sent to the selected search provider
and returned excerpts and source URLs are included in the model prompt.
Uncheck **Web search** before sending a message to keep that message out of web search.
Set `CAREYOU_SEARCH_PROVIDER=off` to disable search for the deployment.

If `LANGSEARCH_API_KEY` is set, Care keeps using LangSearch. To choose explicitly,
set `CAREYOU_SEARCH_PROVIDER=parallel` or `CAREYOU_SEARCH_PROVIDER=langsearch`.
Explicit LangSearch requires its key. Provider errors, rate limits and a
20-second search timeout leave the search context empty; they never switch
providers. Stop cancels an in-flight search. Clear starts a new conversation;
related searches within a chat share an opaque conversation ID.

Search dependencies require Python 3.10+ and are included by `requirements.txt`.
The search path can also be checked without downloading the model or audio stack:

```bash
python -m venv /tmp/care-search-venv
/tmp/care-search-venv/bin/pip install -r careyou/requirements-search.txt
/tmp/care-search-venv/bin/python -m unittest discover -s careyou/tests -v
```

These tests use scripted model inference and a local MCP transport fixture.
Running the full app still requires the existing GPU, model, RAG and TTS setup.

## 🙏 Acknowledgments
We are grateful to Modelscope for supporting this project with resources.

The rag codes are based on [EmoLLM](https://github.com/SmartFlowAI/EmoLLM)

## 🤝 Contributing
Feel free to contribute to this project via our [github repo](https://github.com/HaiyangPeng/careyou). Grow together!