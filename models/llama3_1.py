import torch 
from transformers import pipeline 

class llama3_1:
    device = "cuda" # the device to load the model onto

    model = None
    tokenizer = None
    pipe = None
    messages = []
    def __init__(self, system_prompt=None):
        torch.random.manual_seed(0) 
        model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="cuda",
            token="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"
        )
        if system_prompt == None:
            self.reset_chat()
        else:
            self.set_system_prompt(system_prompt)

    def chat(self, prompt):
        # print("Prompt to model: ", prompt)
        generation_args = { 
            "max_new_tokens": 500, 
            "return_full_text": False, 
            "temperature": 0.0, 
            "do_sample": False, 
        }

        self.messages.append({"role": "user", "content": prompt})
        output = self.pipe(self.messages, **generation_args) 
        response = output[0]['generated_text']
        if response != None:
            self.messages.append({"role": "assistant", "content": response})

        return response

    def reset_chat(self):
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

    def set_system_prompt(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]