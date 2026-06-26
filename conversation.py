
import warnings
warnings.filterwarnings("ignore") 

import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate
)
from langchain_core.callbacks import BaseCallbackHandler

# A simple callback to stream text to Streamlit
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

class PersonaConversation:
    def __init__(self, persona_dict):
        self.persona = persona_dict
        
        # Load API key. First check Streamlit secrets, then check .env file
        openai_api_key = None
        try:
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        except:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key == None:
            raise ValueError("Hey, you forgot to set OPENAI_API_KEY!")

        self.openai_api_key = openai_api_key
        
        # Setup the LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=self.openai_api_key,
            streaming=True,
            max_tokens=400
        )
        
        # Setup the prompt
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.persona["system_prompt"]),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        self.reset()

    def reset(self):
        # Create a strict, zero-temperature LLM just for summarizing
        summary_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0, # Zero creativity ensures facts are perfectly retained
            api_key=self.openai_api_key
        )
        
        # A meticulous custom prompt to force the AI to keep exact details
        strict_summary_prompt = PromptTemplate(
            input_variables=["summary", "new_lines"],
            template=(
                "You are a meticulous memory assistant. Progressively summarize the lines of conversation provided, "
                "adding onto the previous summary. You MUST retain all specific facts, names, dates, constraints, "
                "and the exact intent of the user. Do not lose critical details.\n\n"
                "Current summary:\n{summary}\n\n"
                "New lines of conversation:\n{new_lines}\n\n"
                "New comprehensive summary:"
            )
        )

        # Setup memory to summarize old messages ONLY when we exceed 800 tokens
        self.memory = ConversationSummaryBufferMemory(
            llm=summary_llm,
            max_token_limit=800,
            prompt=strict_summary_prompt,
            return_messages=True,
            memory_key="history"
        )
        # Create the actual chat chain
        self.chain = ConversationChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def chat(self, user_input, st_container=None):
        start_time = time.time()
        
        # Add the streaming callback if we got a streamlit container
        my_callbacks = []
        if st_container != None:
            my_callbacks.append(StreamHandler(st_container))
            
        # Get the response from LLM
        response = self.chain.invoke({"input": user_input}, config={"callbacks": my_callbacks})
        reply = response["response"]
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        # Save latency in the last memory message so we can show it later
        # We only do this if there's at least one message
        messages_list = self.memory.chat_memory.messages
        if len(messages_list) > 0:
            last_message = messages_list[-1]
            if last_message.type == "ai":
                last_message.additional_kwargs["latency"] = latency_ms
        
        return reply, latency_ms

    def get_turn_count(self):
        # each turn has 2 messages (human and ai), so divide by 2
        return len(self.memory.chat_memory.messages) // 2
