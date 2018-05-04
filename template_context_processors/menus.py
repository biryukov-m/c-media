from blog.models import Category
from blog.models import Post


def get_categories(request):
    dic = Category.objects.all()
    return {"category_list": dic}


def get_drafted_posts_count(request):
    return {"drafted_posts_count": Post.objects.is_drafted().count()}
