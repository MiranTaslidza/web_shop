from django.db import models

# Kategorije
class Categories ( models.Model ):
    name = models.CharField( max_length=100 )
    description = models.TextField()
    icon = models.ImageField( upload_to='categories/' )
    slug = models.SlugField( unique=True )
    display_order = models.IntegerField( default=0 ) # display order

    def __str__(self):
        return self.name

# Podkategorije
class SubCategories ( models.Model ):
    name = models.CharField( max_length=100 )
    description = models.TextField()
    slug = models.SlugField( unique=True )
    category = models.ForeignKey( Categories, on_delete=models.CASCADE )
    icon = models.ImageField( upload_to='subcategories/' )
    display_order = models.IntegerField( default=0 ) # display order


    def __str__(self):
        return self.name   

# Proizvodi    

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
# Slike proizvoda
class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)  # Označava glavnu sliku
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']

# klasa za recenzije
class Review(models.Model):
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.product.name} - Rating: {self.rating}'