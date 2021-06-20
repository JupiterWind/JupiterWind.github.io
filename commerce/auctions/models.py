from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    pass

class Auction(models.Model):
    CATEGORY_CHOICES = (
        ('AL', 'None'),
        ('FS', 'Fashion'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HO', 'Home'),
        ('ET', 'etc')
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, blank="True")
    current_bid = models.IntegerField()
    state = models.CharField(max_length=6, default="active")
    created_date = models.DateField(auto_now=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator"
    )

class AuctionForm(forms.Form):
    CATEGORY_CHOICES = (
        ('AL', 'None'),
        ('FS', 'Fashion'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HO', 'Home'),
        ('ET', 'etc')
    )
    title = forms.CharField(label='title', max_length=200)
    description = forms.CharField(label='description',widget=forms.Textarea)
    image_url = forms.CharField(label="Image URL",required=False)
    category = forms.ChoiceField(label="category",required=False,choices=CATEGORY_CHOICES)
    starting_bid = forms.IntegerField(label="Staring Bid")


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    ending_bid = models.IntegerField(default=0)
    number_of_bid = models.IntegerField(default=0)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder", null=True
    )
    bidded_date = models.DateField(auto_now=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="winner",null=True
    )

class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name="commented_auction")
    comment = models.CharField(max_length=300)
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    modified_date = models.DateField(auto_now_add=True)

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=300)

class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    registered_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} {self.auction_id} {self.registered_date}"
