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


class State(MessagesState):
    history: str


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


# ----------------------------------------------------------------


def call_model(state: State, conversation_summary: str) -> dict:
    """
    Call llm to generate a response based on current state and conversation summary.
    Args :
        state (State): current state of conversation, including history and messages.
        conversation_summary (str): summary of conversation so far
    Returns:
        dict: dictionary containing the generated response message.
    """

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["API_MODEL"],
        temperature=0.2,
    )

    # if history exists, add history in system message :
    history = state.get("history")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        system_message = SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # return is a list, will be added to existing list
    return {"messages": [response]}


def summarize_history(state: State) -> dict:
    """
    Summarize history, in case of history is too long
    """
    llm_summarize = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["API_MODEL"],
        temperature=0.2,
    )

    history = state.get("history", "")
    if history:
        history_message = f"Summary of conversation earlier: {history}"
    else:
        history_message = "No conversation history available"
    message = state["messages"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)
    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"history": response.content, "message": delete_message}


def should_continue(state: State) -> Literal["summarize_history", END]:
    message = state["messages"]
    if len(message) > 6:
        return "summarize_history"
    return END


def print_update(update: dict) -> None:
    """
    Display conversation
    Args:
        update (dict): _description_
    """
    for k, v in update.items():
        for m in v["messages"]:
            m.pretty_print()
        if "history" in v:
            print(v["history"])
