from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title
