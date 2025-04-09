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

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

def ask_with_history(session_id: str, question: str):

    # make prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You're an assistant who's good at {ability}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    llm = load_model()

    chain = prompt | llm
    
    # define the chain_history
    chain_with_history = RunnableWithMessageHistory(
        chain,
        # Uses the get_by_session_id function defined in the example
        # above.
        get_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
    )

    # take session id to catch the history
    chain_with_history.invoke(
        {"ability": "math", "question": question},
        config={"configurable": {"session_id": session_id}}
    )

    print(store)

    # output AIMessage
    print(store[session_id])
    # print(store[session_id]["AI"])


# define the history manager
# def history_manage():


if __name__ == "__main__":

    while True:
        session_id = input("sessionid:")
        question = input("question:")
        ask_with_history(session_id=session_id, question=question)    
