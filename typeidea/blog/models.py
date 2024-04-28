from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(verbose_name='名称', max_length=50)
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL)
    is_nav = models.BooleanField(verbose_name='是否设置为导航', default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,
                                        editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {'navs': nav_categories, 'categories': normal_categories}


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(verbose_name='名称', max_length=50)
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,
                                        editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )
    title = models.CharField(verbose_name='标题', max_length=255)
    desc = models.CharField(verbose_name='摘要', max_length=1024, blank=True)
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,
                                        editable=False)
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        if len(str(self.title)) > 50:
            return self.title[:50] + '...'
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Tag.objects.get(pk=category_id)
        except Tag.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = Category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, category

    @classmethod
    def latest_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
