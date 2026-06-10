import os, re, subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
model = os.environ.get("LITELLM_MODEL", "gpt-oss-120b")

SYSTEM_PROMPT = """You are a helpful, agentic coding and system assistant.
You have access to a bash shell on the user's machine.
To run a bash command, output it inside a `<bash>` and `</bash>` tag, for example:
<bash>ls -la</bash>

Only execute one command at a time. Explain your reasoning before calling any command. If you have completed the request, explain your findings/solution clearly and wait for further instructions.
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
    response = client.chat.completions.create(model=model, messages=messages)  # type: ignore
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
