from langchain.llms import HuggingFaceHub
import os

def load_llm():
    return HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.1",
        huggingfacehub_api_token=os.getenv("HF_TOKEN")
    )
