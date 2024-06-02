import asyncio
import re
from metagpt.actions.write_tutorial import WriteDirectory, WriteContent
from metagpt.logs import logger
from metagpt.roles.role import Role
from metagpt.schema import Message
from metagpt.actions import Action
from metagpt.prompts.tutorial_assistant import DIRECTORY_PROMPT, CONTENT_PROMPT
from metagpt.utils.common import OutputParser
from datetime import datetime
from pathlib import Path
import os
import time
import yaml

# 创建对话
def CreateDir():
    path = 'Interlocution'
    if os.path.exists(path) == False:
        os.makedirs(path)
    files = os.listdir(path)
    file_num = str(len(files))
    # 需提前创建一个Interlocution文件夹
    path = Path('Interlocution').joinpath(file_num + '.txt')
    with open(path, 'a') as f:
        f.write(f'创建时间{datetime.fromtimestamp(int(time.time()))}\n')
    return path

# 记录对话
def Recording(question : str, answer : str, path : str):
    with open(path, 'a') as f:
        question = '病人：{}\n'.format(question)
        answer = '医生：{}\n'.format(answer)
        f.write(question)
        f.write(answer)


    
class EmoLLM(Action):

    def __init__(self, question: str, choice: str):
        super().__init__()
        with open('config.yml', 'r', encoding='utf-8') as f:
            configs = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.question = question
        self.choice = choice
        self.PROMPT_TEMPLATE = configs['PROMPT'][choice]
        self.PROMPT = configs['Emoji_PROMPT']
        self.name = choice
        
    async def run(self, question):
        prompt = self.PROMPT_TEMPLATE.format(question=question)
        rsp = await self._aask(prompt)
        # 将回答进行专业化处理 -- 暂未完成
        # process_rsp = 
        # 将回答添加表情
        prompt = self.PROMPT.format(answer=rsp)
        process_rsp = await self._aask(prompt)
        text = EmoLLM.parse_code(process_rsp)
        return process_rsp


    @staticmethod
    def parse_code(rsp):
        pattern = r'```处理之后的回答(.*?)```'
        match = re.search(pattern, rsp, re.DOTALL)
        text = match.group(1) if match else rsp
        return text


# 设计人设
class ch_aiwei(Role):
    """
    角色类，继承自Role基类
    """
    def __init__(self, question: str, choice: str):
        """
        初始化aiwei角色
        """
        super().__init__() # 调用基类构造函数
        self.question = question
        self.choice = choice
        self.set_actions([EmoLLM(question=self.question, choice=self.choice)]) # 目前只有一个动作
        self._set_react_mode(react_mode='by_order') # 顺序执行
        
    async def _act(self) -> Message:
        """
        定义角色行动逻辑
        """
        logger.info(f"{self._setting}: 准备 {self.rc.todo}") # 记录日志
        todo = self.rc.todo # 按照排列顺序获取执行的动作

        msg = self.get_memories(k=1)[0]

        # 回答风格化
        result = await todo.run(msg.content)

        # 构造 Message 对象
        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg) # 将运行结果添加到记忆

        return msg # 返回最终的 Message
        
async def main():
    with open('config.yml', 'r', encoding='utf-8') as f:
        configs = yaml.load(f.read(), Loader=yaml.FullLoader)
    path = CreateDir()
    question = input('你好，请问您需要什么帮助吗？')
    role = ch_aiwei(question, '爹系男友')
    logger.info(question)
    while question != 'exit':
        result = await role.run(question)
        logger.info(result)
        Recording(question, result, path)
        question = input()

asyncio.run(main())