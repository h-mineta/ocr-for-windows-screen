# OCR for Windows Screen 
Windows画面上のテキストをOCRで取り込むPython

## Install
Python 3.12 -> Microsoft Storeで入れると良い
https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=ja-jp&gl=JP

Tesseract v5.3.3 -> GitHubの最新インストーラ(exe)を入れる
https://github.com/UB-Mannheim/tesseract/wiki

pipで必要なライブラリをインストール
```powershell
cd ocr-for-windows-screen
pip.exe install -r .\requirements.txt
```

環境変数名の設定にTesseract-OCRのPATHを追加
![環境変数名の編集](https://raw.githubusercontent.com/h-mineta/ocr-for-windows-screen/main/doc/images/setting_windows_env.png)

## Start
```powershell
cd ocr-for-windows-screen
python3.exe .\main.py
```

## 参考
Pythonでディスプレイ上のテキストをOCRで定期的に抽出するの巻
https://vucavucalife.com/periodically-extract-on-screen-text-using-python-ocr/
