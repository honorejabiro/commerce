from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
class Category(models.Model):
    categoryname = models.CharField(max_length=600)

    def __str__(self):
        return self.categoryname
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bids')
    price = models.FloatField(default=0)


class Listing(models.Model):
    title = models.CharField(max_length=600)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=5000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name='listings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user') 
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='listing')
    user = models.ManyToManyField('User', null=True, blank=True, related_name='watchlist')


    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.user} commented {self.message}"

