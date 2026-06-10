"""
Tests for simple_agent.py
"""

from simple_agent import parse_bash_command, execute_bash


def test_parse_bash_command_valid() -> None:
    """Tests parsing of valid bash tags."""
    text = "Let me list files:\n<bash>ls -la</bash>\nDone."
    assert parse_bash_command(text) == "ls -la"


def test_parse_bash_command_no_tag() -> None:
    """Tests parsing when no tags are present."""
    text = "Hello, I cannot execute commands."
    assert parse_bash_command(text) is None


def test_parse_bash_command_multiline() -> None:
    """Tests parsing of multi-line bash commands."""
    text = "Let's run this script:\n<bash>\necho 'Hello'\necho 'World'\n</bash>"
    assert parse_bash_command(text) == "echo 'Hello'\necho 'World'"


def test_parse_bash_command_multiple_tags() -> None:
    """Tests that the first bash tag is extracted when multiple exist."""
    text = "First:\n<bash>echo 1</bash>\nSecond:\n<bash>echo 2</bash>"
    assert parse_bash_command(text) == "echo 1"


def test_execute_bash_success() -> None:
    """Tests successful execution of a safe, standard command."""
    output = execute_bash("echo 'Test Output'")
    assert "Exit code: 0" in output
    assert "Stdout:" in output
    assert "Test Output" in output


def test_execute_bash_failure() -> None:
    """Tests execution failure of a non-existent command."""
    output = execute_bash("nonexistentcommand12345")
    # In bash, command not found typically returns 127
    assert "Exit code: 127" in output or "Exit code: 1" in output or "Error" in output
