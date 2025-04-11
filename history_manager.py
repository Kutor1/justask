from operator import itemgetter
from typing import List
from load_model import load_model

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

class History_Manager:
    """Manage the AI message History"""

    def __init__(self):

        # init parameter
        self.store = {}
        
        pass

    def delete(self, session_id):
        self.store[session_id] = []

    def get_by_session_id(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryHistory()
        return self.store[session_id]

    def ask_with_history(self, session_id: str, question: str, model):

        # make prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You're an assistant who's good at {ability}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        chain = prompt | model
        
        # define the chain_history
        chain_with_history = RunnableWithMessageHistory(
            chain,
            # Uses the get_by_session_id function defined in the example
            # above.
            self.get_by_session_id,
            input_messages_key="question",
            history_messages_key="history",
        )
        
        # return the chain with history
        return chain_with_history

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []