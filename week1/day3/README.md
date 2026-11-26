# Multiple Prompts and Token Usage with Groq API

## 1. Overview

This program sends multiple prompts to an LLM using the Groq API. It processes each prompt one by one using a `for` loop and displays token usage and the finish reason for every response.

## 2. Creating Multiple Prompts

```
prompt1 = "Hi"
prompt2 = "Explain array in dsa"
prompt3 = "Write 1000 essay on love marriage"

prompts = [prompt1, prompt2, prompt3]
```

- Three different prompts are created.
- All prompts are stored inside a list called `prompts`.
- This allows us to process multiple inputs without writing separate API requests.

## 3. Using a For Loop

```
for prompt in prompts:
```

- The loop iterates through the prompts list.
- In each iteration, one prompt is assigned to the variable `prompt`.
- The same API request is executed for every prompt.

**Example:**

| Iteration | Current Prompt                    |
| --------- | --------------------------------- |
| 1         | Hi                                |
| 2         | Explain array in dsa              |
| 3         | Write 1000 essay on love marriage |

## 4. Creating Messages

```
message = {
    "role": "user",
    "content": prompt
}
messages = [message]
```

- `role`: Specifies that the message comes from the user.
- `content`: Contains the current prompt.
- `messages`: Stores the message in a list format required by the chat API.

## 5. Sending the API Request

```
Response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=2000
)
```

This sends the current prompt to the selected LLM.

**Understanding `max_tokens=2000`:**

- Sets the maximum number of tokens the model can generate in its response.
- It is a limit, not a guarantee that the model will generate 2,000 tokens.
- The actual response length depends on the prompt and model output.

## 6. Understanding Token Usage

```
usage = Response.usage
```

This extracts token usage information from the API response.

| Property                  | Meaning                                    |
| ------------------------- | ------------------------------------------ |
| `usage.prompt_tokens`     | Number of tokens used in the input prompt  |
| `usage.completion_tokens` | Number of tokens generated in the response |
| `usage.total_tokens`      | Total tokens used for input and output     |

**Formula:**

`Total Tokens = Prompt Tokens + Completion Tokens`

**Example:**

If the prompt uses 10 tokens and the response generates 100 tokens:

- Prompt Tokens = 10
- Completion Tokens = 100
- Total Tokens = 110

Token count depends on the model's tokenizer. A token can represent a word, part of a word, or punctuation.

## 7. Understanding Finish Reason

```
Response.choices[0].finish_reason
```

This tells us why the model stopped generating its response.

| Finish Reason | Meaning                                           |
| ------------- | ------------------------------------------------- |
| `stop`        | Response completed normally                       |
| `length`      | Generation stopped after reaching the token limit |
| `tool_calls`  | Model requested a tool call                       |

## 8. Complete Workflow

1. Store multiple prompts in a list.
2. Use a `for` loop to access each prompt.
3. Convert the current prompt into a message.
4. Send the message to the LLM through the API.
5. Set `max_tokens` to control the maximum generated output.
6. Extract token usage from the response.
7. Display input tokens, output tokens, total tokens, and finish reason.
8. Repeat until all prompts are processed.

## 9. Key Learning

- How to process multiple prompts using a `for` loop.
- How to send individual prompts to an LLM.
- How to control response length using `max_tokens`.
- How to monitor input and output token consumption.
- How to identify why an LLM response stopped using `finish_reason`.

Add the complete loop codeShow the generated response output