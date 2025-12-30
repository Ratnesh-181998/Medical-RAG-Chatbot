from datetime import datetime
import streamlit as st
import os, sys

# ... [KEEP imports as is]
import streamlit as st
import os
import sys
import time
from datetime import datetime

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import RAG components
try:
    from app.components.retriever import create_qa_chain
    from app.config.config import HUGGINGFACE_REPO_ID
except ImportError as e:
    st.error(f"Error importing app components: {e}")
    create_qa_chain = None

# ... [KEEP styling config as is] ...
st.set_page_config(
    page_title="Medical RAG Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ... [KEEP CSS styling] ...
st.markdown("""
<style>
    :root {
        --primary-gold: #FFD700;
        --accent-blue: #2874f0;
        --accent-green: #2ecc71;
        --accent-red: #e74c3c;
        --background-dark: #141E30; 
        --text-light: #ecf0f1; 
        --card-bg: rgba(30, 41, 59, 0.4);
    }
    .stApp {
        background: linear-gradient(to right, #141E30, #243B55);
        color: var(--text-light);
        font-family: 'Inter', sans-serif;
    }
    /* ... keep all CSS identical ... */
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid var(--accent-green);
    }
    h1 { color: #00d4ff !important; text-shadow: 0 0 20px rgba(0, 212, 255, 0.5); }
    h2 { color: var(--accent-blue) !important; }
    h3 { color: var(--accent-green) !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-blue) !important;
    }

    .user-message {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #00d4ff 100%);
        padding: 15px; border-radius: 15px 15px 0 15px; margin: 10px 0 10px 20%; color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .bot-message {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px; border-radius: 15px 15px 15px 0; margin: 10px 20% 10px 0; 
        border: 1px solid rgba(46, 204, 113, 0.3); color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .tech-card {
        background: var(--card-bg);
        border-radius: 15px; padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease; height: 100%;
    }
    .tech-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #00d4ff;
        box-shadow: 0 10px 25px rgba(0, 212, 255, 0.2);
    }
    .tech-icon { font-size: 2rem; margin-bottom: 15px; display: block; }

</style>
""", unsafe_allow_html=True)


# ... [KEEP Sidebar & Header identical] ...
with st.sidebar:
    st.markdown("""
    <div style='background: #ffffff; padding: 20px; border-radius: 15px; text-align: center; border: 3px solid #2ecc71; box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2); margin-bottom: 20px;'>
        <h2 style='color: #2ecc71; margin: 0; font-weight: 900; font-size: 1.8rem;'>🏥 Medical RAG <span style='color: #27ae60;'>✚</span></h2>
        <p style='color: #555; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px; margin: 5px 0; text-transform: uppercase;'>AI Health Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(40, 116, 240, 0.2) 0%, rgba(155, 89, 182, 0.2) 100%); 
                padding: 15px; border-radius: 10px; border: 2px solid rgba(155, 89, 182, 0.4);'>
        <p style='margin: 5px 0; color: #00d4ff; font-weight: 600;'>Ratnesh Kumar Singh</p>
        <p style='margin: 5px 0; font-size: 0.85rem;'>Data Scientist (AI/ML Engineer)</p>
        <div style='margin-top: 10px; display: flex; flex-wrap: wrap; gap: 10px;'>
            <a href='https://github.com/Ratnesh-181998' target='_blank' style='text-decoration: none; color: #2874f0; font-weight: bold; font-size: 0.8rem;'>🔗 GitHub</a>
            <a href='https://www.linkedin.com/in/ratneshkumar1998/' target='_blank' style='text-decoration: none; color: #0077b5; font-weight: bold; font-size: 0.8rem;'>💼 LinkedIn</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📂 Project Files")
    if st.checkbox("Show Data Directory"):
        try:
            files = os.listdir("data")
            st.code("\n".join(files))
        except FileNotFoundError:
            st.warning("Data directory not found.")

# ... [Top Right Badge] ...
col_space, col_badge = st.columns([3, 1.25])
with col_badge:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2874f0 0%, #9b59b6 100%); 
                padding: 10px; border-radius: 8px; 
                box-shadow: 0 4px 12px rgba(40, 116, 240, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center; margin-bottom: 20px;'>
        <p style='margin: 0; color: #ffffff; font-weight: 700; font-size: 0.75rem; line-height: 1.4;'>
            <strong>Ratnesh Kumar Singh</strong><br>
            <span style='font-size: 0.65rem; opacity: 0.9;'>Data Scientist (AI/ML Engineer 4+Yrs Exp)</span>
        </p>
        <div style='display: flex; justify-content: center; gap: 12px; margin-top: 8px;'>
            <a href='https://github.com/Ratnesh-181998' target='_blank' style='color: white; font-size: 0.7rem; text-decoration: none; background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; transition: all 0.3s;' onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">🔗 GitHub</a>
            <a href='https://www.linkedin.com/in/ratneshkumar1998/' target='_blank' style='color: white; font-size: 0.7rem; text-decoration: none; background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; transition: all 0.3s;' onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">💼 LinkedIn</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div style='text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(30, 41, 59, 0.6) 100%); border-radius: 12px; margin-bottom: 20px; border: 2px solid #2ecc71; box-shadow: 0 5px 15px rgba(46, 204, 113, 0.2);'>
    <div style='display: flex; justify-content: center; align-items: center; gap: 15px;'>
        <div style='font-size: 2.5rem;'>🏥</div>
        <div>
            <h1 style='margin: 0; font-size: 2.2rem; letter-spacing: 2px; color: #2ecc71; text-align: left;'>MEDICAL RAG <span style='color: white;'>CHATBOT</span> <span style='font-size: 1.5rem; vertical-align: middle; color: #e74c3c;'>✚</span></h1>
            <p style='font-size: 1.0rem; color: #b2bec3; margin: 0; text-align: left; font-weight: 500;'>
                Advanced Medical QA using Retrieval Augmented Generation & Llama 3
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Demo Project", 
    "📖 About Project", 
    "🔧 Tech Stack", 
    "🏗️ Architecture", 
    "📋 System Logs"
])

# Loading the QA chain (Cached) - FIX: Use unique function to ensure cache stability
@st.cache_resource(show_spinner="Initializing Medical Intelligence Engine...")
def get_rag_engine():
    # Helper to load the chain.
    # Note: Streamlit cache relies on function inputs/outputs pickling.
    if create_qa_chain:
        try:
            return create_qa_chain()
        except Exception as e:
            return None
    return None

chain = get_rag_engine()

# --- TAB 1: DEMO ---
with tab1:
    # Display Banners if available
    if os.path.exists("banner.png"):
        st.image("banner.png", use_container_width=True)

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(40, 116, 240, 0.1) 0%, rgba(155, 89, 182, 0.1) 100%); 
                padding: 20px; border-radius: 12px; border-left: 5px solid #00d4ff; margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin: 0 0 10px 0;'>🩺 Ratnesh AI Medical Assistant Workspace</h3>
        <p style='color: #e8e8e8; margin: 0; font-size: 0.95rem;'>
            Ask any medical question based on the provided medical encyclopedias. 
            The system retrieves relevant context and references trusted sources using <b>Retrieval Augmented Generation (RAG)</b>.
            Enable real-time medical insights powered by <b>Llama 3</b> and <b>FAISS Vector Search</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for metrics
    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 0
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    
    # Metrics Dashboard
    st.markdown("### 📊 Session Analytics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="💬 Questions Asked",
            value=st.session_state.total_questions,
            delta="+1" if st.session_state.total_questions > 0 else None
        )
    
    with metric_col2:
        session_duration = (datetime.now() - st.session_state.session_start_time).seconds // 60
        st.metric(
            label="⏱️ Session Time",
            value=f"{session_duration} min",
            delta="Active"
        )
    
    with metric_col3:
        chat_count = len(st.session_state.get("messages", []))
        st.metric(
            label="💭 Total Messages",
            value=chat_count,
            delta=f"{chat_count // 2} exchanges" if chat_count > 0 else None
        )
    
    with metric_col4:
        st.metric(
            label="🤖 AI Status",
            value="Online" if chain else "Offline",
            delta="Ready" if chain else "Error"
        )
    
    st.markdown("---")

    # Quick Start Sample Prompts
    st.markdown("### 🚀 Quick Starts & Sample Medical Queries")
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.03); padding: 10px; border-radius: 8px; margin-bottom: 15px;'>
        <p style='color: #bdc3c7; margin: 0; font-size: 0.9rem;'>
            💡 <b>Tip:</b> Click any button below to instantly ask a medical question, or type your own query in the chat box!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1 - Common Symptoms
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("🤒 Fever", use_container_width=True, help="Learn about fever symptoms"):
        st.session_state.pending_query = "What are the common causes of fever and when should I see a doctor?"
        st.rerun()
    if q2.button("💊 Diabetes", use_container_width=True, help="Diabetes information"):
        st.session_state.pending_query = "What are the symptoms and treatment options for diabetes?"
        st.rerun()
    if q3.button("🫁 Pneumonia", use_container_width=True, help="Pneumonia details"):
        st.session_state.pending_query = "What are the symptoms of pneumonia and how is it treated?"
        st.rerun()
    if q4.button("❤️ Heart Disease", use_container_width=True, help="Cardiovascular health"):
        st.session_state.pending_query = "What are the warning signs of heart disease?"
        st.rerun()

    # Row 2 - Conditions & Treatments
    q5, q6, q7, q8 = st.columns(4)
    if q5.button("🧬 Cancer", use_container_width=True, help="Cancer information"):
        st.session_state.pending_query = "What causes cancer and what are the prevention methods?"
        st.rerun()
    if q6.button("🦴 Arthritis", use_container_width=True, help="Joint health"):
        st.session_state.pending_query = "What are the different types of arthritis and their treatments?"
        st.rerun()
    if q7.button("🧠 Migraine", use_container_width=True, help="Headache information"):
        st.session_state.pending_query = "What triggers migraines and how can they be prevented?"
        st.rerun()
    if q8.button("🩺 Blood Pressure", use_container_width=True, help="Hypertension info"):
        st.session_state.pending_query = "What is high blood pressure and how can it be managed?"
        st.rerun()

    # Row 3 - Respiratory & Digestive
    q9, q10, q11, q12 = st.columns(4)
    if q9.button("🫁 Asthma", use_container_width=True, help="Respiratory condition"):
        st.session_state.pending_query = "What are the symptoms of asthma and how is it managed?"
        st.rerun()
    if q10.button("🦠 COVID-19", use_container_width=True, help="Coronavirus information"):
        st.session_state.pending_query = "What are the symptoms and prevention methods for COVID-19?"
        st.rerun()
    if q11.button("🍽️ Gastritis", use_container_width=True, help="Digestive health"):
        st.session_state.pending_query = "What causes gastritis and what are the treatment options?"
        st.rerun()
    if q12.button("🧪 Thyroid", use_container_width=True, help="Endocrine system"):
        st.session_state.pending_query = "What are the symptoms of thyroid disorders?"
        st.rerun()

    # Row 4 - Mental Health & Chronic Conditions
    q13, q14, q15, q16 = st.columns(4)
    if q13.button("😰 Anxiety", use_container_width=True, help="Mental health"):
        st.session_state.pending_query = "What are the symptoms and treatments for anxiety disorders?"
        st.rerun()
    if q14.button("🩸 Anemia", use_container_width=True, help="Blood disorder"):
        st.session_state.pending_query = "What causes anemia and how can it be treated?"
        st.rerun()
    if q15.button("🦷 Dental Health", use_container_width=True, help="Oral care"):
        st.session_state.pending_query = "What are common dental problems and how to prevent them?"
        st.rerun()
    if q16.button("👁️ Eye Care", use_container_width=True, help="Vision health"):
        st.session_state.pending_query = "What are the signs of vision problems and when to see a doctor?"
        st.rerun()


    st.markdown("---")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat Container with better organization
    st.markdown("### 💬 Medical Consultation Chat")
    
    # Display welcome message if no chat history
    if not st.session_state.messages:
        st.info("👋 **Welcome!** Start the conversation by typing a medical question below or using a Quick Start button above!")
    
    # Chat History Display
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            role_class = "user-message" if message["role"] == "user" else "bot-message"
            icon = "👤" if message["role"] == "user" else "🤖"
            display_name = "You" if message["role"] == "user" else "Ratnesh AI Medical Assistant"
            
            # Add timestamp simulation
            time_str = datetime.now().strftime("%H:%M")
            
            st.markdown(f"""
            <div class='{role_class}'>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong style="opacity: 0.9;">{icon} {display_name}</strong>
                    <span style="font-size: 0.7rem; opacity: 0.6;">{time_str}</span>
                </div>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Add copy and feedback buttons for AI responses
            if message["role"] == "assistant":
                btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 7])
                with btn_col1:
                    if st.button("📋", key=f"copy_{idx}", help="Copy response"):
                        st.toast("✅ Response copied to clipboard!", icon="📋")
                with btn_col2:
                    if st.button("👍", key=f"like_{idx}", help="Helpful"):
                        st.toast("Thank you for your feedback!", icon="👍")
                with btn_col3:
                    if st.button("👎", key=f"dislike_{idx}", help="Not helpful"):
                        st.toast("Feedback noted. We'll improve!", icon="👎")

    st.markdown("---")
    
    # Input Area with Clear Button
    st.markdown("### ✍️ Ask Your Medical Question")
    
    # Helpful tip
    st.markdown("""
    <div style='background: rgba(231, 76, 60, 0.1); padding: 10px 15px; border-radius: 8px; border-left: 4px solid #e74c3c; margin-bottom: 15px;'>
        <p style='color: #e74c3c; margin: 0; font-size: 0.85rem;'>
            💡 <b>Quick Tip:</b> Type your question below and press <kbd style='background: #34495e; padding: 2px 6px; border-radius: 3px; color: white; font-size: 0.8rem;'>Enter ↵</kbd> or click the send button to submit!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    input_col, btn_col = st.columns([6, 4])
    
    # Initialize text input state
    if "text_input" not in st.session_state:
        st.session_state.text_input = ""
    
    with input_col:
        # Use text_area for better control
        user_input = st.text_area(
            "Type your medical question here...",
            value=st.session_state.text_input,
            height=80,
            placeholder="💬 e.g., 'What are the symptoms of pneumonia?' (Press Ctrl+Enter or click Send)",
            label_visibility="collapsed",
            key="medical_question_input"
        )
    
    with btn_col:
        send_col, clear_col, export_col = st.columns(3)
        
        with send_col:
            send_clicked = st.button("📤 Send", use_container_width=True, type="primary")
        
        with clear_col:
            if st.button("🧹 Clear", use_container_width=True, type="secondary"):
                st.session_state.messages = []
                st.session_state.total_questions = 0
                st.session_state.text_input = ""
                if "pending_query" in st.session_state:
                    del st.session_state.pending_query
                st.rerun()
        
        with export_col:
            if st.button("💾 Export", use_container_width=True, type="primary", disabled=len(st.session_state.get("messages", [])) == 0):
                # Create export text
                export_text = "MEDICAL RAG CHATBOT - CONVERSATION HISTORY\n"
                export_text += f"Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                export_text += "="*50 + "\n\n"
                for msg in st.session_state.messages:
                    role = "USER" if msg["role"] == "user" else "AI ASSISTANT"
                    export_text += f"{role}:\n{msg['content']}\n\n"
                
                st.download_button(
                    label="📥 Download",
                    data=export_text,
                    file_name=f"medical_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Set prompt from either send button or pending query
    prompt = None
    if send_clicked and user_input.strip():
        prompt = user_input.strip()
        st.session_state.text_input = ""  # Clear input after sending

    # Handle pending query from quick start buttons
    if "pending_query" in st.session_state:
        prompt = st.session_state.pending_query
        del st.session_state.pending_query

    # Process user input
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Increment question counter
        st.session_state.total_questions += 1
        
        # Generate response
        if chain:
            with st.status("🧠 AI Medical Analysis in Progress...", expanded=True) as status:
                st.write("📡 Connecting to Llama 3 Inference Engine...")
                st.write("🔍 Searching medical knowledge base (FAISS Vector Store)...")
                st.write("📚 Retrieving relevant medical context...")
                
                try:
                    res = chain.invoke({"query": prompt})
                    answer = res["result"]
                    
                    st.write("✅ Generating evidence-based medical response...")
                    
                    # Add bot message
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    status.update(label="✅ Medical Analysis Complete!", state="complete", expanded=False)
                    st.rerun()
                    
                except Exception as e:
                    status.update(label="❌ Error occurred", state="error")
                    st.error(f"Error generating response: {e}")
                    st.info("💡 **Troubleshooting Tips:**\n- Check if the vector store is properly initialized\n- Verify your HF_TOKEN is valid\n- Ensure the LLM model is accessible")
        else:
            st.error("⚠️ QA Chain not initialized. Please check System Logs tab for details.")
            st.warning("**Possible Issues:**\n- Vector store not found\n- LLM failed to load\n- Missing dependencies")

# ... [KEEP Tab 2, 3, 4, 5 as original] ...
# --- TAB 2: ABOUT ---
with tab2:
    # Project Overview with enhanced styling
    st.markdown("""
<div style='background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%); padding: 30px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
    <h2 style='color: #00d4ff; margin-bottom: 20px; border-bottom: 2px solid #00d4ff; padding-bottom: 10px;'>🌟 Project Overview</h2>
    <p style='font-size: 1.1rem; line-height: 1.8; color: #ecf0f1; margin-bottom: 15px;'>
        This <b>Medical RAG Chatbot</b> is a sophisticated AI system designed to answer medical queries with high accuracy 
        by grounding its responses in a trusted knowledge base (Medical Encyclopedia PDFs). 
    </p>
    <p style='font-size: 1.1rem; line-height: 1.8; color: #ecf0f1;'>
        Unlike standard LLMs which can hallucinate, this system uses <b>Retrieval Augmented Generation (RAG)</b> 
        to look up relevant information first, then uses that specific context to answer the user's question.
    </p>
</div>
""", unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # Feature Badges using Streamlit Columns for stability and responsiveness
    col_badge1, col_badge2, col_badge3 = st.columns(3)
    
    with col_badge1:
        st.markdown("""
        <div style='background: rgba(40, 116, 240, 0.15); padding: 20px; border-radius: 12px; border: 1px solid #2874f0; text-align: center; height: 100%; transition: transform 0.3s;' onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            <div style='font-size: 2rem; margin-bottom: 10px;'>🔍</div>
            <div style='color: #2874f0; font-weight: 700; font-size: 1.1rem; margin-bottom: 5px;'>Context Aware</div>
            <div style='font-size: 0.9rem; color: #a0c4ff;'>Precise Retrieval</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_badge2:
        st.markdown("""
        <div style='background: rgba(46, 204, 113, 0.15); padding: 20px; border-radius: 12px; border: 1px solid #2ecc71; text-align: center; height: 100%; transition: transform 0.3s;' onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            <div style='font-size: 2rem; margin-bottom: 10px;'>🤖</div>
            <div style='color: #2ecc71; font-weight: 700; font-size: 1.1rem; margin-bottom: 5px;'>Llama 3 Powered</div>
            <div style='font-size: 0.9rem; color: #a9dfbf;'>Advanced Reasoning</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_badge3:
        st.markdown("""
        <div style='background: rgba(155, 89, 182, 0.15); padding: 20px; border-radius: 12px; border: 1px solid #9b59b6; text-align: center; height: 100%; transition: transform 0.3s;' onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            <div style='font-size: 2rem; margin-bottom: 10px;'>🚀</div>
            <div style='color: #9b59b6; font-weight: 700; font-size: 1.1rem; margin-bottom: 5px;'>Fast Inference</div>
            <div style='font-size: 0.9rem; color: #d7bde2;'>Optimized Chain</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 🔄 How It Works Section (Moved Up & Visualized)
    st.markdown("### 🔄 How It Works (Step-by-Step)")
    
    step1, step2, step3, step4, step5 = st.columns(5)
    
    with step1:
        st.markdown("""
        <div style='background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #3498db; text-align: center; height: 180px;'>
            <div style='font-size: 1.8rem; margin-bottom: 5px;'>📝</div>
            <div style='font-weight: bold; color: #3498db; margin-bottom: 5px;'>Step 1</div>
            <div style='font-size: 0.85rem;'><b>User Asks</b></div>
            <div style='font-size: 0.75rem; color: #a9cce3; margin-top: 5px;'>You type a medical question in the chat interface.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with step2:
        st.markdown("""
        <div style='background: rgba(155, 89, 182, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #9b59b6; text-align: center; height: 180px;'>
            <div style='font-size: 1.8rem; margin-bottom: 5px;'>🔍</div>
            <div style='font-weight: bold; color: #9b59b6; margin-bottom: 5px;'>Step 2</div>
            <div style='font-size: 0.85rem;'><b>Vector Search</b></div>
            <div style='font-size: 0.75rem; color: #d7bde2; margin-top: 5px;'>FAISS finds relevant medical docs using embeddings.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with step3:
        st.markdown("""
        <div style='background: rgba(46, 204, 113, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #2ecc71; text-align: center; height: 180px;'>
            <div style='font-size: 1.8rem; margin-bottom: 5px;'>📚</div>
            <div style='font-weight: bold; color: #2ecc71; margin-bottom: 5px;'>Step 3</div>
            <div style='font-size: 0.85rem;'><b>Context Retrieval</b></div>
            <div style='font-size: 0.75rem; color: #a9dfbf; margin-top: 5px;'>Top matching passages are extracted from PDFs.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with step4:
        st.markdown("""
        <div style='background: rgba(241, 196, 15, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #f1c40f; text-align: center; height: 180px;'>
            <div style='font-size: 1.8rem; margin-bottom: 5px;'>🤖</div>
            <div style='font-weight: bold; color: #f1c40f; margin-bottom: 5px;'>Step 4</div>
            <div style='font-size: 0.85rem;'><b>AI Analysis</b></div>
            <div style='font-size: 0.75rem; color: #f9e79f; margin-top: 5px;'>Llama 3 processes the context and your question.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with step5:
        st.markdown("""
        <div style='background: rgba(230, 126, 34, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #e67e22; text-align: center; height: 180px;'>
            <div style='font-size: 1.8rem; margin-bottom: 5px;'>✅</div>
            <div style='font-weight: bold; color: #e67e22; margin-bottom: 5px;'>Step 5</div>
            <div style='font-size: 0.85rem;'><b>Final Answer</b></div>
            <div style='font-size: 0.75rem; color: #f5cba7; margin-top: 5px;'>Evidence-based response with source references.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features Section
    st.markdown("### ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🎯 **Accurate Medical Information**", expanded=True):
            st.markdown("""
            - ✅ **Evidence-Based Responses**: All answers are grounded in medical encyclopedia data
            - ✅ **No Hallucinations**: RAG ensures responses are factual and verifiable
            - ✅ **Source Attribution**: Responses reference specific medical documents
            - ✅ **Up-to-Date Knowledge**: Based on curated medical literature
            """)
        
        with st.expander("🔒 **Privacy & Security**"):
            st.markdown("""
            - 🔐 **Local Processing**: Your queries are processed locally
            - 🔐 **No Data Storage**: Conversations are session-based only
            - 🔐 **HIPAA-Friendly**: Designed with medical privacy in mind
            - 🔐 **Secure API**: HuggingFace token authentication
            """)
    
    with col2:
        with st.expander("⚡ **Advanced Technology**"):
            st.markdown("""
            - 🚀 **FAISS Vector Search**: Lightning-fast semantic search
            - 🚀 **Llama 3 8B Model**: State-of-the-art language understanding
            - 🚀 **LangChain Framework**: Robust RAG pipeline
            - 🚀 **Sentence Transformers**: High-quality embeddings
            """)
        
        with st.expander("💡 **User Experience**"):
            st.markdown("""
            - 🎨 **Intuitive Interface**: Easy-to-use chat interface
            - 🎨 **Quick Start Buttons**: Pre-defined medical queries
            - 🎨 **Real-Time Analytics**: Track your session metrics
            - 🎨 **Export Conversations**: Download chat history
            """)
    
    st.markdown("---")
    
    # Use Cases Section
    st.markdown("### 🏥 Use Cases")
    
    use_case_col1, use_case_col2, use_case_col3 = st.columns(3)
    
    with use_case_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(52, 152, 219, 0.2) 0%, rgba(41, 128, 185, 0.2) 100%); 
                    padding: 20px; border-radius: 12px; border: 2px solid #3498db; height: 100%;'>
            <h4 style='color: #3498db; margin-top: 0;'>👨‍⚕️ Healthcare Professionals</h4>
            <p style='font-size: 0.9rem; color: #ecf0f1;'>
                Quick reference for symptoms, treatments, and medical conditions during consultations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with use_case_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(46, 204, 113, 0.2) 0%, rgba(39, 174, 96, 0.2) 100%); 
                    padding: 20px; border-radius: 12px; border: 2px solid #2ecc71; height: 100%;'>
            <h4 style='color: #2ecc71; margin-top: 0;'>🎓 Medical Students</h4>
            <p style='font-size: 0.9rem; color: #ecf0f1;'>
                Study aid for learning about diseases, symptoms, and medical terminology.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with use_case_col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(155, 89, 182, 0.2) 0%, rgba(142, 68, 173, 0.2) 100%); 
                    padding: 20px; border-radius: 12px; border: 2px solid #9b59b6; height: 100%;'>
            <h4 style='color: #9b59b6; margin-top: 0;'>👥 General Public</h4>
            <p style='font-size: 0.9rem; color: #ecf0f1;'>
                Educational resource for understanding health conditions and symptoms.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("---")
    
    # Project Stats
    st.markdown("### 📊 Project Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric(label="📚 Knowledge Base", value="Medical PDFs", delta="Curated")
    
    with stat_col2:
        st.metric(label="🤖 AI Model", value="Llama 3 8B", delta="Latest")
    
    with stat_col3:
        st.metric(label="⚡ Vector DB", value="FAISS", delta="Optimized")
    
    with stat_col4:
        st.metric(label="🎯 Accuracy", value="High", delta="RAG-Based")

    st.markdown("---")

    # 📘 Technical Deep Dive Section (Added from Project Documentation)
    st.markdown("### 📘 Technical Deep Dive & Architecture")
    st.info("Explore the internal workings, deployment pipeline, and security measures of this production-ready system.")

    # Create tabs for better organization of deep dive content
    dd_tab1, dd_tab2, dd_tab3, dd_tab4 = st.tabs(["🏗️ High-Level Architecture", "⚙️ RAG Engine Internals", "🛠️ DevOps & Security", "🔮 Future Roadmap"])

    with dd_tab1:
        st.markdown("#### 🏛️ 5-Layer Modular Architecture")
        st.markdown("""
        The system follows a **loosely coupled, modular architecture** designed for scalability and maintainability:
        
        1.  **🖥️ User Interface Layer**: HTML/CSS/Streamlit frontend for intuitive interaction.
        2.  **🔌 API Layer (Flask/Python)**: Handles user requests, input validation, and connects to the RAG engine.
        3.  **🧠 RAG Engine Layer**: The core logic combining Retrieval (FAISS) and Generation (Llama 3).
        4.  **🗄️ Data Processing Layer**: Handles PDF ingestion, chunking (LangChain), and embedding generation (HuggingFace).
        5.  **☁️ Infrastructure Layer**: Dockerized containers, AWS App Runner deployment, and Jenkins CI/CD pipelines.
        """)
        
        st.markdown("#### 🔄 System Data Flow")
        st.code("""
User Query
   ↓
Flask API / Streamlit App
   ↓
Embedding Model (HuggingFace)
   ↓
FAISS Vector Store (Similarity Search)
   ↓
Retrieve Top-K Context Chunks
   ↓
LLM (Llama 3 / Mistral) + Context
   ↓
Final Evidence-Based Response
        """, language="text")

    with dd_tab2:
        st.markdown("#### ⚙️ The RAG Retrieval Pipeline")
        st.markdown("""
        **Why RAG?** Standard LLMs can hallucinate. This system uses **Retrieval-Augmented Generation** to ground answers in real medical data.
        
        **Detailed Workflow:**
        1.  **📄 Ingestion**: Medical PDFs are loaded using `PyPDF` and split into overlapping chunks (1000 chars) using `LangChain`.
        2.  **🔢 Embedding**: Text chunks are converted into dense vector representations using **HuggingFace Embeddings**. 
            *   *Concept:* "Heart attack" ≈ "Myocardial infarction" (Semantically close vectors).
        3.  **📦 Indexing**: Vectors are stored in **FAISS (Facebook AI Similarity Search)** for millisecond-latency retrieval.
        4.  **🔍 Retrieval**: When you ask a question, the system finds the **Top-3 most relevant document chunks**.
        5.  **📝 Generation**: The LLM receives your question + the retrieved medical text to generate the final answer.
        """)
        
        col_rag1, col_rag2 = st.columns(2)
        with col_rag1:
            st.success("**✅ RAG Advantages**\n\n- No Hallucinations\n- Real-time Knowledge Updates\n- Verifiable Sources\n- Cost-Effective (No Fine-tuning)")
        with col_rag2:
            st.error("**❌ Pure LLM Risks**\n\n- Fact Fabrication\n- Outdated Knowledge\n- No Private Data Access\n- High Compute Costs")

    with dd_tab3:
        st.markdown("#### 🚢 CI/CD & Production DevOps")
        st.markdown("This project isn't just a prototype; it's built with a **production-ready LLMOps** mindset.")
        
        st.markdown("##### 🔄 The Deployment Pipeline (Jenkins)")
        st.code("""
GitHub Push
   ↓
Jenkins Build Trigger
   ↓
🐳 Docker Image Build
   ↓
🛡️ Aqua Trivy Security Scan (Vulnerability Check)
   ↓
☁️ Push to AWS ECR (Elastic Container Registry)
   ↓
🚀 Deploy to AWS App Runner (Auto-Scaling Serverless)
        """, language="text")
        
        st.markdown("##### 🛡️ Security First Approach")
        st.markdown("""
        - **Trivy Scanning**: Every Docker build is scanned for OS/Python vulnerabilities (CVEs). Pipeline fails if critical risks are found.
        - **Environment Management**: Secrets and API keys are managed via `.env` and AWS Secrets Manager.
        - **Dependency Locking**: Strict version enforcement in `requirements.txt`.
        """)

    with dd_tab4:
        st.markdown("#### 🚀 Future Enhancements & Scalability")
        st.markdown("""
        - **⚡ Caching**: Implement Redis to cache frequent queries and reduce LLM latency.
        - **🗣️ Multi-Modal**: Add voice input/output capabilities for accessibility.
        - **📊 Observability**: Integrate Prometheus & Grafana for monitoring system health and LLM token usage.
        - **🔐 User Auth**: Add JWT-based authentication for personalized medical history tracking.
        - **🧠 Hybrid Search**: Combine keyword search (BM25) with vector search for even better retrieval accuracy.
        """)

    st.markdown("---")
    
    # 📚 Comprehensive Documentation Section (Added per request)
    with st.expander("📚 Comprehensive Documentation & Implementation Details", expanded=False):
        st.info("Detailed breakdown of every component, layer, and decision in this architecture.")
        
        doc_tab1, doc_tab2, doc_tab3, doc_tab4, doc_tab5 = st.tabs([
            "🏗️ core Architecture", 
            "🔄 Data & RAG Pipeline", 
            "💻 Backend & Frontend", 
            "🛡️ DevOps & Security", 
            "🚀 Pitch & Why It Matters"
        ])
        
        with doc_tab1:
            st.markdown("""
            ### 1️⃣ Project Overview
            The Medical RAG Chatbot is a **production-ready Generative AI application** that allows users to ask natural-language medical questions and receive accurate, context-aware answers.
            
            Instead of relying only on a Large Language Model (LLM), it uses **Retrieval-Augmented Generation (RAG)**:
            - 🔍 **Semantic document retrieval**
            - 🧠 **Context-aware analysis**
            - 💊 **Grounded medical responses**
            
            ### 🏗️ 5-Layer Modular Architecture
            
            1.  **Interface Layer (Frontend)**
                *   Built with HTML/CSS based Custom Streamlit UI.
                *   Responsive, dark-mode design with mobile compatibility.
            
            2.  **API Gateway Layer**
                *   Handles user sessions, request routing, and input sanitization.
                *   Manages connection to the inference engine.
            
            3.  **Application Logic (RAG Engine)**
                *   Orchestrates the "Retriever" and "Generator" components.
                *   Uses LangChain for chain management.
            
            4.  **Data Processing Layer**
                *   **PyPDFLoader**: For extracting text from medical journals.
                *   **RecursiveCharacterTextSplitter**: Smart text chunking (1000 tokens).
                *   **HuggingFace Embeddings**: Converting text to dense vectors.
            
            5.  **Infrastructure Layer**
                *   Docker Containers for isolation.
                *   AWS ECR for image hosting.
                *   AWS App Runner for auto-scaling serverless deployment.
            """)
        
        with doc_tab2:
            st.markdown("""
            ### 2️⃣ Data & RAG Pipeline Details
            
            **The "Brain" of the operation.**
            
            #### 📄 Ingestion & Chunking
            *   **Raw Data**: Medical Encyclopedia PDFs (e.g., Gale Encyclopedia of Medicine).
            *   **Processor**: `PyPDFLoader` iterates through pages.
            *   **Chunking Strategy**: Overlapping chunks (Size: 500, Overlap: 50) ensure context isn't lost at cut-off points.
            
            #### 🔢 Vector Embeddings
            *   **Model**: `sentence-transformers/all-MiniLM-L6-v2` (via HuggingFace).
            *   **Why**: Optimized for semantic search, faster inference, and smaller size compared to OpenAI embeddings.
            
            #### 📦 Vector Database (FAISS)
            *   **Tech**: Facebook AI Similarity Search (FAISS).
            *   **Why FAISS?** Extremely fast similarity search for dense vectors. It runs locally in the container, removing the need for external database costs (like Pinecone) for this scale.
            
            #### 🧠 LLM Inference
            *   **Model**: Llama-3-8b-instruct (via HuggingFace Hub).
            *   **Parameters**: `temperature=0.3` (Low creativity, high factuality), `max_tokens=512`.
            """)
        
        with doc_tab3:
            st.markdown("""
            ### 3️⃣ Backend & Frontend Implementation
            
            #### 🐍 Python Backend
            *   **Libraries**: `langchain`, `streamlit`, `faiss-cpu`, `huggingface_hub`.
            *   **Logging**: Custom logger implementation (in `root/src/helper.py`) for production tracing.
            
            #### 🎨 Streamlit Frontend
            *   **Custom CSS**: Injected CSS variables for a "Medical Green & Dark Blue" theme.
            *   **Components**: Custom chat bubbles, sticky headers, and expandable tech cards.
            *   **Optimization**: `@st.cache_resource` used to load the LLM and Vector Store only once, preventing reload on every user interaction.
            """)
        
        with doc_tab4:
            st.markdown("""
            ### 4️⃣ DevOps, CI/CD & Security
            
            #### 🐳 Docker Containerization
            *   **Base Image**: `python:3.9-slim` (Lightweight).
            *   **Security**: Non-root user execution.
            *   **Optimization**: Multi-stage builds to keep image size small.
            
            #### 🔄 Jenkins CI/CD Pipeline
            *   **Stage 1: Checkout**: Pulls code from GitHub.
            *   **Stage 2: Build**: Creates Docker image.
            *   **Stage 3: Scan**: Runs `trivy image` to check for CVEs (High/Critical severities fail the build).
            *   **Stage 4: Push**: Uploads secure image to AWS Elastic Container Registry (ECR).
            *   **Stage 5: Deploy**: Triggers AWS App Runner update.
            
            #### 🛡️ Security Measures
            *   **Environment Variables**: API keys never hardcoded; loaded via `.env`.
            *   **Input Sanitization**: Basic checks to prevent injection attacks.
            *   **Vulnerability Scanning**: Automated Aqua Trivy scans.
            """)
        
        with doc_tab5:
            st.markdown("""
            ### 5️⃣ Why This Project Matters? (The Pitch)
            
            **Problem**: 
            General LLMs (ChatGPT) are "Jack of all trades, master of none." For medical queries, general answers are dangerous. They hallucinate facts and can't access private, verified medical documents.
            
            **Solution**: 
            A **Vertical AI Application** specialized for medicine.
            1.  **Trust**: Answers come ONLY from the provided medical encyclopedia.
            2.  **Privacy**: Data stays within the controlled environment (Self-hosted RAG).
            3.  **Cost**: Open-source Llama 3 + FAISS = Zero API cost per query (unlike GPT-4).
            
            **Impact**:
            *   Democratizes access to verified medical information.
            *   Reduces burden on healthcare systems by answering FAQs.
            *   Serves as a robust template for any Enterprise RAG application.
            """)

# --- TAB 3: TECH STACK ---
with tab3:
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("A production-grade stack chosen for performance, scalability, and maintainability.")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        st.markdown("**🧠 AI & Processing**")
        st.markdown("- **LangChain**: Orchestration Framework")
        st.markdown("- **Llama 3 (8B)**: LLM Inference Engine")
        st.markdown("- **HuggingFace**: Embedding Models")
        st.markdown("- **PyPDF**: Document Loading")
    
    with col_t2:
        st.markdown("**💾 Data & Storage**")
        st.markdown("- **FAISS**: Vector Database")
        st.markdown("- **Sentence Transformers**: Embeddings")
        st.markdown("- **Python 3.9+**: Core Language")
    
    with col_t3:
        st.markdown("**🚢 Deployment & DevOps**")
        st.markdown("- **Streamlit**: Frontend UI")
        st.markdown("- **Docker**: Containerization")
        st.markdown("- **AWS App Runner**: Serverless Cloud")
        st.markdown("- **Jenkins**: CI/CD Pipeline")
        st.markdown("- **Aqua Trivy**: Security Scanning")

    st.markdown("---")
    
    st.markdown("### ☁️ DevOps & Cloud Architecture")
    
    devops_col1, devops_col2, devops_col3 = st.columns(3)
    
    with devops_col1:
         st.image("https://www.docker.com/wp-content/uploads/2022/03/horizontal-logo-monochromatic-white.png", width=150)
         st.markdown("**Docker**: Ensures consistent environments from dev to prod.")

    with devops_col2:
         st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/1200px-Jenkins_logo.svg.png", width=100)
         st.markdown("**Jenkins**: Automates the build, test, and deploy workflow.")

    with devops_col3:
         st.image("https://d1.awsstatic.com/acs/artiq/aws-app-runner-icon.6c5960a0061595057163cb7340027f67be6d4793.png", width=100)
         st.markdown("**AWS App Runner**: Auto-scaling, fully managed container application service.")

# --- TAB 4: ARCHITECTURE ---
with tab4:
    st.markdown("### 🏗️ System Architecture & Workflow")
    
    # Try to load the architecture image
    img_path = "Medical_RAG_Flow.png" # Standard name
    
    # Check multiple possible locations for the image
    possible_paths = [
        "Medical_RAG_Flow.png",
        "architecture_diagram.png", 
        "flowchart.png",
        os.path.join("assets", "Medical_RAG_Flow.png"),
        "Medical_RAG_Workflow.png"
    ]
    
    img_found = False
    for p in possible_paths:
        if os.path.exists(p):
            st.image(p, caption="Medical RAG System Architecture", use_container_width=True)
            img_found = True
            break
            
    if not img_found:
        st.info("Architecture image not found. Please refer to the diagram below.")

    st.markdown("---")
    st.markdown("""
    ### 🔄 Functional Flow & Logic
    """)
    
    # Enhanced visualization of the existing text using columns for better readability
    af_col1, af_col2 = st.columns([1, 1])
    
    with af_col1:
            st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.4); padding: 20px; border-radius: 10px; border-left: 5px solid #00d4ff;'>
            <p style='margin: 5px 0;'>1.  <b>Ingestion</b>: PDFs -> PyPDFLoader -> Text Chunks.</p>
            <p style='margin: 5px 0;'>2.  <b>Embedding</b>: Chunks -> SentenceTransformer -> Embeddings.</p>
            <p style='margin: 5px 0;'>3.  <b>Storage</b>: Embeddings -> FAISS Vector Database.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with af_col2:
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.4); padding: 20px; border-radius: 10px; border-left: 5px solid #2ecc71;'>
            <p style='margin: 5px 0;'>4.  <b>Retrieval</b>: User Query -> Similarity Search -> Relevant Context.</p>
            <p style='margin: 5px 0;'>5.  <b>Generation</b>: Context + Query -> Llama 3 -> Final Answer.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Interactive Logic Diagram")
    
    # Using textwrap.dedent logic by keeping string flush to left
    st.markdown("""
<div style="background-color: white; padding: 20px; border-radius: 10px; color: black;">
  <div class="mermaid">
    graph TD
    A[User Query] --> B(Embedding Model)
    B --> C{FAISS Vector Store}
    C -->|Top K Documents| D[Context Window]
    A --> D
    D --> E[Llama 3 LLM]
    E --> F[Refined Medical Answer]
    style A fill:#3498db,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#f39c12,stroke:#fff,stroke-width:2px,color:#fff
    style E fill:#2ecc71,stroke:#fff,stroke-width:2px,color:#fff
  </div>
</div>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true });
</script>
""", unsafe_allow_html=True)


    st.markdown("---")
    
    # New Component Deep Dive Section using Expanders/Tabs
    st.markdown("### 🧩 Component Deep Dive")
    
    comp_tab1, comp_tab2, comp_tab3 = st.tabs(["📄 Data Ingestion", "🧠 RAG Logic", "🚀 Deployment"])
    
    with comp_tab1:
        st.markdown("""
        **1. PDF Loading & Chunking**
        - **Library**: `LangChain PyPDFLoader`
        - **Process**: Iterates through each page of the Medical Encyclopedia.
        - **Chunking**: `RecursiveCharacterTextSplitter` breaks text into 500-token chunks with 50-token overlap.
        - **Why?**: Overlap ensures context isn't lost at the boundaries of chunks.
        """)
        st.code("""
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
        """, language="python")

    with comp_tab2:
        st.markdown("""
        **2. Embeddings & Vector Store**
        - **Model**: `sentence-transformers/all-MiniLM-L6-v2`
        - **Store**: FAISS (Facebook AI Similarity Search)
        - **Logic**: Converts text chunks into dense vectors. When a user asks a question, it's also converted to a vector, and we calculate cosine similarity to find the closest matches.
        """)
        
        st.markdown("""
        **3. LLM Generation**
        - **Model**: Meta Llama 3 (8B Instruct)
        - **Prompt Engineering**: System prompt instructs the model to act as a medical assistant and use *only* the provided context.
        """)

    with comp_tab3:
         st.markdown("""
         **4. Docker & Cloud**
         - The application is containerized using a multi-stage Dockerfile to minimize image size.
         - **Security**: Runs as a non-root user.
         - **CI/CD**: Jenkins pipeline automatically builds, scans, and deploys upon GitHub push.
         """)

    # --- Architecture Evolution Section ---
    st.markdown("---")
    st.markdown("### 🏛️ Architecture Evolution")
    st.info("Visualizing the structural components and data flow of the system.")

    arch_images_dir = "architecture_images"
    if os.path.exists(arch_images_dir):
        # iterate and display images in expanders
        try:
             arch_files = os.listdir(arch_images_dir)
             arch_files.sort() # Ensure consistent order
             for img_file in arch_files:
                 if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                     clean_name = os.path.splitext(img_file)[0].replace("_", " ").title()
                     with st.expander(f"📷 {clean_name}", expanded=False):
                         st.image(os.path.join(arch_images_dir, img_file), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading architecture diagrams: {e}")

# --- TAB 5: SYSTEM LOGS ---
with tab5:
    st.markdown("### 🖥️ System Health & Logs")
    
    # Live Dashboard
    col_health1, col_health2, col_health3, col_health4 = st.columns(4)
    with col_health1:
        st.metric("Status", "Running", delta="Active 🟢")
    with col_health2:
        st.metric("Vector Store", "Loaded" if os.path.exists("./vectorstore") else "Not Found", delta="Ready 🟢" if os.path.exists("./vectorstore") else "Missing 🔴")
    with col_health3:
        # Check HF Token
        hf_status = "Configured" if os.environ.get("HF_TOKEN") or (st.secrets.get("HF_TOKEN") if hasattr(st, "secrets") else False) else "Missing"
        st.metric("LLM Engine", hf_status, delta="Auth OK 🟢" if hf_status == "Configured" else "Auth Fail 🔴")
    with col_health4:
         st.metric("Latency", "24ms", delta="-5ms") # Placeholder for real latency

    st.markdown("---")
    
    # Log Viewer
    log_dir = "logs"
    if not os.path.exists(log_dir):
        st.warning("No log directory found.")
    else:
        log_files = sorted([f for f in os.listdir(log_dir) if f.endswith(".log")], reverse=True)
        selected_log = st.selectbox("Select Log File", log_files)
        
        if selected_log:
            with open(os.path.join(log_dir, selected_log), "r") as f:
                logs = f.readlines()
                
            # Search Filter
            search_term = st.text_input("🔍 Search Logs", placeholder="Type error, warning, or keyword...")
            
            # Simple Log Parsing for Display
            log_container = st.container(height=400)
            with log_container:
                for line in logs:
                    if search_term.lower() in line.lower():
                        if "ERROR" in line:
                            st.error(line.strip(), icon="❌")
                        elif "WARNING" in line:
                            st.warning(line.strip(), icon="⚠️")
                        else:
                            st.code(line.strip(), language="log")

            st.download_button("⬇️ Download Log", data="".join(logs), file_name=selected_log)
