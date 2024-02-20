from langchain import  SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain import  SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool

import os
from typing import Optional

def terminal(command: str):
    return os.popen(command).read().strip()

def python_agent(prompt):
    """
    Execute a Python REPL command by spinning up a Langchain PythonREPL agent
    """
    llm = ChatOpenAI(model="gpt-4-turbo", api_key=os.environ["OPENAI_API_KEY"])
    from langchain_experimental.agents.agent_toolkits.python.base import create_python_agent
    agent = create_python_agent(llm=llm, tool=PythonREPLTool(), agent_type=AgentType.OPENAI_FUNCTIONS)
    return {"response": agent.run({"input": prompt}), "prompt": prompt, "agent": agent.dict()}

def sql_database_agent(prompt: str):
    """
    Execute a Python REPL command by spinning up a Langchain PythonREPL agent
    """

    # Setup database
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://coredata:5cPMhnSS27sFKgCFRvXxKpc9e@postgresql-general-test.cff6npe4bzmg.us-west-2.rds.amazonaws.com/coredata",
    )

    llm = ChatOpenAI(model="gpt-4-turbo", api_key=os.environ["OPENAI_API_KEY"])

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        agent_type="openai-functions",
        db=db,
        tools=toolkit,
        llm=llm,
        verbose=True,
        handle_parsing_errors=True
    )

    return {"response": agent.run(prompt), "prompt": prompt, "agent": agent.dict()}