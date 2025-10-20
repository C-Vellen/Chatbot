import os
from typing import Literal
from dotenv import load_dotenv

from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import MessagesState, END

from tuning.models import LLMModel, Prompt


client = OpenAI()
MODEL_LIST = [m.id for m in client.models.list().data]


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

    model, temperature, verbosity = LLMModel.get_active_model_params()
    SUMMARIZE_PROMPT = Prompt.get_active_prompt_text("SUMMARIZE")
    prompt_template = SUMMARIZE_PROMPT
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=model,
        temperature=temperature,
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke(conversation)


def generate_response(prompt: str) -> GeneratorExit:
    """return a generator of chunks of llm (OpenAI) response

    Args:
        prompt (str): the prompt

    Yields:
        GeneratorExit: stream of response
    """
    model, temperature, verbosity = LLMModel.get_active_model_params()
    stream = client.chat.completions.create(
        model=model,
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
    model, temperature, verbosity = LLMModel.get_active_model_params()
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=model,
        temperature=temperature,
    )

    # if history exists, add history in system message :
    history = state.get("history")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        SYSTEM_PROMPT = Prompt.get_active_prompt_text("SYSTEM")
        system_message = SYSTEM_PROMPT.format(text=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # return is a list, will be added to existing list
    return {"messages": [response]}


def summarize_history(state: State) -> dict:
    """
    Summarize history, in case of history is too long
    """

    model, temperature, verbosity = LLMModel.get_active_model_params()
    llm_summarize = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=model,
        temperature=temperature,
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
