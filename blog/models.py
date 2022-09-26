from django.db import models

from accounts.models import CustomUser

# Create your models here.

class Blog(models.Model):
    
    # 必要な項目を列挙する
    # ユーザー：外部キー（カスタムユーザー）
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    # タイトル：文字列　最大40文字
    title = models.CharField(verbose_name='タイトル', max_length=40)
    # 本文：テキスト　空白許可
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    # 写真：画像　空白許可
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    # 作成日時：日付時刻　新規作成時、自動で現在時刻を設定
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    # 更新日時：日付時刻　更新時、自動で現在時刻を設定
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'ブログ'