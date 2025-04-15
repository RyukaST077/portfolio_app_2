from django.shortcuts import render



def page_qrcode(request):
    return render(request, "qrcode_app/qrcode_index.html")

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect # CSRF保護を有効にする
from .qrcode_utils import generate_qrcode_file
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
# from .utils import generate_qrcode_file # 別ファイルにした場合
# または同じファイル内なら from . import generate_qrcode_file
import logging

logger = logging.getLogger(__name__)

def index(request):
    """画像生成ページを表示するビュー"""
    return render(request, 'qrcode_app/qrcode_index.html')

@require_POST # POSTリクエストのみ受け付ける
@csrf_protect # CSRF対策
def generate_qrcode_ajax(request):
    """Ajaxリクエストを受け取り、QRコードを生成して画像のURLを返すビュー"""

    # HTMLフォームのinput要素のname属性が 'url_input' であると仮定
    url_to_encode = request.POST.get('url_input', None) # .get()でキーが存在しない場合Noneを返す

    if not url_to_encode:
        # URLが入力されていない場合のエラーレスポンス
        return JsonResponse({'success': False, 'error': 'URLを入力してください。'}, status=400) # 400 Bad Request

    try:
        # ユーザー入力を渡してQRコード生成関数を呼び出す
        image_url = generate_qrcode_file(url_to_encode)

        # 成功レスポンスを返す
        return JsonResponse({'success': True, 'image_url': image_url})

    except ValueError as ve:
        # generate_qrcode_file内で発生したValueError (入力値が原因)
        logger.warning(f"QRコード生成失敗 (入力エラー): {ve}")
        return JsonResponse({'success': False, 'error': str(ve)}, status=400) # 400 Bad Request

    except IOError as ioe:
        # generate_qrcode_file内で発生したIOError (サーバー側ファイル保存エラー)
        logger.error(f"QRコード画像保存失敗: {ioe}", exc_info=True)
        return JsonResponse({'success': False, 'error': '画像の保存中にサーバーエラーが発生しました。'}, status=500) # 500 Internal Server Error

    except Exception as e:
        # その他の予期せぬエラー
        logger.error(f"QRコード生成処理中に予期せぬエラー: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'QRコードの生成中に不明なエラーが発生しました。'}, status=500) # 500 Internal Server Error
