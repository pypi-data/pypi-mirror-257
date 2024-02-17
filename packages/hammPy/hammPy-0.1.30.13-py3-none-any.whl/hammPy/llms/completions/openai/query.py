
#==============================================================================#
#== Hammad Saeed ==============================================================#
#==============================================================================#
#== www.hammad.fun ============================================================#
#== hammad@supportvectors.com =================================================#
#==============================================================================#

##== HamPy ==######################################== Hammad's Python Tools ==## 
##== @/llms/completions/openai/query ==#########################################
##== Queries OpenAI Chat Completions ==#########################################

#==============================================================================#

from ....llms.lib.models import QueryContentModel, QueryListModel, QueryNestedListModel
from hammPy.pydantic import ContentModel_STR, ContentModel_INT, ListModel_STR, ListModel_INT, DoubleListModel_STR, DoubleListModel_INT, TripleListModel_STR, TripleListModel_INT, NestedListModel_STR, NestedListModel_INT, NestedListModel_INTSTR

import os
import json
import getpass
import instructor
from openai import OpenAI

#==============================================================================#

class OpenAIKey:
    def __init__(self):
        print("Testing OpenAI API Key.")

    def key(self):
        if os.getenv("OPENAI_API_KEY") == None:
            print("No OpenAI API Key found in environment variables.")
            self.key = getpass.getpass("OpenAI API Key: ")
            os.environ["OPENAI_API_KEY"] = self.key
            self.apikey = os.getenv("OPENAI_API_KEY")
            return self.apikey
        else:
            os.environ["OPENAI_API_KEY"] = self.key
            self.key = os.getenv("OPENAI_API_KEY")
            return self.apikey          
            
#==============================================================================#

