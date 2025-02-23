from django.contrib import admin
from .models import Game, Category, Item


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'price')
    list_editable = ('available', 'price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
