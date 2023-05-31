from django.db import models

# Create your models here.


class URL(models.Model):
    url = models.CharField(max_length=2048)

    def __str__(self):
        return self.url
