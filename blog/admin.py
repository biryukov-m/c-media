from django.contrib import admin
from .models import Post, Pseudo, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PseudoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Pseudo, PseudoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
