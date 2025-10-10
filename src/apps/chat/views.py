from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from home.context import usercontext
from .chain import summarize
from src.settings import BASE_DIR
from .forms import UploadFileForm


@login_required
def summarize_text(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "conversation",
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

    return render(request, "chat.html", context)
