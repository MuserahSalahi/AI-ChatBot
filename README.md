#  AI Chatbot

A professional AI-powered chatbot built with **Streamlit**, **LangChain**, and **Groq LLMs**, featuring intelligent API key fallback, multi-session chat history management, and a modern user interface.

---

##  Overview

AI Chatbot is a smart conversational assistant designed to provide accurate, context-aware, and professional responses. The application utilizes Groq's high-performance language models through LangChain and automatically switches between multiple API keys and models whenever rate limits are encountered.

The system also supports persistent conversation storage, allowing users to manage and revisit previous chat sessions.

---

##  Features

###  Intelligent AI Responses

* Powered by Groq Large Language Models
* Context-aware conversations
* Professional and accurate responses

###  Smart Fallback Architecture

* Automatic API key rotation
* Automatic model switching
* Handles rate limits seamlessly
* Improved reliability and uptime

###  Multi-Session Chat Management

* Create unlimited conversations
* Switch between previous chats
* Persistent chat storage using JSON

###  Modern User Interface

* Clean and responsive Streamlit design
* Professional layout
* Sticky footer
* Elegant conversation history panel

### High Performance

* Fast response generation
* Optimized LangChain pipeline
* Efficient session management

---

##  Technology Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Backend Development             |
| Streamlit  | Web Application Framework       |
| LangChain  | LLM Orchestration               |
| Groq API   | AI Model Provider               |
| dotenv     | Environment Variable Management |
| JSON       | Session Storage                 |

---

##  Project Structure

```text
AI-Chatbot/
│
├── app.py
├── .env
├── requirements.txt
├── .gitignore
├── chat_sessions.json
└── README.md
```

---

##  Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Chatbot.git
cd AI-Chatbot
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GROQ_API_KEYS=gsk_key_1,gsk_key_2,gsk_key_3
```

### Notes

* Multiple API keys can be added.
* Separate keys using commas.
* Never upload your `.env` file to GitHub.
* Add `.env` to `.gitignore`.

---

##  Running the Application

```bash
streamlit run app.py
```

The application will launch in your browser automatically.

---

##  Fallback Mechanism

The chatbot implements a robust fallback strategy:

1. Primary Groq Model

   * llama-3.3-70b-versatile

2. Backup Groq Model

   * llama-3.1-8b-instant

3. Automatic API Key Rotation

If:

* Rate limit occurs
* API quota is exhausted
* Temporary API restriction happens

The system automatically switches to the next available model or API key without interrupting the user experience.

---

##  Chat History Storage

Conversation history is automatically stored in:

```text
chat_sessions.json
```

Features:

* Persistent storage
* Session recovery
* Multiple conversation management
* Automatic saving

---

##  Security Best Practices

* Store API keys in `.env`
* Never expose credentials publicly
* Use `.gitignore`
* Keep dependencies updated
* Rotate API keys regularly

---

##  Future Enhancements

* User Authentication
* Database Integration
* Voice Input Support
* File Upload Analysis
* PDF Question Answering
* Image Understanding
* Dark Mode Support
* Cloud Deployment

---

##  Application Highlights

* Professional Interface
* Session-Based Conversations
* Intelligent Context Handling
* Smart Failover Architecture
* Persistent Chat Storage

---

##  Contributing

Contributions, feature suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

---

##  License

This project is intended for educational and learning purposes.

---

#  Author

### Muserah Salahi

**Artificial Intelligence Student | Machine Learning Enthusiast | Python Developer**

This project was designed and developed by **Muserah Salahi** as part of continuous learning and practical implementation of modern AI technologies.

### Connect

* LinkedIn: Muserah Salahi
* GitHub: MuserahSalahi

---

### ⭐ If you find this project useful, consider giving it a star on GitHub.
