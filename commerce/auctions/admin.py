from django.contrib import admin
from .models import User, Auction, Watchlist, Bid, Comment, Image
from mptt.admin import MPTTModelAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bid)

admin.site.register(Image)

admin.site.register(Comment, MPTTModelAdmin)

