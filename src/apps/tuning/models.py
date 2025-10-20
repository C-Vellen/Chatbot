from django.db import models

VERBOSITY_LIST = (("Low", "Low"), ("Medium", "Medium"), ("High", "High"))
TARGET_LIST = (("SUMMARIZE", "SUMMARIZE"), ("SYSTEM", "SYSTEM"))


class LLMModel(models.Model):
    """
    LLM Model features
    """

    LLM = models.CharField(max_length=200, default="")
    temperature = models.FloatField()
    verbosity = models.CharField(max_length=20, choices=VERBOSITY_LIST)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Modèle de LLM"

    @classmethod
    def get_active_model(cls):
        llm_model, created = cls.objects.get_or_create(
            active=True,
            defaults={"model": "gpt-5-nano", "temperature": 0.2, "verbosity": "Medium"},
        )
        if created:
            print("new llm_model created")
        return llm_model

    @classmethod
    def get_active_model_params(cls):
        llm_model = cls.get_active_model()
        return llm_model.LLM, llm_model.temperature, llm_model.verbosity

    def __str__(self):
        return f"{self.LLM} | {self.id}"


class Prompt(models.Model):
    """_
    Prompt features
    """

    name = models.CharField(max_length=50, default="")
    target = models.CharField(max_length=20, choices=TARGET_LIST)
    prompt_text = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "prompt"

    @classmethod
    def get_active_prompt(cls, target):
        prompt, created = cls.objects.get_or_create(
            active=True,
            target=target,
            defaults={"name": f"empty-{target.lower()}", "prompt_text": ""},
        )
        if created:
            print(f"new empty prompt-{target.lower()} created")
        return prompt

    @classmethod
    def get_active_prompt_text(cls, target):
        prompt = cls.get_active_prompt(target=target)
        return f"{prompt.prompt_text} ### TEXT:" + "{text}"

    @classmethod
    def get_prompt(cls, target):
        try:
            return cls.objects.filter(target=target)
        except cls.DoesNotExist:
            return ""

    def __str__(self):
        return f"{self.name}-{self.target}"
