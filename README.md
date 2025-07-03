# mdメモアプリ

## 概要
Django で実装された Markdown メモ管理アプリです。Markdown テキストを HTML へ変換し PDF を生成、サムネイル画像も作成して保存できます。作成したメモは他のユーザーと共有可能です。

## 主な機能
- メールアドレスを用いたユーザー登録・ログイン
- Markdown ファイルの作成、一覧表示、編集、削除
- Markdown を HTML に変換し PDF を出力
- PDF からサムネイル画像を生成しローカルまたは AWS S3 に保存
- 他ユーザーへのメモ共有

## セットアップ
1. Python 3.10 以上を用意して仮想環境を作成します。
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install django weasyprint pdf2image pillow boto3 python-dotenv django-environ
   ```
2. プロジェクトルートに `.env` を配置し、以下の値を設定します。
   ```env
   SECRET_KEY=your-secret-key
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_STORAGE_BUCKET_NAME=your-bucket
   ```
3. 初期設定を行います。
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. 開発サーバを起動します。
   ```bash
   python manage.py runserver
   ```

## ディレクトリ構成
- `mdapp/` … Markdown メモの管理アプリ
- `accounts/` … 認証・ユーザー管理

## 補足
- 環境変数は `django-environ` を使って読み込まれます【config/settings.py L18-L31】。
- 各ユーザー内でタイトルが重複しないよう制約を設けています【mdapp/models.py L54-L58】。
- PDF 生成処理は `weasyprint` を利用しており CSS を取り込んで PDF を作成します【mdapp/services/pdf_gerater.py L1-L36】。
- 生成した PDF からサムネイル画像を作成する処理も実装されています【mdapp/services/img_generater.py L1-L36】。
