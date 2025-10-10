import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import MessagesState, END

from .prompts import PROMPT_SUMMARIZE, SYSTEM_PROMPT


def summarize(conversation: str) -> str:

    prompt_template = PROMPT_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["API_MODEL"],
        temperature=0.2,
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke(conversation)
