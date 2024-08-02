from models.phi3 import phi3
from RagTest.ragInterface.json_file_interface import json_file_interface
from RagTest.dataRepository.wikipediaRepo import wikipedia_repo
import sys

class rag_chat:
    model = None
    rag_interface = None
    system_message = None
    data_repo = None

    def __init__(self, model=None):
        self.system_message = f"""
            You are an AI agent that is an expert at following instructions.
            You receive a prompt, followed by some information. Use this information to answer the prompt.
        """
        print("System Message:", self.system_message)
        if model == None:
            self.model = phi3(self.system_message)
        else:
            self.model = model
            self.model.set_system_prompt(self.system_message)
        self.rag_interface = json_file_interface()
        self.data_repo = wikipedia_repo()        
    
    def store_info(self, prompt):
        query_words = prompt.split("store:",1)[1].strip()
        data = self.data_repo.query_data(query_words)
        self.rag_interface.process_data(data)

    def generate_response(self, prompt):
        relevant_chunks = self.rag_interface.retrieve_relevant_chunks(prompt)
        print(relevant_chunks)
        message_str = "The prompt is: {}. Use the following information to answer the prompt: {}".format(prompt, "".join(relevant_chunks))
        # print("LLM message: ", message_str)
        response = self.model.chat(message_str)
        self.model.set_system_prompt(self.system_message)
        return response
    
    def chat(self, prompt):
        if prompt.lower().startswith("store:"):
            self.store_info(prompt)
            return "Added to data store"
        elif prompt.lower().startswith("norag:"):
            return self.model.chat(prompt)
        else:
            return self.generate_response(prompt)

    def get_size(self, obj, seen=None):
        """Recursively finds size of objects"""
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        # Important mark as seen *before* entering recursion to gracefully handle
        # self-referential objects
        seen.add(obj_id)
        if isinstance(obj, dict):
            size += sum([self.get_size(v, seen) for v in obj.values()])
            size += sum([self.get_size(k, seen) for k in obj.keys()])
        elif hasattr(obj, '__dict__'):
            size += self.get_size(obj.__dict__, seen)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum([self.get_size(i, seen) for i in obj])
        return size