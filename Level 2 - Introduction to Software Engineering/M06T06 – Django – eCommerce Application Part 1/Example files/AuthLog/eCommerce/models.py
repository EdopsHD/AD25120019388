from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)  
    # The name of the product, like "T-shirt" or "Laptop"
    
    description = models.TextField(blank=True)  
    # A longer description of the product; it’s optional (can be empty)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    # The price of the product, with up to 10 digits total and 2 decimal places for cents
    
    stock = models.PositiveIntegerField()  
    # How many items are available in stock (only positive numbers allowed)
    
    def __str__(self):
        # This makes it easier to see the product’s name when printing or in admin pages
        return self.name

    class Meta:
        # These are special permissions for users who can add, change, delete, or view products
        permissions = [
            ("add_products", "Can add products"),
            ("change_products", "Can change products"),
            ("delete_products", "Can delete products"),
            ("view_products", "Can view products"),
        ]
