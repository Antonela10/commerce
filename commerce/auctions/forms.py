from django import forms
from django.forms import ModelForm
from .models import Auction, Comment, User, Bid, Image



class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('product_name', 'product_category', 'starting_bid', 'description')

        labels = {
            'product_name':'Product Name',
            'product_category':'Category',
            'starting_bid':'Starting Bid',
            'description':'Product Description',
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Product Name', 'autocomplete': 'off'}),
            'product_category': forms.Select(attrs={'class':'form-control', 'placeholder':'Product Category', 'autocomplete': 'off'}),
            'starting_bid': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Starting Bid', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'autocomplete': 'off'}),
        }


class ImageForm(ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={"multiple":True}),
    )

    class Meta:
        model = Image
        fields = ('image',)



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )

        labels = {
            'body':'',
            }


        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Comment', 'rows':6, 'class':'comment_form'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('new_bid', )

        labels = {
            'new_bid':'',
            }

        widgets = {
            'new_bid': forms.TextInput(attrs={'class':'form-control', 'placeholder':'New Bid', 'autocomplete': 'off'}),
        }
