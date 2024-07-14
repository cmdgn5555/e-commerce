from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }

    fields = ['name', 'slug']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }

    fields = ['title', 'slug', 'description', 'price', 'image', 'category', 'brand']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)