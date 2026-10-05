def chunk_text(text):
    chunks = []

    for chunk in text.split("\n\n"):
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

    return chunks

text = """
Python Java SQL Docker FastAPI
""" * 100

chunks = chunk_text(text)

