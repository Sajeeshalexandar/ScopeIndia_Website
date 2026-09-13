from django.db import models

# Create your models here.

class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

class Reviews(models.Model):
    name = models.CharField(max_length=30)
    review = models.TextField()

    def __str__(self):
        return self.name
