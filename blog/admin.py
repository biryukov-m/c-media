from django.contrib import admin
from .models import Post, Pseudo, Category, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Pseudo)
admin.site.register(Category)
admin.site.register(Tag)
