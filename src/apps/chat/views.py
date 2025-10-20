import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import StreamingHttpResponse

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from simple_yt_api import YouTubeAPI

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

from src.settings import CSRF_TRUSTED_ORIGINS
from home.context import usercontext
from .forms import UploadFileForm, UploadURL

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
    text = None
    summary = None

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
                summary

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
            "originURL": CSRF_TRUSTED_ORIGINS[0],
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
            "originURL": CSRF_TRUSTED_ORIGINS[0],
        }
    )

    upload = False
    filename = None
    summary = None

    if request.method == "POST":
        upload = True
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            filename = file.name
            if file.content_type != "text/plain":
                return {"error": "Only text files are supported"}
            content = file.read()
            text = content.decode("utf-8")
            s = initialize(text)
            summary = s["summary"]

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


def initialize(text):

    global chain

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


@login_required
def videotalk(request):

    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "conversation",
            "msg": "Entrez le lien d'une video Youtube, et ensuite nous pourrons en discuter !",
            "originURL": CSRF_TRUSTED_ORIGINS[0],
        }
    )

    upload = False
    url = ""
    video_has_transcript = False
    video_title = ""
    short_description = ""
    thumbnail_url = ""
    summary = ""

    if request.method == "POST":
        upload = True
        form = UploadURL(request.POST)
        if form.is_valid():

            url = request.POST["url"].split("&")[0]
            yt = YouTubeAPI()

            try:
                data, transcript = yt.get_video_data_and_transcript(
                    url=url,
                    language_code="fr",
                    as_dict=False,
                )
                transcript2 = yt.get_transcript(
                    url=url, language_code="fr", as_dict=True
                )
                video_has_transcript = True
                video_title = data["title"]
                short_description = data["short_description"]
                thumbnail_url = data["img_url"]
                s = initialize(transcript)
                summary = s["summary"]

            except TypeError:
                # except  NoTranscriptFound:
                pass

    else:
        form = UploadURL()

    context.update(
        {
            "video_has_transcript": video_has_transcript,
            "video_title": video_title,
            "short_description": short_description,
            "video_url": url,
            "thumbnail_url": thumbnail_url,
            "summary": summary,
            "form": form,
            "upload": upload,
        }
    )
    return render(request, "chat/videotalk.html", context)
