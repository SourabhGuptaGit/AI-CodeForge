# AI-CodeForge: Your AI Coding Sidekick\!

Hey there\! Welcome to **AI-CodeForge**—a super cool project that shows off how large language models (LLMs) can actually become self-correcting coders\! This thing is built with the **Gemini SDK**, and it uses an awesome feature called **function calling** to take control of a little sandboxed file system. Seriously, this agent can look around, read code, write new files, and even run scripts, all while logging every single decision it makes. Think of it as your new go-to for checking out automated debugging or complex AI tool interactions\!

## 🧠 Wait, How's It Work?

It's pretty simple, actually\! The agent just runs in a continuous loop, sending the entire conversation history back to the Gemini model in every step.

1.  **You Start It:** You send in a coding request (that's the `user` turn).

2.  **AI Plans:** Gemini gets the message and figures out what's next.

      * Need to peek at a file? It makes a **Function Call** (`model`).

      * Done with the job? It sends a **Final Text Response** (`model`).

3.  **Tools Execute:** The app jumps in, takes the function call (like "read file"), and runs the code.

4.  **AI Gets Results:** The function's output (like the file content) is packaged as a **Tool Response** (`tool`) and sent right back into the chat history.

5.  **Loop Continues\!** The AI sees the results and starts planning its next move.

## ✨ The Agent's Cool Toolkit

Everything this agent does is strictly confined to the working directory set in `config.py` (which is `calculator/` by default).

| Tool Name | Purpose | What It Does | Key Info |
| :--- | :--- | :--- | :--- |
| `get_files_info` | **File Scout** | It lists files and folders so the agent knows what's around. | Needs a `directory` (optional) |
| `get_file_content` | **File Reader** | Grabs the text inside any file. Heads up: it only reads the first 10,000 characters\! | Needs the `file_path` |
| `write_file` | **Code Writer** | Creates a new file or overwrites an existing one. It even makes folders if they don't exist\! | Needs `file_path` and the `content` |
| `run_python_file` | **Script Runner** | Executes a Python script and grabs whatever gets printed (`stdout`/`stderr`). | Needs the `file_path` |

## 🚀 Ready to Get Started?

Awesome\! Here's what you need to get this thing running.

### Prerequisites

  * You'll need Python 3.9 or newer (Recommended 3.12 or above).
  * You'll also need a Gemini API Key.

### 1\. Installation

Time to clone the repo and grab those libraries:

**Windows:**
```bash
git clone https://github.com/SourabhGuptaGit/AI-CodeForge.git
cd AI-CodeForge
python -m venv .venv
.venv/bin/activate
pip install requirements.txt
```
**Linux/Mac:**
```bash
git clone https://github.com/SourabhGuptaGit/AI-CodeForge.git
cd AI-CodeForge
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requirements.txt
```

### 2\. Environment Setup

Gotta keep that API key safe\! Create a file called `.env` in the main folder:

```text
# .env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 3\. Usage

Run the agent from your terminal, just put your whole request in quotes. Use the `--verbose` flag to see all the action\!

```bash
python main.py "Your coding request goes here" --verbose
```

## 🔎 Seeing the Magic Happen (Examples\!)

If you run it with `--verbose`, you get a super clear log of the AI's "brain" at work\!

### Example: Finding a Bug

**User Prompt:** `"Find the main calculator logic file, read its content, and then run tests.py."`

| Role | Log Output (Simulated) | Purpose |
| :--- | :--- | :--- |
| **User** | `User: "Find the main calculator logic file, read its content, and then run tests.py."` | Kicks off the task. |
| **Model Action** | `Model Action: Calling functions: get_files_info` | "Okay, first I need to see the file list." |
| **Tool Result** | `Tool Result: Successfully ran get_files_info. Result length: 350 chars.` | "Got it—files are: main.py, tests.py, and pkg/." |
| **Model Action** | `Model Action: Calling functions: get_file_content` | "Now I'll read pkg/calculator.py to check out the logic." |
| **Tool Result** | `Tool Result: Successfully ran get_file_content. Result length: 580 chars.` | "Here are the calculator's file contents." |
| **Model Action** | `Model Action: Calling functions: run_python_file` | "Time to run the tests.py script\!" |
| **Tool Result** | `Tool Result: Successfully ran run_python_file. Result length: 120 chars.` | "Tests results are in: 3 failed, 1 passed." |
| **Model Final Response** | `Model Final Response: I've checked the files, reviewed the code, and found 3 test failures! I'm ready to figure out the fix.` | Final answer\! |

## 📋 Keeping Tabs (Logging)

Transparency is key, right? The **AI-CodeForge** tracks everything using its neat little `logger.py` utility.

### Centralized Logging

All conversation moves, calls, and system messages are logged in two spots at the same time:

1.  **Terminal:** Shows you what's happening live.

2.  **`Agent.log`:** A saved file that archives the full history of every session. Super handy for checking later\!

### Token Tracking

We track API usage so you don't get surprised\! You'll see this logged for every turn:

```json
--- Turn 2 Token Usage ---:
{
    "prompt_tokens": 583,
    "response_tokens": 76
}
```

This helps you keep an eye on how big the conversation history is getting.

### Smart Error Handling

If the agent tries to do something impossible (like reading a file that doesn't exist), the app grabs the error and sends it *back* to the AI. This lets the model realize its mistake and **self-correct**—like "Whoops, that file wasn't there\! Let me try listing the directory first." Pretty smart\!

```
```