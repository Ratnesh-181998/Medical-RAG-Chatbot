from llm.llm_setup import load_llm

def get_answer(question):
    llm = load_llm()
    return llm(question)
