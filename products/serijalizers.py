from rest_framework import serializers
from .models import Products, Categories, SubCategories, ProductImage, Review

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