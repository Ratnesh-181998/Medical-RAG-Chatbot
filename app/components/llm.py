from langchain_huggingface import HuggingFaceEndpoint
from app.config.config import HF_TOKEN,HUGGINGFACE_REPO_ID

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

from langchain_openai import ChatOpenAI

def load_llm(huggingface_repo_id: str = HUGGINGFACE_REPO_ID , hf_token:str = HF_TOKEN):
    try:
        logger.info(f"Loading LLM: {huggingface_repo_id}")

        llm = ChatOpenAI(
            model=huggingface_repo_id,
            openai_api_key=hf_token,
            openai_api_base="https://router.huggingface.co/v1",
            temperature=0.3,
            max_tokens=256
        )

        logger.info("LLM loaded sucesfully...")

        return llm
    
    except Exception as e:
        error_message = CustomException("Failed to load a llm" , e)
        logger.error(str(error_message))