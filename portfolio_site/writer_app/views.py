

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import ApiKeyForm, QuestionForm
import google.generativeai as genai
import os
from django.contrib.auth.forms import UserCreationForm # 標準のユーザー作成フォーム
from django.shortcuts import render, redirect
from django.urls import reverse_lazy # URL名を解決するため
from django.contrib import messages # メッセージ表示用

def index(request):
    return render(request, 'writer_app/index.html')

def signup(request):
    """ユーザー登録ビュー"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # ユーザーを作成してデータベースに保存
            # UserProfileを自動作成するシグナルが設定されていれば、ここで自動で作成されるはず
            messages.success(request, 'アカウントを登録しました。ログインしてください。')
            return redirect('login') # ログインページへリダイレクト
        else:
            # フォームが無効な場合、エラーメッセージがformに含まれる
            messages.error(request, '入力内容に誤りがあります。確認してください。')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def manage_api_key(request):
    # UserProfileが存在しない場合は作成 (シグナルがあるので通常は不要だが念のため)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ApiKeyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'APIキーを保存しました。')
            return redirect('writer_app:ask_gemini') # 質問ページへリダイレクト
        else:
            messages.error(request, '入力内容を確認してください。')
    else:
        form = ApiKeyForm(instance=profile)

    return render(request, 'writer_app/api_key_form.html', {'form': form})



@login_required
def ask_gemini(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    api_key = profile.gemini_api_key

    if not api_key:
        messages.warning(request, 'Geminiを利用するには、まずAPIキーを設定してください。')
        return redirect('writer_app:manage_api_key') # APIキー設定ページへ誘導

    question_form = QuestionForm()
    answer = None
    error_message = None


    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.cleaned_data['question']
            prompt = f"""
#質問
{question}

#制約
・出力は必ずHTML形式で行うこと。
・styleタグは使用しないこと。"""
            try:
                # APIキーを使ってGeminiを設定
                genai.configure(api_key=api_key)

                # モデルを選択 (例: gemini-1.5-flash)
                # model = genai.GenerativeModel('gemini-pro') # 旧モデル
                model = genai.GenerativeModel('gemini-1.5-flash') # 新しい高速モデル

                # Geminiにリクエスト送信
                response = model.generate_content(prompt)
                answer = response.text
                answer = answer.replace('```html', '').replace('```', '') # コードブロックを削除

            except Exception as e:
                # APIキーが無効な場合などのエラーハンドリング
                error_message = f"Gemini APIとの通信中にエラーが発生しました: {e}"
                print(f"Gemini API Error for user {request.user.username}: {e}") # ログ出力
                # APIキーが無効な場合のエラーメッセージ例 (実際のメッセージは異なる可能性あり)
                if "API key not valid" in str(e) or "permission denied" in str(e).lower():
                     messages.error(request, "APIキーが無効か、権限がありません。APIキーを確認・再設定してください。")
                     # 必要に応じてAPIキーをクリアする
                     # profile.gemini_api_key = None
                     # profile.save()
                     return redirect('writer_app:manage_api_key') # 再設定を促す
                elif "quota" in str(e).lower():
                     messages.error(request, "APIの利用上限に達した可能性があります。")
                else:
                    messages.error(request, error_message)

    context = {
        'question_form': question_form,
        'answer': answer,
        'error_message': error_message, # messagesフレームワークで表示しない場合に使用
    }
    return render(request, 'writer_app/ask_gemini.html', context)