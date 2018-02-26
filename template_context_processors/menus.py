from django.template.context_processors import request
from blog.models import Category, Menu


def get_categories(request):
    dic = Category.objects.all()
    return {"category_list": dic}


def get_menu(request):
    center = Menu.objects.all().count() // 2
    left = Menu.objects.filter(pk__lte=center)
    right = Menu.objects.filter(pk__gt=center)
    return {"menu_left_list": left, "menu_right_list": right}
