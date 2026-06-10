import asyncio
import os
import re
from dotenv import load_dotenv
from openai import AsyncOpenAI
from microsandbox import Sandbox

load_dotenv()

SYSTEM_PROMPT = """You are a helpful, agentic coding and system assistant.
You have access to a secure, isolated bash shell inside a sandbox VM. You can use it to write bash command or run python code to help you solve the user's request.
To run a bash command, output it inside a `<bash>` and `</bash>` tag, for example:
<bash>ls -la</bash>

To write and run a Python script dynamically, you can use bash commands to create a script file and then run it, for example:
<bash>cat << 'EOF' > script.py
print("hello")
EOF
python3 script.py</bash>

Only write one command at a time. Explain your reasoning before calling any command. If you have completed the request, explain your findings/solution clearly.
"""
async def main() -> None:
    # Initialize AsyncOpenAI client with environment variables
    client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    model = os.environ.get("LITELLM_MODEL", "gpt-oss-120b")

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    prompt = input("Enter prompt: ")
    messages.append({"role": "user", "content": prompt})

    # Create secure microVM sandbox using python image
    print("Creating secure microVM sandbox...")
    async with await Sandbox.create(
        "agent-sandbox",
        image="python",
        replace=True,
    ) as sb:
        print("Sandbox created successfully. Agent loop starting...")

        while True:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
            )
            content = response.choices[0].message.content or ""
            print(f"\nAgent:\n{content}")
            messages.append({"role": "assistant", "content": content})

            # Find and execute the first <bash> command if present
            match = re.search(r"<bash>(.*?)</bash>", content, re.DOTALL)
            if match:
                cmd = match.group(1).strip()
                print(f"\n[Running in Sandbox: {cmd}]")
                result = await sb.shell(cmd)
                output = f"Exit code: {result.exit_code}\nStdout:\n{result.stdout_text}\nStderr:\n{result.stderr_text}"
                messages.append({"role": "user", "content": output})
            else:
                # Prompt user for their next command/response
                user_input = input("\nYou (type 'exit' to quit): ").strip()
                if user_input.lower() in ["exit", "quit", "q"]:
                    break
                messages.append({"role": "user", "content": user_input})


if __name__ == "__main__":
    asyncio.run(main())
