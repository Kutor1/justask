from operator import itemgetter
from typing import List
from load_model import load_model
# from database_history import DatabaseHistory
from inmemoryhistory import InMemoryHistory
from database_history import DataBaseHistory
from format_output import format_and_print_history

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

    # def __init__(self):

        # init store
        # self.history_db = DataBaseHistory()

    def delete(self, session_id: str):
        """delete session_id and all messages with session_id"""
        
        dbase = DataBaseHistory(session_id=session_id)
        dbase.clear()
        dbase.delete_session()

    def add_session_id(self, session_id: str):

        dbase = DataBaseHistory(session_id=session_id)
        dbase.add_session()

    def get_all_session(self):
        all_session = DataBaseHistory.get_session()

        return all_session
    
    def show_session(self):
        """show all session_id"""

        # self.get_all_session()
        format_and_print_history(self.get_all_session())
        
        return
    
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
            get_session_history=lambda session_id: DataBaseHistory(session_id),
            input_messages_key="question",
            history_messages_key="history",
        )   
        
        # return the chain with history
        return chain_with_history
    
if __name__=="__main__":

    hm = History_Manager()
    # db = DataBaseHistory
    # print(DataBaseHistory.get_session())