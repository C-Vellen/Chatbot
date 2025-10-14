# video 1-Mise en place d'une architecture de projet
PROMPT_SUMMARIZE = """Resume le texte en un maximum de 5 phrases :
    ###
    TEXT: {text}
    """

# video 3-Création de la fonction résumé
SYSTEM_PROMPT = """The following is a frienly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its CONVERSATION context.
    If the AI does not know the answer of a question, it truthfully says it does not know.
    CONVERSATION;
    ###
    {conversation}
"""
