from django.db import models

# Create your models here.

class Placements(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='placements/')

    def __str__(self):
        return self.name