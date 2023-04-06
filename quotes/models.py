from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


# Create your models here.
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, blank=False)
    born_date = models.CharField(max_length=100, blank=False)
    born_location = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'fullname'], name='author of username')
        ]

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    quote = models.TextField(null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'quote'], name='quote of username')
        ]

    def __str__(self):
        return self.quote