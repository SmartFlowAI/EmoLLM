"""Care's search resolver, independent of model and audio dependencies."""

import asyncio
import logging
import os
from uuid import uuid4

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


PARALLEL_URL = "https://search.parallel.ai/mcp"
LANGSEARCH_URL = "https://api.langsearch.com/v1/web-search"
USER_AGENT = "EmoLLM-Care/1.0 (+https://github.com/SmartFlowAI/EmoLLM)"
SEARCH_TIMEOUT = 20.0
logger = logging.getLogger(__name__)


def new_conversation_id():
    """Called by Gradio for each browser session and when Clear starts a new chat."""
    return str(uuid4())


def resolve_provider():
    """An explicit choice wins; existing LangSearch credentials retain their use."""
    explicit = os.getenv("CAREYOU_SEARCH_PROVIDER")
    if explicit is not None:
        provider = explicit.strip().lower()
        if provider not in ("parallel", "langsearch", "off"):
            raise ValueError("CAREYOU_SEARCH_PROVIDER must be parallel, langsearch or off")
        return provider
    return "langsearch" if os.getenv("LANGSEARCH_API_KEY", "").strip() else "parallel"


async def _parallel_search(client, query, conversation_id):
    async with streamable_http_client(PARALLEL_URL, http_client=client) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            if not any(tool.name == "web_search" for tool in tools.tools):
                raise ValueError("Search MCP does not offer web_search")
            result = await session.call_tool("web_search", {
                "objective": query,
                "search_queries": [query],
                "session_id": conversation_id,
            })
            if result.isError:
                raise ValueError("Search MCP returned a tool error")
            # Keep source URLs and excerpts together in the model's context.
            return "\n".join(block.text for block in result.content if block.type == "text")


async def _langsearch(client, query):
    key = os.getenv("LANGSEARCH_API_KEY", "").strip()
    if not key:
        raise ValueError("LangSearch requires LANGSEARCH_API_KEY")
    response = await client.post(LANGSEARCH_URL, headers={"Authorization": f"Bearer {key}"},
                                 json={"query": query, "freshness": "noLimit", "summary": True, "count": 10})
    response.raise_for_status()
    results = response.json()["data"]["webPages"]["value"]
    return "\n".join(
        f"标题: {item.get('name', '')}\n摘要: {item.get('snippet', '')}\n链接: {item.get('url', '')}\n"
        for item in results
    )


async def _search(query, conversation_id, provider, cancelled):
    # Keep deployment proxy/CA settings; provider credentials are added only for LangSearch.
    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT},
                                 timeout=SEARCH_TIMEOUT) as client:
        call = _parallel_search(client, query, conversation_id) if provider == "parallel" else _langsearch(client, query)
        task = asyncio.create_task(call)
        try:
            while not task.done():
                if cancelled():
                    return ""
                await asyncio.wait({task}, timeout=0.05)
            return await task
        finally:
            if not task.done():
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)


def search_web(query, conversation_id, enabled=True, cancelled=lambda: False):
    """Return prompt context, or empty context on disabled/failed/cancelled search.

    The selected provider is never replaced after an error. The caller owns the
    conversation ID, so retries and subsequent turns retain it across connections.
    """
    if not enabled or cancelled():
        return ""
    try:
        provider = resolve_provider()
        if provider == "off":
            return ""
        return asyncio.run(asyncio.wait_for(
            _search(query, conversation_id, provider, cancelled), timeout=SEARCH_TIMEOUT
        ))
    except Exception as exc:
        # Do not put sensitive queries, credentials or provider response bodies in logs.
        logger.warning("Web search unavailable (%s)", type(exc).__name__)
        return ""
