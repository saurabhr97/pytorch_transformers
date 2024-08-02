import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 

class qwen2:
    device = "cuda" # the device to load the model onto

    model = None
    tokenizer = None
    pipe = None
    messages = []
    def __init__(self):
        torch.random.manual_seed(0) 
        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen2-7B-Instruct",
            torch_dtype="auto",
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

        self.pipe = pipeline( 
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer, 
        ) 
        self.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
        ]

    def chat(self, prompt):
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
        self.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
        ]