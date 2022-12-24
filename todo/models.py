from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.urls import reverse


class Todo(models.Model):
    name = models.CharField(max_length=150)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('showtodo', kwargs={'todo_id': self.pk})

    class Meta:
        ordering = ['-created_at']