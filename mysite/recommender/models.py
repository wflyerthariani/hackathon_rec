from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_image = models.CharField(max_length=200)
    
class Store(models.Model):
    store_name = models.CharField(max_length=200)
    store_items = models.ManyToManyField(Item)

class Review(models.Model):
    review_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=10000)
