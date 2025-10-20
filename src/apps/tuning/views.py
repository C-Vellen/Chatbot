from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from home.context import usercontext
from chat.chain import MODEL_LIST

from .models import LLMModel, Prompt, VERBOSITY_LIST, TARGET_LIST
from .forms import LLMModelForm


@login_required
def model_tuning(request):
    context = usercontext(request)
    verbosity_list = [v[1] for v in VERBOSITY_LIST]
    target_list = [t[1] for t in TARGET_LIST]

    llm_model = LLMModel.get_active_model()
    model = llm_model.LLM
    temperature = llm_model.temperature
    verbosity = llm_model.verbosity

    selected_prompts = {t: Prompt.get_active_prompt(t) for t in target_list}
    all_prompts = Prompt.objects.all()

    # print("==============================================")
    # print("### Initial: ", model, temperature, verbosity)
    # for p in all_prompts:
    #     print(f"prompt: {p.name} | {p.target} | {p.active}")
    # print("target_list: ", target_list)
    # print(" ### Initial; ", selected_prompts, all_prompts)

    if request.method == "POST":

        # print(
        #     f"### Post: {request.POST["LLM"]} | {request.POST["temperature"]} | {request.POST["verbosity"]} | {request.POST["prompt-SUMMARIZE"]} | {request.POST["prompt-SYSTEM"]} "
        # )

        form = LLMModelForm(request.POST, instance=llm_model)
        form.save()

        for prompt in Prompt.objects.all():
            prompt.active = False
            prompt.save()

        for target in target_list:
            selected_prompt = Prompt.objects.get(id=request.POST[f"prompt-{target}"])
            selected_prompt.active = True
            selected_prompt.save()

        context.update({"titre_onglet": "Chatbot"})
        return render(request, "home/index.html", context)

    context.update(
        {
            "titre_onglet": "Tuning model",
            "msg": "Choisissez le model et les prompts :",
            "model": model,
            "model_list": MODEL_LIST,
            "temperature": temperature,
            "verbosity": verbosity,
            "verbosity_list": verbosity_list,
            "target_list": target_list,
            "selected_prompts": selected_prompts,
            "all_prompts": all_prompts,
        }
    )

    return render(request, "tuning/model_tuning.html", context)


@login_required
def prompt_tuning(request):
    context = usercontext(request)
    context.update({"msg": "Créez ou modifiez des prompts :"})
    return render(request, "tuning/prompt_tuning.html", context)
