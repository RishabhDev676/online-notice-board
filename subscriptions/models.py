from django.db import models
from notices.models import Category, Department


class EmailSubscription(models.Model):
    email = models.EmailField(unique=True)
    categories = models.ManyToManyField(Category, blank=True)
    departments = models.ManyToManyField(Department, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
