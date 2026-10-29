# ChatBot with LangGraph Memory

A Python-based intelligent conversational assistant built using **LangGraph** and **LangChain**. This project implements persistent conversation memory using an underlying SQLite database, ensuring the chatbot retains context across user sessions.

## 🚀 Features

* **LangGraph Orchestration:** Utilizes state graphs to manage conversational flows and transitions smoothly.
* **Persistent Memory:** Uses a SQLite saver (`SqliteSaver`) to store and retrieve message histories across distinct thread IDs.
* **Environment Isolation:** Configured with a dedicated `.env` file for secure API key management and a Python virtual environment (`myenv`).

## 🛠️ Project Structure

```text
├── ChatBot_langgraph_memory/
│   ├── .env                       # Environment variables (API keys)
│   ├── .gitignore                 # Git ignore patterns (.env, myenv/, databases)
│   ├── langgraph_database.py      # Core chatbot logic and state graph definitions
│   ├── chatbot.db                 # Persistent SQLite database for memory
│   └── README.md                  # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd ChatBot_with_LangGraph_Memory
   ```

2. **Set up the virtual environment:**
   ```bash
   # Windows
   python -m venv myenv
   myenv\Scripts\activate

   # macOS/Linux
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install langchain langgraph openauth python-dotenv sqlite3
   ```
   *(Adjust dependency packages according to your specific LLM provider, e.g., `langchain-openai` or `langchain-anthropic`)*

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API credentials:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 💻 Usage

Run the main application script to initialize the chatbot state machine and begin chatting:

```bash
python langgraph_database.py
```
