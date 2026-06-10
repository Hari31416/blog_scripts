import os, re, subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
model = os.environ.get("LITELLM_MODEL", "gpt-oss-120b")

SYSTEM_PROMPT = """You are a helpful, agentic coding and system assistant. You have access to a bash shell on the user's machine. You can use it to write bash command or run python code to help you solve the user's request.

To run a bash command, output it inside a `<bash>` and `</bash>` tag, for example:
<bash>ls -la</bash>

To write and run a Python script dynamically, you can bash commands to create a script file and then run it, for example:
<bash>cat << 'EOF' > script.py
print("hello")
EOF
python3 script.py</bash>

Only write one command at a time. Explain your reasoning before calling any command. If you have completed the request, explain your findings/solution clearly.
"""
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]

prompt = input("Enter prompt: ")
messages.append({"role": "user", "content": prompt})

while True:
    response = client.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content or ""
    print(f"\nAgent:\n{content}")
    messages.append({"role": "assistant", "content": content})

    # Find and execute the first <bash> command if present
    match = re.search(r"<bash>(.*?)</bash>", content, re.DOTALL)
    if match:
        cmd = match.group(1).strip()
        print(f"\n[Running: {cmd}]")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = f"Exit code: {result.returncode}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
        messages.append({"role": "user", "content": output})
    else:
        # Prompt user for their next command/response
        user_input = input("\nYou (type 'exit' to quit): ").strip()
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        messages.append({"role": "user", "content": user_input})
