from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

# 同じフォルダのforms.pyからPostFormクラスをインポート
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Blog

# Create your views here.

class IndexView(generic.TemplateView):
    # templatesフォルダの中のblog/index.htmlを表示
    template_name='blog/index.html'

class PostView(generic.FormView):
    # templatesフォルダの中のblog/input.htmlを表示
    template_name='blog/post.html'
    form_class=PostForm
    success_url=reverse_lazy('blog:post')
    
    def form_valid(self, form):
        
        # POST送信されたnextの値を取得
        next = self.request.POST.get('next')
        # テンプレートで出力したい変数
        context={'form':form, 'tekitou':'適当な文字列'}

        # 確認画面の表示
        if next == 'check':
            # check.htmlを表示
            # contextの内容をテンプレートに渡す
            return render(self.request,'blog/check.html',context)
        # 入力画面に戻る
        elif next=='back':
            # post.htmlを表示
            return render(self.request,'blog/post.html',context)
        # 確定する
        elif next=='confirm':
            # 本来の成功時の処理を記述
            # form.send_email()
            messages.success(self.request, 'メッセージを送信しました。')
            logger.info('Inquiry sent by {}'.format(form.cleaned_data['email1']))
            print("aaaaaaaaaaaaaaaaaaa")
            return super().form_valid(form)

class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name='blog/blog_list.html'

    def get_queryset(self):
        blogs = Blog.objects.filter(user=self.request.user).order_by('-created_at')
        return blogs