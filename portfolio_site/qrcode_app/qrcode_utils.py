# qrcode_app/utils.py や qrcode_app/views.py など、適切な場所に配置

import qrcode
import uuid
import os
import time
from django.conf import settings
import logging

logger = logging.getLogger(__name__) # ロギング設定 (推奨)

def generate_qrcode_file(url_data):
    """
    与えられたデータ (URL) からQRコード画像を生成し、
    MEDIA_ROOT以下に保存して、その公開URLを返す関数。

    Args:
        url_data (str): QRコードに変換したいURL文字列。

    Returns:
        str: 生成されたQRコード画像の公開URL。

    Raises:
        ValueError: url_dataが空の場合やQRコード生成に失敗した場合。
        IOError: 画像ファイルの保存に失敗した場合。
    """
    # 1. 入力データの検証
    if not url_data:
        # URLデータが空の場合はエラー
        raise ValueError("QRコードに変換するURLが指定されていません。")

    # 2. QRコードを生成
    try:
        # qrcodeライブラリを使って画像をメモリ上に生成
        img = qrcode.make(url_data) # 引数 url_data を使用
    except Exception as e:
        logger.error(f"QRコード生成中にエラーが発生しました (データ: {url_data}): {e}")
        # qrcode.makeで失敗する可能性のあるエラーを捕捉
        raise ValueError(f"QRコードの生成に失敗しました: {e}")

    # 3. 画像ファイルとして保存
    #    一意なファイル名を生成
    filename = f"qr_{uuid.uuid4()}_{int(time.time())}.png"

    #    保存先ディレクトリ (例: media/qrcodes/)
    #    settings.py で MEDIA_ROOT が正しく設定されている前提
    save_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes') # 'generated_images' から 'qrcodes' に変更 (任意)
    os.makedirs(save_dir, exist_ok=True) # ディレクトリがなければ作成

    #    保存するファイルのフルパス
    filepath = os.path.join(save_dir, filename)

    #    画像をファイルに保存
    try:
        img.save(filepath, 'PNG') # 保存形式を明示 (PNGが一般的)
        logger.info(f"QRコードを {filepath} として保存しました。") # ログ出力 (開発/デバッグに便利)
    except Exception as e:
        logger.error(f"QRコード画像の保存中にエラーが発生しました (パス: {filepath}): {e}")
        raise IOError(f"画像の保存に失敗しました: {e}") # 保存失敗はIOErrorなど適切な例外を発生

    # 4. 生成された画像の公開URLを組み立てる
    #    settings.py で MEDIA_URL が正しく設定されている前提
    #    例: MEDIA_URL = '/media/'
    image_url = f"{settings.MEDIA_URL}qrcodes/{filename}" # 保存先ディレクトリ名と合わせる

    return image_url