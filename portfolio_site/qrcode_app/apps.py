from django.apps import AppConfig
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class QrcodeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qrcode_app'
    
    def ready(self):
        # アプリケーション起動時にメディアディレクトリの存在と権限を確認
        qrcode_base_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        
        try:
            os.makedirs(qrcode_base_dir, exist_ok=True)
            
            # 書き込み権限をチェック
            if os.access(qrcode_base_dir, os.W_OK):
                logger.info(f"QRコード保存ディレクトリ {qrcode_base_dir} は正常に設定されています。")
            else:
                logger.warning(f"QRコード保存ディレクトリ {qrcode_base_dir} に書き込み権限がありません！")
        except Exception as e:
            logger.error(f"QRコード保存ディレクトリの設定中にエラーが発生しました: {e}")