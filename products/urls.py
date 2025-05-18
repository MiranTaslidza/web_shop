from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoriesViewSet.as_view(), name='categories-list'),
    path('categories/<int:pk>/', views.CategoriesDetailView.as_view(), name='categories-detail'),

    # Subcategories
    path('subcategories/', views.SubCategoriesViewSet.as_view(), name='subcategories-list'),
    path('subcategories/<int:pk>/', views.SubCategoriesDetailView.as_view(), name='subcategories-detail'),

    # Products
    path('products/', views.ProductsViewSet.as_view(), name='products-list'),
    path('products/<int:pk>/', views.ProductsDetailView.as_view(), name='products-detail'),
    path('upload-product-image/', views.ProductImageUploadView.as_view(), name='upload-product-image'),
]