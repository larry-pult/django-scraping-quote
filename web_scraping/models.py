from django.db import models


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.tag


class Author(models.Model):
    author = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.author


class Quote(models.Model):
    quote = models.CharField(max_length=2000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()

    def __str__(self):
        return self.quote
