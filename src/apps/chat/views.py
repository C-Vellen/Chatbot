import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import StreamingHttpResponse

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .chain import (
    State,
    summarize,
    generate_response,
    call_model,
    summarize_history,
    should_continue,
    print_update,
)

from src.settings import BASE_DIR
from home.context import usercontext
from .forms import UploadFileForm

chain = None


@login_required
def summarize_text(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "résumé",
            "msg": "Hello ! Entrez un fichier à résumer :",
        }
    )

    upload = False
    text = ""
    summary = ""

    if request.method == "POST":
        upload = True
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            if file.content_type == "text/plain":
                content = file.read()
                text = content.decode("utf-8")

                summary = summarize(text)
                # summary = "*** ici le résumé ***"

            else:
                text = "Error : only text files are supported"
                summary = ""

    else:
        form = UploadFileForm()

    context.update(
        {
            "text": text,
            "summary": summary,
            "form": form,
            "upload": upload,
        }
    )

    return render(request, "chat/summarize.html", context)


# ----------------------------------------------------------------------------------------------


@login_required
def chat(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "conversation",
            "msg": "Hello ! Voulez-vous démarrer une nouvelle conversation ?",
        }
    )
    return render(request, "chat/chat.html", context)


@login_required
@api_view(["GET", "POST"])
def answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data["prompt"]
        response = StreamingHttpResponse(
            generate_response(prompt), status=200, content_type="text/plain"
        )
        return response
    else:
        return Response({"Error": "not POST"})


# ----------------------------------------------------------------------------------------------


@login_required
def talk(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "conversation",
            "msg": "Hello ! Entrez un fichier à résumer et ensuite nous en discuterons !",
        }
    )

    upload = False
    text = ""
    filename = ""
    summary = ""

    if request.method == "POST":
        upload = True
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            filename = file.name
            print("########### > ", filename)

            s = initialize(file)
            print("=> ", s)
            summary = s["summary"]
            # summary = "*** ici le résumé ***"

    else:
        form = UploadFileForm()

    context.update(
        {
            "filename": filename,
            "summary": summary,
            "form": form,
            "upload": upload,
        }
    )

    return render(request, "chat/talk.html", context)


def initialize(file):

    global chain

    # test fichier textuel (copié/collé fonction précédente)
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    # content = await file.read()
    content = file.read()
    text = content.decode("utf-8")
    print("...........", text)

    workflow = StateGraph(State)
    workflow.add_node(
        "conversation",
        lambda input: call_model(state=input, conversation_summary=summary),
    )
    workflow.add_node(summarize_history)
    workflow.add_edge(START, "conversation")
    workflow.add_conditional_edges(
        "conversation",
        should_continue,
    )
    workflow.add_edge("summarize_history", END)
    memory = MemorySaver()
    chain = workflow.compile(checkpointer=memory)

    summary = summarize(text)
    return {"summary": summary}


def generate_stream(input_message, config, chain):
    for event in chain.stream(
        {"messages": [input_message]}, config, stream_mode="updates"
    ):

        yield event["conversation"]["messages"][0].content


@login_required
@api_view(["GET", "POST"])
def update(request):

    config = {"configurable": {"thread_id": "4"}}
    data = json.loads(request.body)
    prompt = data["prompt"]
    input_message = HumanMessage(content=prompt)

    print(">> chain: ", chain)

    response = StreamingHttpResponse(
        generate_stream(input_message, config, chain),
        status=200,
        content_type="text/plain",
    )

    return response
