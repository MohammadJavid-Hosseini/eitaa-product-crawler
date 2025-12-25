def clean_text(text: str) -> str:
    # HACK: later it turns into a proper parsing function
    if not text:
        return ""

    return text.strip()
