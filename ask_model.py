from operator import itemgetter
from typing import List
from load_model import load_model
from history_manager import History_Manager

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import Optional

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

class Ask_Model():
    """ask model with api in langchain"""
    def __init__(self):
        # init history_manager
        self.history_manager = History_Manager()

        pass

    def once_ask(self, prompt: str):

        # load model
        llm = load_model()
        response = llm.invoke(prompt)

        return self.extract_ai_message(response)


    def ask_with_history(self, session_id: str, prompt: str):

        # load model
        llm = load_model()
        
        chain_with_history = self.history_manager.ask_with_history(session_id=session_id, question=prompt, model=llm)
        
        chain_with_history.invoke(
            {"ability": "math", "question": prompt},
            config={"configurable": {"session_id": session_id}}
        )

        return self.history_manager.store
    
    def extract_ai_message(self, response):

        # ai_messages = [
            # response.content
            # for msg in response.messages  # 直接遍历消息列表
            # if isinstance(msg, AIMessage)    # 类型过滤
        # ]

        ai_message = response.content

        return ai_message
