MOTS_CLES_IA = r"\b(?:AI|LLMs?|GPT|ChatGPT|OpenAI|Claude|Anthropic|Gemini|Llama|Mistral)\b"


def parle_d_ia(titres):
    return titres.str.contains(MOTS_CLES_IA, regex=True)
