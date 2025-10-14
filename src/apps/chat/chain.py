import os
from typing import Literal
from dotenv import load_dotenv

from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import MessagesState, END

from .prompts import PROMPT_SUMMARIZE, SYSTEM_PROMPT


def summarize(conversation: str) -> str:
    """Summarize a conversation (text) through a langchain pipeline :
    apply a prompt (which tell to summarize) then a llm (ChatOepnAI from langchain)

    Args:
        conversation (): a text to summarize
    Returns:
        str: the summary
    """
    prompt_template = PROMPT_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["API_MODEL"],
        temperature=0.2,
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke(conversation)


client = OpenAI()


def generate_response(prompt: str) -> GeneratorExit:
    """return a generator of chunks of llm (OpenAI) response

    Args:
        prompt (str): the prompt

    Yields:
        GeneratorExit: stream of response
    """

    stream = client.chat.completions.create(
        model=os.environ["API_MODEL"],
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield (chunk.choices[0].delta.content)
