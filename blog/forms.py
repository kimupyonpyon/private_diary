from django import forms

class PostForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=30)
    # sexの選択肢
    _choices=(
        # 送信する値と表示する文字列を組で記述する
        (1,'男性'),
        (2,'女性'),
        (3,'未回答')
    )
    # ChoiceField:デフォルトはセレクトボックス
    # widget=forms.RadioSelectでラジオボタン
    sex = forms.ChoiceField(label='性別', choices=_choices, widget=forms.RadioSelect)

    # MultipleChoiceFieldは複数選択
    # widget=forms.CheckboxSelectMultipleでチェックボックス
    sex2 = forms.MultipleChoiceField(label='性別', choices=_choices,widget=forms.CheckboxSelectMultiple)

    email1 = forms.EmailField(label='メールアドレス')
    email2 = forms.EmailField(label='メールアドレス(再入力)')

    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'


        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    # clean_フィールド名　メソッド
    # 該当フィールドの入力値チェックを行う
    def clean_message(self):
        # 入力されたmessageの値を取得
        message = self.cleaned_data['message']
        if("NG" in message):
            # エラーを発生させる
            # 引数が画面上にエラーメッセージとして表示される
            raise forms.ValidationError('NGワードが含まれています')
        return message

    # 複数のフィールドに対するチェックを行う
    def clean(self):
        cleaned_data=super().clean()
        # 入力された値を取得
        email1=cleaned_data.get('email1')
        email2=cleaned_data.get('email2')
        if email1 != email2:
            # form.non_field_errorsで表示される
            raise forms.ValidationError('メールアドレスが一致しません')

            # email2にエラーメッセージを表示させたい場合は
            # raise~の代わりに下記を記載
            # self.add_error('email2','メールアドレスが一致しません')