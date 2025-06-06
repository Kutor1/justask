from operator import itemgetter
from typing import List
from load_model import load_model

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
        
        session_history = self.get_all_session()

        # match the session_id with the history in databse
        if any(session_id in session for session in session_history):
            
            dbase = DataBaseHistory(session_id=session_id)

            # use DataBaseHistory def to delete the session and messages history
            dbase.clear()
            dbase.delete_session()

            print("delete completed")

        else:
            print("session_id is not exist")

    def add_session_id(self, session_id: str):
        '''
        add session_id into the database
        '''
        
        dbase = DataBaseHistory(session_id=session_id)
        dbase.add_session()

    def get_all_session(self):
        '''get session history from database'''
        all_session = DataBaseHistory.get_session()

        return all_session
    
    def show_session(self):
        """show all session_id"""

        # use format def to print the session_id history
        format_and_print_history(self.get_all_session())
        
    
    def get_messages(self, session_id: str):
        '''use session_id to get the specific messages history'''
        
        dbase = DataBaseHistory(session_id=session_id)
        return dbase.get_messages_by_session()

    def show_history_messages(self, session_id: str):
        '''print the messages history'''
        
        messages = self.get_messages(session_id=session_id)

        for message in messages:
            # confirm the message type
            sender_type = message["type"]
            if sender_type == "human":
                prefix = "Human: "
            elif sender_type == "ai":
                prefix = "AI: "
            else:
                prefix = "Unknown: "  # unknown type 
            
            # extract the message content
            content = message["data"]["content"]
            
            print(f"{prefix}{content}")

    def ask_with_history(self, session_id: str, question: str, model):
        '''ask the model with messages history'''

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
    # hm.add_session_id("1")
    hm.show_history_messages(session_id="1")
    # hm.delete("2")
    # db = DataBaseHistory
    # print(DataBaseHistory.get_session())