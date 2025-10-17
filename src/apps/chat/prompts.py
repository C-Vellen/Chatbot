PROMPT_SUMMARIZE = """Resume le texte en un maximum de 5 phrases :
    ###
    TEXT: {text}
    """

SYSTEM_PROMPT = """Ce qui suit est une conversation amicale entre un humain et une IA. L'IA est bavarde et fournit de nombreux détails précis issus de son contexte de CONVERSATION.
Si l'IA ne connaît pas la réponse à une question, elle dit honnêtement qu'elle ne la connaît pas.
    ###
    CONVERSATION: {conversation}
"""
