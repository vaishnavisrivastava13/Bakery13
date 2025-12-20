from django.db import models

class Beverage(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='beverages/')
    description = models.TextField(blank=True)
    rating = models.FloatField(default=4.5)
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

