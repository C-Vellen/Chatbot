import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import StreamingHttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .chain import summarize, generate_response

from src.settings import BASE_DIR
from home.context import usercontext
from .forms import UploadFileForm

TOKEN_LIST = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.".split(
    " "
)


@login_required
def summarize_text(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "résumé",
            "msg": "Hello ! Entrez un fichier à résumer en anglais :",
        }
    )

    # print(str(BASE_DIR) + "/apps/chat/exemple.txt")
    # with open(str(BASE_DIR) + "/apps/chat/exemple.txt", "r") as file:
    # text = file.read()

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
