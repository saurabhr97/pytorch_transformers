from models.phi3 import phi3
from models.llama3_1 import llama3_1
from InferenceTest.function_call import function_call_chat
from InferenceTest.helper import *
from RagTest.rag import rag_chat

def chat(model):
    while 1:
        prompt = get_input()
        response = model.chat(prompt)
        print_response(response)


if __name__ == '__main__':
    # llm_model = llama3_1()
    llm_model = phi3()
    # model = function_call_chat(llm_model)
    model = rag_chat(llm_model)
    chat(model)