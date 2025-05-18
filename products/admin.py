from django.contrib import admin
from .models import Categories, SubCategories, Products, ProductImage, Review


admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(Review)

# Register your models here.
