from django.db import models

from blog.models import Post


# Create your models here.
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='评论目标')
    content = models.CharField(verbose_name='内容', max_length=2000)
    nickname = models.CharField(verbose_name='昵称', max_length=50)
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_ITEMS,
                                         default=STATUS_NORMAL)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,
                                        editable=False)

    def __str__(self):
        if len(str(self.content)) > 50:
            return self.content[:50] + '...'
        return self.content

    class Meta:
        verbose_name = verbose_name_plural = '评论'
