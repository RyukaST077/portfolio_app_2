from django import forms
from .models import UserProfile

class ApiKeyForm(forms.ModelForm):
    # フィールド定義はシンプルにしておくことも可能
    gemini_api_key = forms.CharField(
        label='Gemini API Key',
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text='Your personal Gemini API key.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # 親クラスの __init__ を呼び出す
        # フィールドウィジェットの attrs を更新
        self.fields['gemini_api_key'].widget.attrs.update({
            'class': 'search',
            'placeholder': 'Google AI Studio等で取得したキー',
            # 他の属性も追加可能
            'autocomplete': 'off' # オートコンプリートを無効にする例
        })

    class Meta:
        model = UserProfile
        fields = ['gemini_api_key']

class QuestionForm(forms.Form):
    question = forms.CharField(
        label='質問を入力してください',
        widget=forms.Textarea(attrs={'rows': 5, 'class':'input-question', 'placeholder': 'Type your Questions...'}),
        required=True
    )