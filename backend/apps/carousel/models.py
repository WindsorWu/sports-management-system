from django.db import models
from django.conf import settings


class Carousel(models.Model):
    """
    轮播图模型
    
    用于管理系统各个页面的轮播图展示
    
    主要功能:
        - 多位置支持: 可在首页、赛事页、公告页等不同位置展示
        - 排序控制: 通过order字段控制展示顺序
        - 定时展示: 支持设置开始和结束时间
        - 点击统计: 记录轮播图点击次数
        - 链接跳转: 支持点击跳转到指定URL或赛事
        
    关键字段说明:
        - position: 展示位置，决定轮播图显示在哪个页面
        - order: 排序值，数字越小越靠前
        - is_active: 是否启用，未启用的不会显示
        - start_time/end_time: 定时展示的时间范围
        - link_url: 点击跳转的链接
        - event: 关联的赛事（可选）
        
    使用场景:
        - 首页轮播图
        - 赛事推广
        - 活动宣传
        
    数据表名: carousel
    """
    # 展示位置选项
    POSITION_CHOICES = (
        ('home', '首页'),           # 首页轮播图
        ('event', '赛事页'),        # 赛事页面轮播图
        ('announcement', '公告页'),  # 公告页面轮播图
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='描述'
    )
    image = models.CharField(
        max_length=500,
        verbose_name='轮播图片',
        help_text='图片路径，如：/images/carousel/xxx.jpg'
    )
    link_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='链接地址',
        help_text='点击轮播图跳转的URL'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='carousels',
        verbose_name='关联赛事'
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='home',
        verbose_name='展示位置'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='排序',
        help_text='数字越小越靠前'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用'
    )
    start_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='开始时间',
        help_text='定时展示的开始时间'
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='结束时间',
        help_text='定时展示的结束时间'
    )
    click_count = models.IntegerField(
        default=0,
        verbose_name='点击次数'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carousels',
        verbose_name='创建者'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'carousel'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['position', 'is_active', 'order']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.title
