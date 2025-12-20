from django.db import models

class Cupcake(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    rating = models.FloatField(default=4.5)
    description = models.TextField(blank=True,default="")
    is_best_seller = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cakes/')


    def __str__(self):
        return self.name