from django.db import models


class Author(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    year_published = models.CharField(max_length=10)
    review = models.PositiveIntegerField()

    def __str__(self):
        return self.title
