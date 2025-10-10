from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from windows_use.llm.openrouter import ChatOpenRouter
from langchain_cerebras.chat_models import ChatCerebras
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm = ChatGoogleGenerativeAI(model='gemini-flash-lite-latest', temperature=0.2)
    # llm=ChatOpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"),model="meta-llama/llama-4-maverick:free",temperature=0.2)
    # llm=ChatCerebras(api_key=os.getenv("CEREBRAS_API_KEY"), model="gpt-oss-120b", temperature=0.2)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=True)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()