from django.contrib.auth.models import AbstractUser
from django.db import models
import PIL.Image
from PIL import ImageOps
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/profile/")



class Auction(models.Model):

    CATEGORY_CHOICES = (
        ('accessories','Accessories'),
        ('art','Art'),
        ('bags', 'Bags'),
        ('books', 'Books'),
        ('cameras','Cameras'),
        ('cell phone accessories','Cell Phone Accessories'),
        ('cell phones','Cell Phones'),
        ('clothes','Clothes'),
        ('computers','Computers'),
        ('cosmetics','Cosmetics'),
        ('jewelry','Jewelry'),
        ('musical instruments','Musical Instruments'),
        ('sporting goods','Sporting Goods'),
        ('shoes','Shoes'),
        ('toys','Toys'),
        ('watches','Watches'),
        ('other','Other'),
    )

    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    starting_bid = models.IntegerField(blank=False)
    product_category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, null=True)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", blank=True, null=True)
    highest_bid = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    active = models.BooleanField(default=True)
    date_closed = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.product_name


class Watchlist(models.Model):
    watchlist_item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_item")
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_user")

    def __str__(self):
        return self.watchlist_item.product_name


class Bid(models.Model):
    auction_biding = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bid")
    new_bid = models.CharField(blank=True, null=True, max_length=100)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_bidder", blank=True, null=True)

    def __str__(self):
        return f"{self.auction_biding.product_name}: ${self.new_bid}"


class Comment(MPTTModel):
    product = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    body = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_likes", blank=True, null=True,)
    dislikes = models.ManyToManyField(User, related_name="comment_dislikes", blank=True, null=True,)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")


    class MPTTMeta:
        order_insertion_by = ['date_added']

    def __str__(self):
        return f"{self.name} commented {self.product}: {self.body}"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()



class Image(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_images")
    image = models.ImageField(default='default.jpg', blank=True, null=True, upload_to="images/")