class OpenAIQuery:
    def __init__(self, key: str = None):
        self.key = key
        self.ai = instructor.patch(OpenAI(api_key=self.key))


    def ask(self, model: str = None, system: str = None, query: str = None):
        """"
        Sends a query to OpenAI Chat Completions.
        
        
        Args:
        -   model (str): Model to be used for the query.
        -   pymodel (str): Pydantic Model to be used for the query.
        -   system (str): System message to be used for the query.
        -   query (str): Query to be sent to OpenAI.
        """
        if model == "3":
            self.model = "gpt-3.5-turbo"
        if model == "4":
            self.model = "gpt-4-preview-1106"
        self.pymodel = QueryContentModel
        self.system = system
        self.query = query
        if self.model == None:
            print("Model is required for invoke()")
            return
        elif self.pymodel == None:
            print("Pydantic Model is required for invoke()")
            return
        elif self.system == None:
            print("System message is required for invoke()")
            return
        elif self.query == None:
            print("Query is required for invoke()")
            return
        else:
            completion = self.ai.chat.completions.create(
                model=self.model,
                response_model=self.pymodel,
                messages=[{"role": "system", "content": self.system}, {"role": "user", "content": self.query}]
            )
            assert isinstance(completion, QueryContentModel)
            print(completion.model_dump_json(indent=2))
            completion = completion.model_dump_json(indent=2)
            completion = json.loads(completion)
            completion = completion["content"]
            return completion
        
    def list(self, model: str = None, system: str = None, query: str = None):
        """"
        Sends a query to OpenAI Chat Completions.
        Returns a list of completions.
        
        
        Args:
        -   model (str): Model to be used for the query.
        -   pymodel (str): Pydantic Model to be used for the query.
        -   system (str): System message to be used for the query.
        -   query (str): Query to be sent to OpenAI.
        """
        if model == "3":
            self.model = "gpt-3.5-turbo"
        if model == "4":
            self.model = "gpt-4-preview-1106"
        self.pymodel = QueryListModel
        self.system = system
        self.query = query
        if self.model == None:
            print("Model is required for invoke()")
            return
        elif self.pymodel == None:
            print("Pydantic Model is required for invoke()")
            return
        elif self.system == None:
            print("System message is required for invoke()")
            return
        elif self.query == None:
            print("Query is required for invoke()")
            return
        elif self.query == tuple:
            for i in self.query:
                completion = self.ai.chat.completions.create(
                    model=self.model,
                    response_model=self.pymodel,
                    messages=[{"role": "system", "content": self.system}, {"role": "user", "content": i}]
                )
                assert isinstance(completion, QueryListModel)
                return completion
        else:
            completion = self.ai.chat.completions.create(
                model=self.model,
                response_model=self.pymodel,
                messages=[{"role": "system", "content": self.system}, {"role": "user", "content": self.query}]
            )
            assert isinstance(completion, QueryListModel)
            completion = completion.model_dump_json(indent=2)
            completions = json.loads(completion)
            completions = completions["items"]
            return completions
        
    def nestedlist(self, model: str = None, system: str = None, query: str = None):
        """
        Sends a query to OpenAI Chat Completions.
        

        Args:
        -   model (str): Model to be used for the query.
        -   pymodel (str): Pydantic Model to be used for the query.
        -   system (str): System message to be used for the query.
        -   query (str): Query to be sent to OpenAI.
        """
        if model == "3":
            self.model = "gpt-3.5-turbo"
        if model == "4":
            self.model = "gpt-4-preview-1106"
        self.pymodel = QueryNestedListModel
        self.system = system
        self.query = query
        if self.model == None:
            print("Model is required for invoke()")
            return
        elif self.pymodel == None:
            print("Pydantic Model is required for invoke()")
            return
        elif self.system == None:
            print("System message is required for invoke()")
            return
        elif self.query == None:
            print("Query is required for invoke()")
            return
        else:
            completions = self.ai.chat.completions.create(
                model=self.model,
                response_model=self.pymodel,
                messages=[{"role": "system", "content": self.system}, {"role": "user", "content": self.query}]
            )
            assert isinstance(completions, QueryNestedListModel)
            completions = completions.model_dump_json(indent=2)
            completions = json.loads(completions)
            completions = completions["nested_items"]
            return completions
        
    def instruct(self, model: str = None, system: str = None, query: str = None, pymodel = ['content_str', 'content_int', 'list_str', 'list_int', 'double_list_str', 'double_list_int', 'triple_list_str', 'triple_list_int', 'nested_list_str', 'nested_list_int', 'nested_list_intstr']):
        """
        Creates an OpenAI query, with a user provided Pydantic model.

        Args:
        -   model (str): Model to be used for the query.
        -   pymodel (class) - Pydantic Model to be used for the query.
        -   system (str): System message to be used for the query.
        -   query (str): Query to be sent to OpenAI.
        """
        if pymodel == "content_str":
            self.pymodel = ContentModel_STR
        elif pymodel == "content_int":
            self.pymodel = ContentModel_INT
        elif pymodel == "list_str":
            self.pymodel = ListModel_STR
        elif pymodel == "list_int":
            self.pymodel = ListModel_INT
        elif pymodel == "double_list_str":
            self.pymodel = DoubleListModel_STR
        elif pymodel == "double_list_int":
            self.pymodel = DoubleListModel_INT
        elif pymodel == "triple_list_str":
            self.pymodel = TripleListModel_STR
        elif pymodel == "triple_list_int":
            self.pymodel = TripleListModel_INT
        elif pymodel == "nested_list_str":
            self.pymodel = NestedListModel_STR
        elif pymodel == "nested_list_int":
            self.pymodel = NestedListModel_INT
        elif pymodel == "nested_list_intstr":
            self.pymodel = NestedListModel_INTSTR
        if model == "3":
            self.model = "gpt-3.5-turbo"
        if model == "4":
            self.model = "gpt-4-preview-1106"
        self.system = system
        self.query = query
        if self.model == None:
            print("Model is required for invoke()")
            return
        elif self.pymodel == None:
            print("Pydantic Model is required for invoke()")
            return
        elif self.system == None:
            print("System message is required for invoke()")
            return
        elif self.query == None:
            print("Query is required for invoke()")
            return
        else:
            completion = self.ai.chat.completions.create(
                model=self.model,
                response_model=self.pymodel,
                messages=[{"role": "system", "content": self.system}, {"role": "user", "content": self.query}]
            )
            return completion

    def chat(self, query: str = None):
        """"
        Creates a simple, base query to OpenAI Chat Completions.
        
        
        Args:
        -   query (str): Query to be sent to OpenAI.
        """
        self.query = query
        if self.query == None:
            print("Query is required for invoke()")
            return
        else:
            completion = self.ai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": self.query}]
            )
            return completion