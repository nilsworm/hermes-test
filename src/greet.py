def greet(name=None):
    """Build a friendly greeting message.

    Args:
        name: The name to greet. Leading/trailing whitespace is trimmed.
            When omitted, empty, or whitespace-only, the greeting falls
            back to "there".

    Returns:
        A greeting in the form ``"Hello, <name>!"``.
    """
    trimmed = (name or "").strip()
    target = trimmed if trimmed else "there"
    return f"Hello, {target}!"
