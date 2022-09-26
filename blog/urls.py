from django.urls import path

from . import views

# アプリケーション名
app_name = 'blog'
urlpatterns = [
    # blog/''にアクセスされたらviews.pyのIndexViewを実行
    # ページ名はindex
    path('', views.IndexView.as_view(), name="index"),
    # blog/'post'にアクセスされたらviews.pyのPostViewを実行
    # ページ名はpost
    path('post', views.PostView.as_view(), name="post"),

    path('blog-list/', views.BlogListView.as_view(), name="blog_list"),
]
