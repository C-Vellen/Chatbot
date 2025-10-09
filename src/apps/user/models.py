from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass

    def __str__(self):
        return "{} {} [{}]".format(self.last_name, self.first_name, self.username)


