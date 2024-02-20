import os
import sys
import json
import requests
import functools
import tiktoken
from urllib.parse import quote
import aiohttp
import inspect
from .tools.coding import python_agent, sql_database_agent, terminal
from .tools.web import web_search, web_content, web_cache, web_scanner
from .tools.factual import fact_check
from .tools.fts import fts_ingest_document, fts_search_index, fts_document_qa, fts_extract, fts_indices
from .tools.graph import execute_cypher_query, graph_query
from .tools.plan import generate_plan, improve_plan, execute_plan
from .tools.tokens import encode_text, decode_tokens
from .tools.memory import insert_memory, lookup_similar_memories, delete_memories
from .tools.diffbot import diffbot_analyze
from .tools.tools import tool_schemas

class FunctionSchema:
    def __init__(self, name: str, description: str, parameters: dict, returns: dict):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.returns = returns

class Function:
    def __init__(self, name: str, function, schema: FunctionSchema):
        self.name = name
        self.function = function
        self.schema = schema

class Brainchain:
    def set_auth_header(self):
        if self.access_token:
            self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
        else:
            self.session.headers.pop('Authorization', None)

    # Authentication
    def login_user(self, email: str = None, password: str = None):
        url = f"{self.base_url}/v1/users/login"
        response = self.session.post(url, json={"email": email, "password": password})
        response_data = response.json()
        self.access_token = response_data.get('access_token')
        self.user_id = response_data.get('user_id')
        self.user_email = response_data.get('user_email')

        self.set_auth_header()  # Update headers with new token
        return response_data

    # Users API
    def get_users(self):
        url = f"{self.base_url}/v1/users/"
        response = self.session.get(url)
        return response.json()

    # Conversations API
    def get_all_conversations(self):
        url = f"{self.base_url}/v1/conversations/"
        response = self.session.get(url)
        return response.json()

    def get_conversation_by_id(self, conversation_id):
        url = f"{self.base_url}/v1/conversations/{conversation_id}"
        response = self.session.get(url)
        return response.json()

    # Messages API
    def get_all_messages(self):
        url = f"{self.base_url}/v1/messages/"
        response = self.session.get(url)
        return response.json()

    def get_message_by_id(self, message_id):
        url = f"{self.base_url}/v1/messages/{message_id}"
        response = self.session.get(url)
        return response.json()

    # Tools API
    def get_all_tools(self):
        url = f"{self.base_url}/v1/tools/"
        response = self.session.get(url)
        return response.json()

    # Language Models API
    def get_all_language_models(self):
        url = f"{self.base_url}/v1/language_models/list"
        response = self.session.get(url)
        return response.json()

    # Conversations API
    def create_conversation(self):
        url = f"{self.base_url}/v1/conversations/"
        data = {"user_id": self.user_id, "messages": []}
        response = self.session.post(url, json=data)
        return response.json()

    # Messages API
    def create_message(self, conversation_id, role, content):
        url = f"{self.base_url}/v1/messages/"
        data = {"conversation_id": conversation_id, "user_id": self.user_id, "role": role, "content": content}
        response = self.session.post(url, json=data)
        return response.json()

    def stream_chat_completion(self, language_model_id, conversation_id, mode='single_token', **params):
        url = f"{self.base_url}" + "/v1/language_models/chat/completions/stream"
        params = {
            "llm_id": language_model_id,
            "conversation_id": conversation_id,
            "mode": mode,
            **params
        }
        with self.session.get(url, stream=True, params=params) as response:
            response.raise_for_status()
            full_completion = []
            try:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if 'data: ' in decoded_line:
                            token = decoded_line.split('data: ')[1]
                            full_completion.append(token)
                            yield json.dumps({"status": "in_progress", "data": token})

            except KeyboardInterrupt:
                # Handle manual interruption
                pass

        yield json.dumps({"status": "done", "data": ''.join(full_completion)})


    # Language Models API
    def get_llm_by_id(self, language_model_id):
        url = f"{self.base_url}/v1/language_models/{language_model_id}/"
        response = self.session.get(url)
        return response.json()

    def get_conversation_messages(self, conversation_id):
        """
        Retrieve messages from a specific conversation.

        Args:
            conversation_id (int): The ID of the conversation.

        Returns:
            dict: A JSON response containing the conversation messages.
        """
        url = f"{self.base_url}/v1/conversations/{conversation_id}/messages"
        response = self.session.get(url)
        return response.json()

    def get_llm_by_model_name(self, language_model_name):
        url = f"{self.base_url}/v1/language_models/{language_model_name}/name"
        response = self.session.get(url)
        return response.json()

    def __init__(self, env: str = "prod", brainchain_api_key: str = os.environ["BRAINCHAIN_API_KEY"], salesintel_api_key: str = os.environ["SALESINTEL_API_KEY"], base_url: str = "https://api.brainchain.cloud"):
        if env == "prod":
            self.base_url = base_url
        elif env == "dev":
            self.base_url = "http://localhost:8000"
        elif env == "test":
            self.base_url = self.base_url.replace("api", "api-test")
        
        print("Brainchain API URL: ", self.base_url)

        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        self.user_email = None


        self.api_key = brainchain_api_key  # or self.enforce_login()
        self.salesintel_api_key = salesintel_api_key

        self.environments = ["prod", "dev"]
        self.tool_schemas = tool_schemas()
        self.tools = {
            'web_search': web_search,
            'web_content': web_content,
            'web_cache': web_cache,
            'web_scanner': web_scanner,
            'terminal': terminal,

            'python_agent': python_agent,
            'sql_database_agent': sql_database_agent,
            
            'encode_text': encode_text,
            'decode_tokens': decode_tokens,
            
            'execute_cypher_query': execute_cypher_query,
            'diffbot_analyze': diffbot_analyze,

            'generate_plan': generate_plan,
            'improve_plan': improve_plan,
            'execute_plan': execute_plan,

            'fts_ingest_document': fts_ingest_document,
            'fts_search_index': fts_search_index,
            'fts_document_qa': fts_document_qa,
            'fts_extract': fts_extract,
            'fts_indices': fts_indices,
            
            'fact_check': fact_check,
            
            'graph_query': graph_query,
            
            'insert_memory': insert_memory,
            'lookup_similar_memories': lookup_similar_memories,
            'delete_memories': delete_memories
        }

        
    


# # Example usage
# client = BrainchainAPIClient()
# client.login_user({'email': 'arthur@brainchain.ai', 'password': '<REDACTED>'})
# convo = client.create_conversation()
# client.create_message(conversation_id=convo["id"], user_id=1)


