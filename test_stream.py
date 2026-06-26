import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
chain = ConversationChain(llm=llm)

for chunk in chain.stream({"input": "Count from 1 to 5"}):
    print("CHUNK:", chunk)

# test_stream.py: This was a similar scratchpad script used earlier in the project.
# It was built specifically to test out LangChain's "Streaming" feature (the cool
# typewriter effect where the AI types its response out letter-by-letter) before we 
# actually integrated that code into the final app.