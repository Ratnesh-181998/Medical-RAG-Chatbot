# 🏥 Medical RAG Chatbot: Advanced AI Health Assistant
<img width="940" height="445" alt="image" src="https://github.com/user-attachments/assets/d225cd28-e180-4d04-a528-788a8d836acb" />

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appudtzei3tyyttd6xjhwur.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-orange)](https://www.langchain.com/)
[![FAISS](https://img.shields.io/badge/Vector%20Database-FAISS-green)](https://github.com/facebookresearch/faiss)
[![GitHub Issues](https://img.shields.io/github/issues/Ratnesh-181998/Medical-RAG-Chatbot.svg)](https://github.com/Ratnesh-181998/Medical-RAG-Chatbot/issues)

> **An intelligent, Retrieval-Augmented Generation (RAG) powered conversational AI designed to provide accurate medical information from verified documentation.**

---

## 📖 Table of Contents
- [✨ Introduction](#-introduction)
- [🚀 Key Features](#-key-features)
- [🏗️ System Architecture](#-system-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📲 App Walkthrough (UI Sections)](#-app-walkthrough-ui-sections)
    - [1. Demo Project](#1-demo-project)
    - [2. About Project](#2-about-project)
    - [3. Tech Stack](#3-tech-stack)
    - [4. Architecture](#4-architecture)
    - [5. System Logs](#5-system-logs)
- [⚙️ Installation & Setup](#-installation--setup)
- [📦 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [📞 Contact](#-contact)
---
## 🌐🎬 Live Demo
🚀 **Try it now:**
- **Streamlit Profile** -[[Link]](https://share.streamlit.io/user/ratnesh-181998)
- **Project Demo** - [[Medical ChatBot Link]](https://medical-rag-chatbot-a7zyhffk6df9nqyek9jb5u.streamlit.app/)

### 🎥 Live Preview
![App Demo](Medical_RAG_Demo_Video.webp)

---

### 🎬 Live Project Demo
> Experience the full flow:

![Project Demo Walkthrough](Medical_RAG_Complete_Walkthrough.gif)

---

## ✨ Introduction

The **Medical RAG Chatbot** is a state-of-the-art AI application built to bridge the gap between complex medical documentation and accessible, user-friendly health queries. By leveraging **Llama-3 (via Hugging Face)** for reasoning and **FAISS** for fast similarity search, this system ingests medical PDFs (e.g., "The Gale Encyclopedia of Medicine"), understands user questions, and retrieves precise, context-aware answers.

Unlike standard chatbots, this system is grounded in **RAG (Retrieval-Augmented Generation)**, meaning every answer is backed by retrieved evidence from trusted sources, significantly reducing hallucinations.

---

## 🚀 Key Features

*   **🔍 RAG-Powered Accuracy**:Retrieves relevant context from indexed medical PDFs before answering.
*   **🤖 Advanced LLM Integration**: Uses `Llama-3` (via Hugging Face API) for high-quality natural language understanding.
*   **⚡ Fast Vector Search**: Implements **FAISS (Facebook AI Similarity Search)** for millisecond-latency document retrieval.
*   **🧠 Conversation Memory**: Remembers past interactions to provide context-aware follow-up answers.
*   **📄 Source Attribution**: Shows exactly which part of the document was used to generate the answer.
*   **🖥️ System Health Dashboard**: Real-time monitoring of vector store status, LLM connectivity, and system latency.
*   **🎨 Premium UI/UX**: A polished Streamlit interface with a custom medical green theme, smooth transitions, and interactive components.

---

### Medical RAG System Architecture

<img width="1117" height="585" alt="image" src="https://github.com/user-attachments/assets/72b5240c-87ba-4d85-80b3-30aa0d67fc9d" />

---
### Interactive Logic Diagram
<img width="496" height="680" alt="image" src="https://github.com/user-attachments/assets/24f0d351-6fa5-4bc2-be17-408dc2999dd0" />

---
### Architecture Evolution
- 📷 Architecture View 1 — Very Simple
<img width="1200" height="504" alt="image" src="https://github.com/user-attachments/assets/b27bb53e-72c8-4839-8217-b51873911295" />
- 📷 Architecture View 2 — Basic Rag Flow
<img width="1218" height="633" alt="image" src="https://github.com/user-attachments/assets/6a4d91ad-01bc-4e9e-b05c-11add2b5a1e8" />
-  Architecture View 3 – Rag With Embeddings
<img width="1215" height="638" alt="image" src="https://github.com/user-attachments/assets/5ff22dcf-73f8-4415-9bdf-0db614023d9e" />
-  Architecture View 4 — Full Application Architecture
<img width="1199" height="647" alt="image" src="https://github.com/user-attachments/assets/45013360-ce71-44a6-b5ac-7c295bf02923" />
- Architecture View 5 — With Memory (Chat History)
<img width="1171" height="653" alt="image" src="https://github.com/user-attachments/assets/2ab084a2-79be-42f4-b903-40bfa6f2b5c3" />
-  Architecture View 6 – Production + Devops
<img width="1191" height="608" alt="image" src="https://github.com/user-attachments/assets/72060362-1970-4e30-9dbd-aa4a0be1dc19" />
- Architecture View 7 — End-To-End (Best Final Diagram)
<img width="1221" height="696" alt="image" src="https://github.com/user-attachments/assets/2a25467e-b30c-48f8-b17d-7ca3eaae336c" />

---
## 🏗️ System Architecture

The system follows a robust data pipeline:

1.  **Ingestion**: Loading medical PDFs using `PyPDFLoader`.
2.  **Chunking**: Splitting text into manageable chunks (`RecursiveCharacterTextSplitter`).
3.  **Embedding**: Converting text to vectors using `SentenceTransformer` (`all-MiniLM-L6-v2`).
4.  **Storage**: Indexing vectors in a local `FAISS` database.
5.  **Retrieval**: Fetching top-k relevant chunks for a user query.
6.  **Generation**: Synthesizing the final answer using the LLM.

![System Architecture](architecture_images/Architecture%20View%207%20—%20End-to-End%20(Best%20Final%20Diagram).png)

<img width="1095" height="719" alt="image" src="https://github.com/user-attachments/assets/d595d389-1c37-447d-84d7-6cbca0555d30" />

*(See the **Architecture** tab in the app for an interactive deep dive into each component.)*

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interactive Web UI & Dashboard |
| **LLM Engine** | **Llama 3 (via Groq/HF)** | Natural Language Generation |
| **Embeddings** | **SentenceTransformers** | Semantic text representation |
| **Vector DB** | **FAISS** | High-performance similarity search |
| **Orchestration** | **LangChain** | Chaining retrieval and generation flows |
| **DevOps** | **Docker & Jenkins** | Containerization & CI/CD Pipelines |
| **Security** | **Aqua Trivy** | Container vulnerability scanning |
| **Cloud** | **AWS App Runner** | Scalable cloud deployment |
| **Language** | **Python 3.10** | Core programming language |

---

## 📲 App Walkthrough (UI Sections)

### 1. 💬 Demo Project
The main interface where users interact with the AI.
- **Input Area**: Type medical questions (e.g., *"What are symptoms of Pneumonia?"*).
- **Answer Display**: Receive detailed, AI-generated responses.
- **Reference Context**: Expandable section showing the raw source text used for the answer.
- **Metrics**: Real-time display of execution time and confidence.
<img width="1873" height="691" alt="image" src="https://github.com/user-attachments/assets/ebd02ea8-fa21-47ed-9496-3f8f55178cf1" />
<img width="1771" height="764" alt="image" src="https://github.com/user-attachments/assets/0c39dd8c-2888-403a-814a-1d2cfe3e6c87" />
<img width="1821" height="722" alt="image" src="https://github.com/user-attachments/assets/1cf52ca5-3026-4dd0-a0b1-0f94d792edb9" />
<img width="1739" height="757" alt="image" src="https://github.com/user-attachments/assets/b9b2bd5d-0574-4f9b-b1cc-d558133f6756" />
<img width="1840" height="699" alt="image" src="https://github.com/user-attachments/assets/017dfe4b-0abd-4fe9-978b-cec2336b806f" />
<img width="1838" height="738" alt="image" src="https://github.com/user-attachments/assets/56e48429-bb34-4299-9f10-d72ddbab3566" />
<img width="1867" height="655" alt="image" src="https://github.com/user-attachments/assets/bd22c624-6369-4bf5-ab35-5d32b62a76d2" />

### 2. 📖 About Project
A detailed overview of the project's mission.
- Explains the "Why" and "How" of Medical RAG.
- Highlights the datasets used (Gale Encyclopedia of Medicine).
- outlines the solution approach.
<img width="1787" height="764" alt="image" src="https://github.com/user-attachments/assets/02d473ed-6b20-4078-8698-ee51267c6831" />
<img width="1519" height="636" alt="image" src="https://github.com/user-attachments/assets/787c82c5-b196-4c7e-80e9-2453a8c12183" />
<img width="1506" height="648" alt="image" src="https://github.com/user-attachments/assets/4d31dce2-f668-4011-9160-50cb463da79c" />
<img width="1484" height="686" alt="image" src="https://github.com/user-attachments/assets/2492e3db-c5ac-4f51-aa2e-f959b8999f2c" />
<img width="1424" height="719" alt="image" src="https://github.com/user-attachments/assets/e56823b7-0d7d-40c3-a1e8-8bd1ecb4f682" />
<img width="1318" height="688" alt="image" src="https://github.com/user-attachments/assets/f1dab6c6-db0a-46ca-a582-66222ef1eba7" />
<img width="1193" height="591" alt="image" src="https://github.com/user-attachments/assets/a175a8f5-ecba-4b0e-a74f-201150d177f0" />
<img width="1362" height="636" alt="image" src="https://github.com/user-attachments/assets/7dc54f60-3f2e-4dfe-8417-e78b34c9b865" />
<img width="711" height="756" alt="image" src="https://github.com/user-attachments/assets/1ba60686-349f-4a3e-8dc1-72b3814a120c" />
<img width="1429" height="700" alt="image" src="https://github.com/user-attachments/assets/52060ba3-239c-477e-bcfc-fc924705a2b1" />
<img width="1376" height="582" alt="image" src="https://github.com/user-attachments/assets/69febed3-e4bc-456a-b995-26fe3e85f00c" />
<img width="1234" height="760" alt="image" src="https://github.com/user-attachments/assets/025deb1e-9885-47b1-a4fb-c1ebea96493d" />
<img width="1392" height="566" alt="image" src="https://github.com/user-attachments/assets/093cd92e-00bc-42f9-9797-fc9d46cb6a6d" />

### 3. 🛠 Tech Stack
Visual representation of the technologies used.
- Cards for **LLM**, **Vector Store**, **DevOps**, and **Frontend**.
- Explains the role of Docker, Jenkins, and AWS in the deployment pipeline.
<img width="1421" height="694" alt="image" src="https://github.com/user-attachments/assets/513ba69b-fc19-4ab8-80d3-99fed02797d2" />
<img width="1390" height="753" alt="image" src="https://github.com/user-attachments/assets/94307c21-17a8-49aa-b8e2-aca6998d1d2b" />
<img width="1470" height="738" alt="image" src="https://github.com/user-attachments/assets/5bd51156-3623-428c-a023-0dbc767025eb" />
<img width="1330" height="735" alt="image" src="https://github.com/user-attachments/assets/a21a2a0f-5602-498f-b431-687907938e73" />
<img width="1467" height="689" alt="image" src="https://github.com/user-attachments/assets/15ef105f-e4bf-480e-8fef-97f03f737a39" />
<img width="1478" height="716" alt="image" src="https://github.com/user-attachments/assets/90fdc4ec-c5ca-4f99-820c-e55a3435a735" />

### 4. 🏛 Architecture
An educational hub for developers.
- **Interactive Flowcharts**: Visualizing the data journey from PDF to Answer.
- **Component Deep Dive**: Tabs explaining **Ingestion**, **Embedding**, and **Generation** with code snippets.
- **Evolution**: A gallery showing how the architecture evolved from MVP to Production.
<img width="1518" height="684" alt="image" src="https://github.com/user-attachments/assets/674d6ea0-9a89-448e-beb8-746b489808cb" />
<img width="1353" height="758" alt="image" src="https://github.com/user-attachments/assets/e76e9dad-d6ae-45a1-827d-4397ce02eae5" />
<img width="1439" height="720" alt="image" src="https://github.com/user-attachments/assets/aadefa22-d006-4f4d-bdc8-97f79d5cfb8b" />
<img width="1473" height="544" alt="image" src="https://github.com/user-attachments/assets/176aa7e3-47ec-4b81-9bcb-bd9265814b2f" />
<img width="1565" height="593" alt="image" src="https://github.com/user-attachments/assets/7aa8b039-1dd5-45ad-b14c-c2f2ffd143e6" />

### 5. 🖥️ System Health & Logs
A dashboard for administrators.
- **Status Indicators**: Green/Red lights for App, Vector Store, and LLM connectivity.
- **Live Logs**: Scrollable, filterable logs showing system activities and errors.
- **Download**: Export logs for external analysis.
<img width="1502" height="693" alt="image" src="https://github.com/user-attachments/assets/a9eaf851-e974-4b96-86cb-edee26a69bf4" />
<img width="1420" height="703" alt="image" src="https://github.com/user-attachments/assets/54827a91-5201-4dc1-8d9d-a756ea13c258" />
<img width="1426" height="745" alt="image" src="https://github.com/user-attachments/assets/0e91d3cf-b36b-46fa-8db2-954645409d26" />

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher.
- A Hugging Face API Token (for the LLM).

### 1. Clone the Repository
```bash
git clone https://github.com/Ratnesh-181998/Medical-RAG-Chatbot.git
cd Medical-RAG-Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory and add your API token:
```ini
HF_TOKEN=your_hugging_face_token_here
```

### 4. Run the Application
```bash
streamlit run Medical_Chatbot_streamlit_app.py
```
The app will open in your browser at `http://localhost:8501`.

---

## 📦 Project Structure

```bash
Medical-RAG-Chatbot/
├── architecture_images/       # Diagrams for documentation
├── vectorstore/               # FAISS index files (if local)
├── Medical_Chatbot_streamlit_app.py  # Main Entry Point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (GitIgnored)
└── README.md                  # Project Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**Ratnesh Kumar Singh**

- 📧 **Email**: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)
- 💼 **LinkedIn**: [Ratnesh Kumar Singh](https://www.linkedin.com/in/ratneshkumar1998/)
- 🐙 **GitHub**: [Ratnesh-181998](https://github.com/Ratnesh-181998)
- 📱 **Phone**: +91-947XXXXX46

### Project Links

- 🌐 **Live Demo**: [Streamlit App](https://medical-rag-chatbot-a7zyhffk6df9nqyek9jb5u.streamlit.app/)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/Ratnesh-181998/Medical-RAG-Chatbot/wiki)
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/Ratnesh-181998/Medical-RAG-Chatbot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ratnesh-181998/Medical-RAG-Chatbot/discussions)

  ---
*Built with passion for the AI Community. 🚀*

</div>

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%">
  
</div>

