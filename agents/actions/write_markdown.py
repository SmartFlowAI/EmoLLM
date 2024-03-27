import re

from metagpt.actions import Action

from agents.utils.common_llm_api import LLMAPI

class WriteMarkdown(Action):
    
    name: str = "WriteMarkdown"
    language: str = "Chinese"

    PROMPT_TEMPLATE: str = """
    将 {text} 严格转换为 Markdown 格式。请严格遵循以下要求：
    1. 输出必须严格符合指定语言，{language}。
    2. 目录应尽可能具体和充分，包括一级和二级目录。
    3. 不需要更改原文本，保证文本的完整性。
    4. 不用添加额外的描述。
    4. 不要有额外的空格或换行符。
    """

    async def run(self, raw_text: str):
        prompt = self.PROMPT_TEMPLATE.format(text=raw_text, language=self.language)
        
        rsp = await LLMAPI()._aask(prompt)

        markdown_text = WriteMarkdown.parse_markdown(rsp)

        return markdown_text
    
    @staticmethod
    def parse_markdown(rsp):
        rsp = rsp.replace("```markdown", "").replace("```", "")
        markdown_text = "```markdown\n" + rsp + "\n```"
        return markdown_text

