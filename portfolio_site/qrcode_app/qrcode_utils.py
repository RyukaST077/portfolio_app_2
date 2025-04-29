import qrcode
import os
import uuid
import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_qrcode_file(url_data):
    """
    与えられたURL情報からQRコードを生成して保存する
    開発環境と本番環境で保存先を自動的に切り替える
    """
    # 入力検証
    if not url_data or not isinstance(url_data, str):
        raise ValueError("QRコード生成には有効なURLが必要です")
    
    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_data)
    qr.make(fit=True)
    
    # PILイメージオブジェクト生成
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 年/月のサブディレクトリ構造
    from datetime import datetime
    now = datetime.now()
    year_month = now.strftime('%Y/%m')
    
    # 環境に応じた保存先の決定
    # 開発環境: settings.py の DEBUG=True のとき、プロジェクト内のmediaディレクトリ
    # 本番環境: settings.py の DEBUG=False のとき、/var/www/media/ など設定された場所
    if settings.DEBUG:
        base_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    else:
        base_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    
    # 保存先ディレクトリ (年月で整理)
    relative_dir = os.path.join('qrcodes', year_month)
    save_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)
    
    # ディレクトリ作成
    os.makedirs(save_dir, exist_ok=True)
    
    # ファイル名を生成 (一意になるようUUIDとタイムスタンプを使用)
    filename = f"qr_{uuid.uuid4().hex}_{int(time.time())}.png"
    filepath = os.path.join(save_dir, filename)
    
    try:
        # 画像を保存
        img.save(filepath, 'PNG')
        logger.info(f"QRコードを {filepath} として保存しました。")
    except Exception as e:
        logger.error(f"QRコード画像の保存中にエラーが発生しました (パス: {filepath}): {e}")
        # パーミッション情報をログに記録
        try:
            parent_dir = os.path.dirname(filepath)
            logger.error(f"ディレクトリ権限: {os.access(parent_dir, os.W_OK)}")
        except:
            pass
        raise IOError(f"画像の保存に失敗しました: {e}")
    
    # メディアURLの構築
    relative_url = os.path.join(relative_dir, filename).replace('\\', '/')
    image_url = f"{settings.MEDIA_URL}{relative_url}"
    
    return image_url