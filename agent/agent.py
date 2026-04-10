from langchain.agents import initialize_agent, AgentType
from tools.stock_tools import get_tools
import os
from langchain_openai import ChatOpenAI


class ChatAgent:
    def __init__(self, open_ai_key):
        chat = ChatOpenAI(model_name="gpt-4o-mini",
                          temperature=0.2, api_key=open_ai_key)
        tool_list = get_tools()
        with open("prompt/instruction.txt", "r", encoding="utf-8") as file:
            system_message = file.read()
        self.agent_chain = initialize_agent(tool_list,
                                            chat,
                                            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                            verbose=True)
        
                                            # kwargs={"system_message": system_message}) Don't use instruction

    def chat(self, question):
        return self.agent_chain.invoke(question)['output']
