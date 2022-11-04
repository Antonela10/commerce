from .models import Auction

def categories_list(request):
    categories = []
    all_categories = Auction.CATEGORY_CHOICES
    for category in all_categories:
        categories.append(category[0])
    return {
        "categories": categories
    }