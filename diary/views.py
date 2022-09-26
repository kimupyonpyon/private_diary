import logging

from django.urls import reverse_lazy

from django.views import generic

from django.contrib import messages

from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

# 同じフォルダのforms.pyからInquiryFormクラスをインポート
from .forms import *

from .models import Diary

from .mixins import OnlyYouMixin

logger=logging.getLogger(__name__)

# indexページを表示するための処理
# TempateView：HTMLを表示する為のクラス
class IndexView(generic.TemplateView):
    # 表示したいHTMLを指定
    template_name="index.html"

# inquiryページを表示するための処理
# FormView：フォームを使ったページを表示するためのクラス
# LoginRequieredMix：ログインしていなければ見られないページ
class InquiryView(generic.FormView):
    template_name="inquiry3.html"
    # 表示したいフォーム
    form_class=InquiryForm
    # 送信が成功したときに移動するURL
    # reverse_lazy:URLの逆引きを行う関数
    # 　diaryアプリのinquiryページのURLを取得
    success_url=reverse_lazy('diary:inquiry')

    # 送信が成功したときに行う処理
    # 引数formに入力した内容が格納される
    def form_valid(self, form):
        # form(InquiryFormクラス)のsend_emailメソッドを実行
        form.send_email()

        # success_urlページで表示するメッセージ
        messages.success(self.request, 'メッセージを送信しました')

        # form.cleand_data['フィールド名']にはエラー処理が完了したデータ保存されている
        logger.info('Inquriry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# 日記一覧ページを表示するビュー
# ListView：指定したモデルを一覧表示する為のクラス
class DiaryListView(LoginRequiredMixin, generic.ListView):
    # 一覧表示したいモデルを指定
    model = Diary
    template_name = 'diary_list.html'
    # １ページに表示する件数を指定
    paginate_by = 2

    # get_queryset：表示したいモデルを設定するメソッド
    # これがないと、モデルの全データが出力される
    def get_queryset(self):
        # モデル.objects：モデルの全データにアクセスする
        # .filter：検索条件を指定
        # self.request.user：ログインしているユーザー
        # .order_by：出力順を指定　フィールド名の先頭に「-」で降順
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

# 日記を１件表示するビュー
# DetailView：指定したモデルに対して、URL引数pkで受け取った主キーを持つデータを表示するクラス
class DiaryDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

# 日記の新規登録をするビュー
# CreateView：指定したモデルに対して、指定したフォームで入力されたデータを登録するクラス
# 　　　　　　　だいたいFormViewと同じ
class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    # データの入力に使用するフォーム
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    # 入力が正しいときに行う処理（データベースに保存する処理）
    def form_valid(self, form):
        # フォームに入力された内容を一時保存する
        # commit=False・・・データベースにはまだ保存されない
        diary = form.save(commit=False)
        # user項目はログインしているユーザーを直接設定
        diary.user = self.request.user
        # データベースに保存
        diary.save()

        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    # 入力が正しくなかった時の処理
    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

# 日記を更新するビュー
# UpdateView：指定したモデルの、URL引数pkで受け取った主キーを持つデータに対して、
# 　　　　　　　指定したフォームで入力されたデータで更新するクラス
# 　　　　　　　だいたいCreateViewと同じ
class DiaryUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    # 今回は「たまたま」新規作成時と同じ入力内容なのでDiaryCreateForm
    form_class = DiaryCreateForm

    # 成功時の移動先が固定でない為
    # success_urlの代わりにget_sccess_urlメソッドを使う
    def get_success_url(self):
        # URL引数としてkwargsに値を設定する
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        # saveメソッドを書かなければ、自動的に入力内容が保存される
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

# 日記を削除するビュー
# DeleteView：指定されたモデルに対して、URL引数pkで受け取った主キーを持つデータを削除するクラス
class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    # 削除処理を行うメソッド
    def delete(self, request, *args, **kwargs):
        # 対象データを削除してくれる
        # 関連するほかのデータの削除処理記述することもある
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)
