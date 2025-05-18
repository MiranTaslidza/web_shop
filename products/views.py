from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categories, SubCategories, Products, ProductImage, Review
from .serijalizers import CategoriesSerializer, SubCategoriesSerializer, ProductsSerializer



# categories
class CategoriesViewSet(APIView):
    def get(self, request):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class CategoriesDetailView(APIView):
    def get(self, request, pk):
        try:
            category = Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            return Response(status=404)
        serializer = CategoriesSerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            category = Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            return Response(status=404)
        serializer = CategoriesSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        try:
            category = Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            return Response(status=404)
        category.delete()
        return Response(status=204)

# subcategories
class SubCategoriesViewSet(APIView):
    def get(self, request):
        subcategories = SubCategories.objects.all()
        serializer = SubCategoriesSerializer(subcategories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = SubCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class SubCategoriesDetailView(APIView):
    def get(self, request, pk):
        try:
            subcategory = SubCategories.objects.get(pk=pk)
        except SubCategories.DoesNotExist:
            return Response(status=404)
        serializer = SubCategoriesSerializer(subcategory)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            subcategory = SubCategories.objects.get(pk=pk)
        except SubCategories.DoesNotExist:
            return Response(status=404)
        serializer = SubCategoriesSerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        try:
            subcategory = SubCategories.objects.get(pk=pk)
        except SubCategories.DoesNotExist:
            return Response(status=404)
        subcategory.delete()
        return Response(status=204)
    
# products
class ProductsViewSet(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProductsDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=404)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=404)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(status=404)
        product.delete()
        return Response(status=204)