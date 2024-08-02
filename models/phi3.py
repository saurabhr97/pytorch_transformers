import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 

class phi3:
    device = "cuda" # the device to load the model onto

    model = None
    tokenizer = None
    pipe = None
    messages = []
    def __init__(self, system_prompt=None):
        torch.random.manual_seed(0) 
        self.model = AutoModelForCausalLM.from_pretrained( 
            "microsoft/Phi-3-mini-128k-instruct",  
            device_map=self.device,  
            torch_dtype="auto",  
            trust_remote_code=True,  
        ) 

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")

        self.pipe = pipeline( 
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer, 
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
