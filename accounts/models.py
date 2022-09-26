from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# モデル＝データベースのテーブル

# マイグレーションファイルの生成・・・データーベースに登録する準備をすること
# python manage.py makemigrations

# マイグレーションを実行・・・実際にデータベースにテーブルを登録すること
# python manage.py migrate

# AbstractUser：Djangoにデフォルトで用意されているユーザーモデル
# 　　　　　　　　ログインIDやパスワードなどが用意されている
# 　　　　　　　　継承したCustomUserクラスにそのほか必要な項目を追加する

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    # 管理で必要な情報などを記述するクラス
    class Meta:
        # 管理サイトで表示されるモデル名
        verbose_name_plural = 'CustomUser'