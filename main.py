from dotenv import load_dotenv
load_dotenv()  # loads your API keys from .env file

from agent import run_agent

if __name__ == "__main__":
    query = input("What do you want me to research? \n> ")
    result = run_agent(query)


