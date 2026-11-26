# Day 1 – First LLM Application Using Groq

## 📌 Project Overview
A beginner Python project that connects to the Groq API and generates AI responses using an LLM (GPT-OSS 20B).

## 🛠️ Technologies
- Python
- Groq API
- GPT-OSS 20B
- python-dotenv

## 📁 Project Structure
```text
day1/
├── hello_llm.py
├── .env
└── README.md
```

## 📦 Installation

```bash
pip install groq python-dotenv
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

## 💻 Code Explanation

| Code | Purpose |
|---|---|
| `import os` | Access environment variables |
| `load_dotenv()` | Loads the `.env` file |
| `os.getenv()` | Retrieves the API key |
| `Groq()` | Creates the Groq API client |
| `model` | Selects the AI model |
| `role = "user"` | Defines the message sender |
| `prompt` | Contains the user's question |
| `messages = [message]` | Stores conversation messages |
| `chat.completions.create()` | Sends the request to the AI |
| `choices[0].message.content` | Extracts the AI response |
| `print(answer)` | Displays the response |

## 🔄 Workflow

1. Import libraries.
2. Load API key from `.env`.
3. Create Groq client.
4. Select AI model.
5. Create user prompt.
6. Send request to Groq API.
7. Receive and print AI response.

## 🧠 Key Concepts Learned
- API and API Key
- Environment Variables
- Large Language Models (LLMs)
- Prompts and Message Roles
- Groq Client
- Chat Completions

## 🎯 Learning Outcome
Learned how to connect Python with an LLM, send prompts, and generate AI responses using the Groq API.

**Next Topics:** System Role, Temperature, Conversation History, and Prompt Engineering.