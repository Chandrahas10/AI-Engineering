# Day 2 – System Role & Temperature in LLM

## 📌 Project Overview
This project explores how system roles and temperature settings influence AI-generated responses using the Groq API and GPT-OSS 20B model.

## 🧠 Key Concepts Learned

### 1. System Role
- Defines the AI's behaviour, personality, and instructions.
- Guides how the AI responds to user messages.
- Example: `"You are my loving girlfriend"`.

### 2. User Role
- Contains the actual user input or prompt.
- Example: `"I love you"`.

### 3. Temperature
Controls the randomness and creativity of AI responses.

| Temperature | Behaviour |
|---|---|
| 0.0 | More predictable |
| 0.5 | Less random |
| 1.0 | Balanced |
| 1.5 | More creative |
| 2.0 | Highly variable |

## 🔄 Workflow
1. Load API key from `.env`.
2. Create Groq client.
3. Define system instructions.
4. Provide user input.
5. Combine system and user messages.
6. Set temperature.
7. Generate and display AI response.

## 🎯 Learning Outcome
Learned how system messages control AI behaviour and how temperature influences the creativity and randomness of LLM responses.

**Next Topics:** Conversation History, Multiple Messages, and Prompt Engineering.