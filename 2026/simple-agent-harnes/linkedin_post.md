# LinkedIn Post Draft

How many lines of Python does it take to build a functional, bash-executing AI agent?

Just 50 lines. 🚀

I put together a minimal agent harness to show how simple the core concepts of agentic tool-use really are:

1. **System Prompt**: Instruct the LLM to wrap shell commands in custom tags, e.g., `<bash>ls -la</bash>`.
2. **LLM Loop**: Call the OpenAI API, parse out the command using a simple regex, and run it via `subprocess`.
3. **Execution & Feedback**: Execute the command locally, capture the stdout/stderr, and feed the output back to the LLM to let it decide the next step.

While frameworks like LangChain or LlamaIndex provide rich abstractions, building a harness from scratch using standard libraries (`re`, `subprocess`, `openai`) is a fantastic way to understand what's happening under the hood. Of course, these frameworks do not use this simple strcuture, instead, they rely on tool calling and structured outputs. I have used this simple structue just to show how an agentic system works.

⚠️ **Important Note**: This is strictly for educational purposes! Running arbitrary LLM-generated bash commands on your host system is not secure and shouldn't be run in production without proper sandboxing.


🔗 https://gist.github.com/Hari31416/2b1a2ee1a3d35c634a8281505f5814e6

#AIAgents #Python #OpenAI #SoftwareEngineering #GenerativeAI #Coding


Adding a sandbox for you agent generated code to run is actually very easy with tools like microsandbox. See this other gist where I have used microsandbox to execute bash commands securely and in isolation. https://gist.github.com/Hari31416/a50aa19b9355fd25aaddfcec274c5ec8