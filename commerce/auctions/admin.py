from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Auction,Comment,Bid

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id","title","description","image_url","current_bid", "state", "creator", "category")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","comment","auction","commenter")

class BidAdmin(admin.ModelAdmin):
    list_display = ("starting_bid","current_bid","ending_bid","number_of_bid","auction","bidder","winner")

admin.site.register(User, UserAdmin)
admin.site.register(Auction,AuctionAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Bid,BidAdmin)
