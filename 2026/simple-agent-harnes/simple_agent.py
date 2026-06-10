#!/usr/bin/env python3
"""
Simple agent harness that uses the OpenAI API to run tasks.
Supports executing bash commands dynamically with user confirmation.
"""

import argparse
import logging
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI


# Custom formatter for clean interactive CLI logging
class CleanFormatter(logging.Formatter):
    """
    Custom formatter that prints INFO messages without metadata prefixes,
    while adding level names to warnings, errors, and debug messages.
    """

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.INFO:
            return record.getMessage()
        return f"[{record.levelname}] {record.getMessage()}"


# Set up logging
logger = logging.getLogger("SimpleAgent")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CleanFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Load environment variables (local first, then parent search)
load_dotenv()

SYSTEM_PROMPT = """You are a helpful, agentic coding and system assistant.
You have access to a bash shell on the user's machine.
To run a bash command, output it inside a `<bash>` and `</bash>` tag, for example:
<bash>ls -la</bash>

Only execute one command at a time. After executing a command, you must wait for the output to be provided to you.
Explain your reasoning before calling any command.
If you have completed the request, explain your findings/solution clearly and wait for further instructions.
"""


def parse_bash_command(text: str) -> Optional[str]:
    """
    Parses a string for the first occurrence of a <bash>...</bash> block.
    Returns the command inside the block if found, otherwise None.
    """
    match = re.search(r"<bash>(.*?)</bash>", text, re.DOTALL)
    return match.group(1).strip() if match else None


def execute_bash(command: str) -> str:
    """
    Executes a bash command and returns a formatted string containing exit code, stdout, and stderr.
    """
    try:
        logger.info(f"\n[Executing Bash Command]: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output_parts: List[str] = [f"Exit code: {result.returncode}"]
        if result.stdout:
            output_parts.append(f"Stdout:\n{result.stdout.strip()}")
        if result.stderr:
            output_parts.append(f"Stderr:\n{result.stderr.strip()}")
        if not result.stdout and not result.stderr:
            output_parts.append("(No output)")

        return "\n".join(output_parts)
    except subprocess.TimeoutExpired:
        logger.warning("Command execution timed out.")
        return "Error: Command timed out after 120 seconds."
    except Exception as e:
        logger.error(f"Error occurred during execution: {e}")
        return f"Error executing command: {str(e)}"


def run_agent_loop(
    client: OpenAI, model: str, initial_prompt: str, auto_approve: bool
) -> None:
    """
    Main conversational agent loop.
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": initial_prompt},
    ]

    while True:
        try:
            logger.info("\nCalling LLM...")
            response = client.chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
            )
        except Exception as e:
            logger.error(f"Failed to call OpenAI API: {e}")
            sys.exit(1)

        assistant_content = response.choices[0].message.content
        if not assistant_content:
            logger.warning("Received empty response from the assistant.")
            assistant_content = ""

        logger.info(f"\nAgent:\n{assistant_content}")
        messages.append({"role": "assistant", "content": assistant_content})

        # Parse for bash tags
        command = parse_bash_command(assistant_content)
        if command:
            # Request confirmation
            approved = auto_approve
            if not approved:
                try:
                    confirm = input("\n[Confirm] Run command? [y/N]: ").strip().lower()
                    approved = confirm in ("y", "yes")
                except KeyboardInterrupt:
                    logger.info("\nAborted by user.")
                    sys.exit(0)

            if approved:
                execution_result = execute_bash(command)
                logger.info(f"\n[Command Output]:\n{execution_result}")
                messages.append(
                    {
                        "role": "user",
                        "content": f"[Command Output]:\n{execution_result}",
                    }
                )
            else:
                logger.info("\nExecution denied by user.")
                messages.append(
                    {
                        "role": "user",
                        "content": "Command execution was denied/aborted by the user.",
                    }
                )
        else:
            # No commands to execute, get next user instruction
            try:
                user_reply = input("\nYou (type 'exit' to quit): ").strip()
            except KeyboardInterrupt:
                logger.info("\nExiting.")
                sys.exit(0)

            if not user_reply:
                continue
            if user_reply.lower() in ("exit", "quit"):
                logger.info("Exiting agent loop.")
                break

            messages.append({"role": "user", "content": user_reply})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple Agent Harness with Bash Execution"
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The initial goal/prompt for the agent. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="gpt_oss_120b",
        help="OpenAI Chat Completion model name (default: gpt_oss_120b)",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Automatically execute all commands without asking for permission",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug level logging",
    )

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")

    if not api_key:
        logger.error(
            "Error: OPENAI_API_KEY environment variable not found in .env or environment."
        )
        sys.exit(1)

    logger.info(f"Initializing OpenAI client (Model: {args.model})...")
    if base_url:
        logger.info(f"Using custom Base URL: {base_url}")

    client = OpenAI(api_key=api_key, base_url=base_url)

    initial_prompt = args.prompt
    if not initial_prompt:
        try:
            initial_prompt = input("Enter initial task: ").strip()
        except KeyboardInterrupt:
            logger.info("\nExiting.")
            sys.exit(0)

    if not initial_prompt:
        logger.error("No prompt provided. Exiting.")
        sys.exit(1)

    run_agent_loop(
        client=client,
        model=args.model,
        initial_prompt=initial_prompt,
        auto_approve=args.yes,
    )


if __name__ == "__main__":
    main()
