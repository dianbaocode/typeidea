from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Category, Tag, Post

from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


# Register your models here.


# class CustomSite(AdminSite):
#     site_header = 'TX'
#     site_title = 'TX管理后台'
#     index_title = '首页'
#
#
# custom_site = CustomSite()
# custom_site = CustomSite(name='cus_admin')


class PostInline(admin.TabularInline):
    fields = ('title', 'desc',)
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count',)
    fields = ('name', 'status', 'is_nav')

    # inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器，只展示当前用户分类 """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'operator',)
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'), 'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc', 'content',
            ),
        }),
        ('额外信息', {
            # 'classes': ('collapse', ),
            'fields': ('tag',),
        }),
    )
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag', )
    list_display_links = []
    # list_filter = ('category', )
    list_filter = (CategoryOwnerFilter,)

    search_fields = ('title', 'category__name',)
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('cus_admin:blog_post_change', args=(obj.pk,)))

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
