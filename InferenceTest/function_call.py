from models.phi3 import phi3
import json
import re
import requests
import sys

class function_call_chat:
    model = None
    functions = []

    def __init__(self, model=None):
        self.functions = [
            self.convert_to_openai_function(self.note_conversation),
            self.convert_to_openai_function(self.calculate)
        ]

        system_message = f"""
            You are an AI agent that is an expert at following instructions.
            You have access to the following functions. After each function call, describe your action in plain text:
            {json.dumps(self.functions, indent=2)}

            If the user's input contains "note conversation" or similar, followed by some content, generate a function call in the following format:
            <functioncall>{{"name": "note_conversation", "arguments": {{"note_str": "note_content"}}}}</functioncall>
            Replace "note_content" with content actually provided by the user, excluding the "note conversation" phrase, and ensure the entire function call is on a single line.

            Example: user: note conversation user conversation content

            If the user's input contains "calculate" or similar, followed by 2 numbers and an arthmetic operator, generate a function call in the following format:
            <functioncall>{{"name": "calculate", "arguments": {{"number_a": "first_number", "number_b": "second_number", "operator": "required_operator"}}}}</functioncall>
            Replace "number_a" with the first number provided by the user, replace "number_b" with the second number provided by the user, and replace "operator" with the operator provided by the user
            Ensure the entire function call is on a single line.            

            Example: user: calculate 5 + 3

            If the user's input contains "get info" or similar, followed by a topic or word, generate a function call in the following format:
            <functioncall>{{"name": "query_wiki", "arguments": {{"wiki_query_str": "query_topic"}}}}</functioncall>
            Replace "query_topic" with the topic provided by the user
            Ensure the entire function call is on a single line.            

            Example: user: get info blue
        """
        print("System Message:", system_message)
        if model == None:
            self.model = phi3(system_message)
        else:
            self.model = model
            model.set_system_prompt(system_message)
        

    def convert_to_openai_function(self, func):
        return {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "note_str": {"type": "string", "description": "Content to be written to notes.txt file"},
                    "number_a": {"type": "float", "description": "First number for calculation"},
                    "number_b": {"type": "float", "description": "Second number for calculation"},
                    "operator": {"type": "string", "description": "Operator to be used for calculation"},
                    "wiki_query_str": {"type": "string", "description": "Topic to provide information for"}
                },
                "required": []
            }
        }

    def note_conversation(self, note_str):
        '''This function writes the passed parameter note_str into a file'''
        with open("InferenceTest\\resources\\notes.txt", '+a') as f:
            f.write(note_str + '\n')
        print("Noted string: ", note_str)

    def calculate(self, number_a, number_b, operator):
        '''This function performs the provided operator on number_a and number_b. The operator values are:
                "+" for addition; "-" for subtraction; "*" for multiplication; "/" for division; "^" for exponent'''
        number_a = float(number_a)
        number_b = float(number_b)
        if operator == '+':
            return number_a + number_b
        elif operator == '-':
            return number_a - number_b
        elif operator == '*':
            return number_a * number_b
        elif operator == '/':
            return number_a/number_b
        elif operator == '^':
            return number_a**number_b
        
    def query_wiki(self, wiki_query_str):
        '''This function provides information on the topic of the parameter passed, "wiki_query_str"
        '''
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles={}&prop=extracts&explaintext=true".format(wiki_query_str)
        print(url)
        r = requests.get(url)
        content = json.loads(r.text)
        for page in content.get("query").get("pages"):
            content = content.get("query").get("pages").get(page).get("extract")[:2000]
            break
        return "Provide a summary without using a function of the following text: " + content

    def parse_function_call(self, response):
        match = re.search(r'<functioncall>(.*)</functioncall>', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                return None
        return None
    
    def chat(self, prompt):
        response = self.model.chat(prompt)
        print("Model response: ", response)
        print("Current Context length: ", self.get_size(self.model.messages))
        function_call = self.parse_function_call(response)
        if function_call:
            function_name = function_call["name"]
            function_arguments = function_call["arguments"]
            if function_name == "note_conversation":
                self.note_conversation(**function_arguments)
                return "Successfully written note to file"
            elif function_name == "calculate":
                answer = self.calculate(**function_arguments)
                return "The answer is " + str(answer)
            elif function_name == "query_wiki":
                new_query = self.query_wiki(**function_arguments)
                return self.model.chat(new_query)
        return response


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