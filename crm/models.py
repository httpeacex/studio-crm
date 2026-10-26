from django.db import models
from django.conf import settings

class Client(models.Model):
    name = models.CharField('Имя', max_length=120)
    company = models.CharField('Компания', max_length=160, blank=True)
    email = models.EmailField('Email', blank=True)
    notes = models.TextField('Заметки', blank=True, max_length=10000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-pk']
        indexes = [models.Index(fields=['owner', 'archived'])]

    def __str__(self):
        return self.name
