# filters.py
import django_filters
from .models import Products
class ProductFilter(django_filters.FilterSet):
    """
    Filter za proizvode koji omogućava filtriranje po kategoriji i podkategoriji.
    """
    class Meta:
        model = Products
        fields = {
            'category': ['exact'],
            'subcategory': ['exact'],
            'price': ['lt', 'gt', 'lte', 'gte'],
            'size': ['exact'],
        }