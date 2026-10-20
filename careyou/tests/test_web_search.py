"""Exercise the production chat callers without import-time GPU/model downloads.

Only inference, RAG and audio are scripted. The production search resolver, MCP
SDK and HTTP request construction execute unchanged against an HTTP fixture.
"""

import ast
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
from threading import Event, Thread
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import web_search


REAL_CLIENT = httpx.AsyncClient
APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP = ast.parse(APP_PATH.read_text())
CONTEXT = "Title: Reference\nExcerpt: useful current information\nURL: https://example.org/reference"


def load_chat():
    """Compile actual source nodes, leaving app startup/downloads unexecuted."""
    names = {"generate_response", "generate_response_and_tts", "stop_generation",
             "ParserState", "parse_response", "format_response", "format_time"}
    nodes = [node for node in APP.body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names]
    nodes += [node for node in APP.body if isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == "prompt_style" for target in node.targets)]
    calls = []

    class Tokenizer:
        def apply_chat_template(self, conversation, **kwargs):
            calls.append(conversation)
            return "scripted input"

        def __call__(self, *args, **kwargs):
            return SimpleNamespace(to=lambda device: SimpleNamespace(input_ids="scripted ids"))

    env = {"search_web": web_search.search_web, "Thread": Thread, "time": time,
           "tokenizer": Tokenizer(), "model": SimpleNamespace(device="cpu", generate=lambda **kwargs: None),
           "TextIteratorStreamer": lambda *args, **kwargs: iter(["A scripted answer.</think>"]),
           "rag_obj": SimpleNamespace(get_retrieval_content=lambda query: ["local knowledge"]),
           "get_tts_wav": lambda *args: "scripted audio"}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(APP_PATH), "exec"), env)
    return env, calls


def run_chat(query="current information", conversation_id=None, enabled=True, tts=True, active=None):
    env, prompts = load_chat()
    history = [[query, None]]
    args = [history, 0.6, 0.95, 64, active if active is not None else [True]]
    if tts:
        args += ["voice", "reference", "中文", "中文", "不切"]
    args += [conversation_id or web_search.new_conversation_id(), enabled]
    list(env["generate_response_and_tts" if tts else "generate_response"](*args))
    return prompts, history


class MCPFixture:
    def __init__(self, mode="success", sse=False):
        self.mode, self.sse = mode, sse
        self.requests = []
        self.started = Event()
        self.cancelled = Event()

    async def handle(self, request):
        body = json.loads(request.content) if request.content else {}
        self.requests.append((request, body))
        if str(request.url) == web_search.LANGSEARCH_URL:
            if self.mode == "http_error":
                return httpx.Response(401)
            return httpx.Response(200, json={"data": {"webPages": {"value": [
                {"name": "Reference", "snippet": "useful current information", "url": "https://example.org/reference"}
            ]}}})
        method = body.get("method")
        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "initialize":
            result = {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}},
                      "serverInfo": {"name": "search-fixture", "version": "1"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "web_search", "inputSchema": {
                "type": "object", "properties": {"objective": {"type": "string"},
                "search_queries": {"type": "array", "items": {"type": "string"}},
                "session_id": {"type": "string"}}, "required": ["objective", "search_queries"]}}]}
        elif method == "tools/call":
            self.started.set()
            if self.mode == "slow":
                try:
                    await asyncio.sleep(10)
                except asyncio.CancelledError:
                    self.cancelled.set()
                    raise
            if self.mode == "http_error":
                return httpx.Response(500)
            if self.mode == "malformed":
                return httpx.Response(200, text="invalid json", headers={"Content-Type": "application/json"})
            result = {"content": [{"type": "text", "text": "Free anonymous quota exceeded" if self.mode == "quota" else CONTEXT}],
                      "isError": self.mode == "quota"}
        else:
            raise AssertionError(f"Unexpected MCP request: {request.method} {body}")
        message = {"jsonrpc": "2.0", "id": body["id"], "result": result}
        if self.sse:
            return httpx.Response(200, content=f"event: message\ndata: {json.dumps(message)}\n\n",
                                  headers={"Content-Type": "text/event-stream"})
        return httpx.Response(200, json=message)

    @contextmanager
    def install(self, environment=None):
        def client(**kwargs):
            return REAL_CLIENT(**kwargs, transport=httpx.MockTransport(self.handle))
        # Deliberately remove all saved/ambient provider credentials and config.
        with patch.dict(os.environ, environment or {}, clear=True), patch.object(
                web_search.httpx, "AsyncClient", client):
            yield self

    def tool_calls(self):
        return [body["params"]["arguments"] for _, body in self.requests if body.get("method") == "tools/call"]


class SearchCallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.quiet = redirect_stdout(io.StringIO())
        cls.quiet.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.quiet.__exit__(None, None, None)

    def test_fresh_no_key_both_production_chat_callers_consume_mcp_results(self):
        for sse in (False, True):
            for tts in (False, True):
                fixture = MCPFixture(sse=sse)
                with fixture.install():
                    prompts, history = run_chat(tts=tts)
                prompt = prompts[-1][-1]["content"]
                self.assertIn(CONTEXT, prompt)
                self.assertIn("current information", prompt)
                self.assertIn("local knowledge" if tts else "", prompt)
                self.assertIn("scripted answer", history[-1][1])
                self.assertEqual({body.get("method") for _, body in fixture.requests},
                                 {"initialize", "notifications/initialized", "tools/list", "tools/call"})
                for request, _ in fixture.requests:
                    self.assertEqual(str(request.url), "https://search.parallel.ai/mcp")
                    self.assertEqual(request.headers["User-Agent"], web_search.USER_AGENT)
                    self.assertNotIn("Authorization", request.headers)
                self.assertEqual(fixture.tool_calls()[0]["search_queries"], ["current information"])

    def test_configured_key_and_explicit_overrides(self):
        configurations = [({"LANGSEARCH_API_KEY": "saved-key"}, "langsearch"),
                          ({"LANGSEARCH_API_KEY": "saved-key", "CAREYOU_SEARCH_PROVIDER": "parallel"}, "parallel"),
                          ({"LANGSEARCH_API_KEY": "saved-key", "CAREYOU_SEARCH_PROVIDER": "langsearch"}, "langsearch")]
        for environment, provider in configurations:
            fixture = MCPFixture()
            with fixture.install(environment):
                prompts, _ = run_chat()
            self.assertIn("https://example.org/reference", prompts[-1][-1]["content"])
            expected = web_search.LANGSEARCH_URL if provider == "langsearch" else web_search.PARALLEL_URL
            self.assertTrue(all(str(request.url) == expected for request, _ in fixture.requests))
            if provider == "langsearch":
                self.assertEqual(fixture.requests[0][0].headers["Authorization"], "Bearer saved-key")

    def test_disabled_permission_and_invalid_configuration_make_no_requests(self):
        cases = [({}, False), ({"CAREYOU_SEARCH_PROVIDER": "off", "LANGSEARCH_API_KEY": "saved-key"}, True),
                 ({"CAREYOU_SEARCH_PROVIDER": "invalid"}, True), ({"CAREYOU_SEARCH_PROVIDER": "langsearch"}, True)]
        for environment, enabled in cases:
            fixture = MCPFixture()
            with fixture.install(environment):
                prompts, _ = run_chat(enabled=enabled)
            self.assertTrue(prompts)
            self.assertEqual(fixture.requests, [])

    def test_provider_errors_do_not_fall_back_and_do_not_enter_prompt(self):
        for mode in ("quota", "http_error", "malformed"):
            fixture = MCPFixture(mode=mode)
            with fixture.install({"LANGSEARCH_API_KEY": "saved-key", "CAREYOU_SEARCH_PROVIDER": "parallel"}), patch.object(web_search, "SEARCH_TIMEOUT", 0.3):
                prompts, _ = run_chat()
            self.assertTrue(all(str(request.url) == web_search.PARALLEL_URL for request, _ in fixture.requests))
            self.assertNotIn(CONTEXT, prompts[-1][-1]["content"])
            self.assertNotIn("quota", prompts[-1][-1]["content"])
        fixture = MCPFixture(mode="http_error")
        with fixture.install({"LANGSEARCH_API_KEY": "saved-key"}):
            run_chat()
        self.assertEqual(len(fixture.requests), 1)
        self.assertEqual(str(fixture.requests[0][0].url), web_search.LANGSEARCH_URL)

    def test_timeout_cancels_transport_and_chat_continues_without_context(self):
        fixture = MCPFixture(mode="slow")
        with fixture.install(), patch.object(web_search, "SEARCH_TIMEOUT", 0.15):
            start = time.monotonic()
            prompts, _ = run_chat()
        self.assertLess(time.monotonic() - start, 2)
        self.assertTrue(fixture.cancelled.is_set())
        self.assertNotIn(CONTEXT, prompts[-1][-1]["content"])

    def test_stop_cancels_search_and_prevents_inference(self):
        fixture = MCPFixture(mode="slow")
        active = [True]
        env, _ = load_chat()
        with fixture.install(), ThreadPoolExecutor() as pool:
            result = pool.submit(run_chat, active=active)
            self.assertTrue(fixture.started.wait(2))
            self.assertIs(env["stop_generation"](active), active)
            prompts, _ = result.result(timeout=2)
        self.assertFalse(prompts)
        self.assertTrue(fixture.cancelled.is_set())
        fixture = MCPFixture()
        with fixture.install():
            prompts, _ = run_chat(active=[False])
        self.assertFalse(prompts)
        self.assertFalse(fixture.requests)

    def test_conversation_followup_retry_concurrency_and_clear_lifecycle(self):
        # Exercise the actual callable State initializer and Clear callback.
        blocks = next(node for node in APP.body if isinstance(node, ast.With) and any(
            isinstance(item.context_expr, ast.Call) and isinstance(item.context_expr.func, ast.Attribute)
            and item.context_expr.func.attr == "Blocks" for item in node.items))
        state = next(node.value for node in blocks.body if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "conversation_id" for target in node.targets))
        initializer = next(keyword.value for keyword in state.keywords if keyword.arg == "value")
        self.assertIsInstance(initializer, ast.Name)
        factory = eval(compile(ast.Expression(initializer), str(APP_PATH), "eval"),
                       {"new_conversation_id": web_search.new_conversation_id})
        first, second = factory(), factory()
        fixture = MCPFixture()
        with fixture.install():
            run_chat(query="first search", conversation_id=first)
            run_chat(query="followup search", conversation_id=first)
            with ThreadPoolExecutor() as pool:
                list(pool.map(lambda pair: run_chat(query=pair[0], conversation_id=pair[1]),
                              [("interleaved first", first), ("independent second", second)]))
            fixture.mode = "quota"
            run_chat(query="retry same conversation", conversation_id=first)
            fixture.mode = "success"
            run_chat(query="retry same conversation", conversation_id=first)
            clear_lambdas = [node for node in ast.walk(blocks) if isinstance(node, ast.Lambda)
                             and isinstance(node.body, ast.Tuple)]
            self.assertEqual(len(clear_lambdas), 1)
            clear = eval(compile(ast.Expression(clear_lambdas[0]), str(APP_PATH), "eval"),
                         {"new_conversation_id": web_search.new_conversation_id})
            history, reset_id = clear()
            self.assertIsNone(history)
            run_chat(query="reset chat", conversation_id=reset_id)
        self.assertEqual(len({first, second, reset_id}), 3)
        ids = {call["objective"]: call["session_id"] for call in fixture.tool_calls()}
        self.assertEqual(ids["first search"], first)
        self.assertEqual(ids["followup search"], first)
        self.assertEqual(ids["interleaved first"], first)
        self.assertEqual(ids["independent second"], second)
        retries = [call["session_id"] for call in fixture.tool_calls() if call["objective"] == "retry same conversation"]
        self.assertEqual(retries, [first, first])
        self.assertEqual(ids["reset chat"], reset_id)


if __name__ == "__main__":
    unittest.main()
