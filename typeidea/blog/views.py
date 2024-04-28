from django.http import HttpResponse
from django.shortcuts import render

from .models import Tag, Post, Category
from config.models import SideBar


# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_post()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        # 'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, template_name='blog/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    context = {'post': post, }
    context.update(Category.get_navs())
    return render(request, template_name='blog/detail.html', context={'post': post})


def links(request):
    return HttpResponse('links')
