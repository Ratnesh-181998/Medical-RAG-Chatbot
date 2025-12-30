from langchain_community.vectorstores import FAISS
import os
import streamlit as st
from app.components.embeddings import get_embedding_model
from app.components.pdf_loader import load_pdf_files, create_text_chunks

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)

def regenerate_vector_store():
    """Helper function to rebuild vector store from scratch on failure"""
    try:
        logger.info("⚠️ Attempting to regenerate vector store from source PDFs...")
        st.toast("⚠️ Rebuilding Vector Store... This may take a minute.", icon="⏳")
        
        # 1. Load Documents
        documents = load_pdf_files()
        if not documents:
            logger.error("No documents found to regenerate vector store.")
            return None
            
        # 2. Chunk Text
        text_chunks = create_text_chunks(documents)
        if not text_chunks:
            logger.error("No text chunks created.")
            return None
            
        # 3. Save & Return
        return save_vector_store(text_chunks)
        
    except Exception as e:
        logger.error(f"Failed to regenerate vector store: {e}")
        return None

def load_vector_store():
    try:
        embedding_model = get_embedding_model()

        # Check if vector store exists
        if os.path.exists(DB_FAISS_PATH):
            logger.info("Loading existing vectorstore...")
            try:
                # Attempt to load
                return FAISS.load_local(
                    DB_FAISS_PATH,
                    embedding_model,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                # If loading fails (e.g. Pydantic/Pickle mismatch), regenerate!
                logger.error(f"❌ Corrupt/Incompatible Vector Store found: {e}")
                logger.info("Initiating automatic repair/regeneration...")
                return regenerate_vector_store()
        else:
            logger.warning("No vector store found. Creating one now...")
            return regenerate_vector_store()

    except Exception as e:
        # Global catch-all
        error_message = CustomException("CRITICAL: Failed to load or regenerate vectorstore", e)
        logger.error(str(error_message))
        return None

# Creating new vectorstore function
def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException("No chunks were found..")
        
        logger.info("Generating your new vectorstore")

        embedding_model = get_embedding_model()

        db = FAISS.from_documents(text_chunks,embedding_model)

        logger.info("Saving vectorstore...")

        db.save_local(DB_FAISS_PATH)

        logger.info("Vectorstore saved successfully!")

        return db
    
    except Exception as e:
        error_message = CustomException("Failed to create new vectorstore", e)
        logger.error(str(error_message))
        return None
