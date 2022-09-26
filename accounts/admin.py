from django.contrib import admin

from .models import CustomUser

# Register your models here.

# admin.py：Djangoにデフォルトで用意されている管理サイトから
# 　　　　　　扱うモデルを登録する

# CustomUserを管理サイトに登録する
admin.site.register(CustomUser)