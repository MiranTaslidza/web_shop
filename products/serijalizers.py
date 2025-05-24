from rest_framework import serializers
from .models import Products, Categories, SubCategories, ProductImage, Review
from django.db.models import Avg

# seriijalizer za kategije
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        read_only_fields = ['id']

# seriijalizer za podkategorije
class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = '__all__'
        read_only_fields = ['id']


# seriijalizer za proizvode
class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    subcategory = SubCategoriesSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all(), write_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategories.objects.all(), write_only=True, required=False, allow_null=True)
    
    average_rating = serializers.SerializerMethodField()  # polje za  prikaz  prosječne ocjene

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'category', 'subcategory']

    def create(self, validated_data):
        category = validated_data.pop('category_id')
        subcategory = validated_data.pop('subcategory_id', None)
        product = Products.objects.create(category=category, subcategory=subcategory, **validated_data)
        return product

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            instance.category = validated_data.pop('category_id')
        if 'subcategory_id' in validated_data:
            instance.subcategory = validated_data.pop('subcategory_id')
        return super().update(instance, validated_data)
    
    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg is not None else None
    

# seriijalizer za slike proizvoda
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ['id']


# seriijalizer za recenzije
class ReviewSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), write_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'product']

    def update(self, instance, validated_data):
        # Izvadi product_id ako ga ima
        product = validated_data.pop('product_id', None)
        if product:
            instance.product = product

        # Ažuriraj ostala polja
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        review = Review.objects.create(product=product, **validated_data)
        return review