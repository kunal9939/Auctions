from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, User, Listing, Bid, Comment, Watchlist


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)