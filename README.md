# ソフトボール つぎはどうする？

まもる人や走る人が、ボールの動きに合わせて「はじめに何をするか」をクイズ形式で練習するアプリです。画面で守備のポジション、バッターランナー、一るいランナー、二るいランナー、三るいランナー、きほんルールの項目を選べます。

## 起動

```bash
uv run --locked flet run
```

または依存関係を入れた環境で:

```bash
python main.py
```

## テスト

Flet を起動せず、クイズロジックと問題データだけを確認します。

```bash
python -m unittest discover -s tests
```

## GitHub Pages で公開

このリポジトリは GitHub Actions で Flet の静的 Web アプリをビルドし、GitHub Pages にデプロイできます。

1. GitHub の `Settings` → `Pages` で、`Build and deployment` の `Source` を `GitHub Actions` にします。
2. `main` ブランチへ push します。
3. `Actions` タブで `Build and Deploy Flet Web App` の完了を確認します。

公開 URL は次の形式です。

```text
https://naan-cyber.github.io/SoftballQuiz_JP/
```

ローカルで Pages 用の静的サイト生成だけ確認する場合:

```bash
rm -rf .pages-app build/web
mkdir -p .pages-app
cp main.py .pages-app/
cp -R softball_quiz .pages-app/
find .pages-app -type d -name __pycache__ -prune -exec rm -rf {} +
FLET_VERSION="$(uv run --locked python -c 'import flet; print(flet.__version__)')"
cat > .pages-app/pyproject.toml <<EOF
[project]
name = "softball-next-play-quiz"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["flet==${FLET_VERSION}"]
EOF
uv run --locked flet publish .pages-app/main.py --distpath "$PWD/build/web" --base-url SoftballQuiz_JP --route-url-strategy hash
cp robots.txt build/web/robots.txt
find build/web -type f \( -name "*.map" -o -name "*.symbols" \) -delete
```

## 公開前のセキュリティ

- GitHub Actions は必要な権限だけを使い、`uv.lock` と一致しない依存関係ではビルドしないようにしています。
- 公開用ビルドから、デバッグ用の source map と symbols ファイルを削除します。
- 公開用ビルドに、クローラーへ全ページのクロール拒否を伝える `robots.txt` を含めます。
- 依存関係と GitHub Actions の更新は Dependabot で確認します。
- 依存関係の既知のぜい弱性は `Security Checks` ワークフローで確認します。
- `.env` や鍵ファイルは、誤ってコミットしにくいよう `.gitignore` に入れています。
- このアプリは、名前・メールアドレスなどの個人情報を入力させず、クイズ結果も外部へ送信しません。

## 構成

- `main.py`: Flet 起動用の薄い入口
- `softball_quiz/models.py`: 問題、選択肢、ランナー、まもる場所などのデータモデル
- `softball_quiz/data/*_questions.py`: まもる場所、走る人、きほんルールごとのクイズ問題データ
- `softball_quiz/services/quiz_engine.py`: 出題順、採点、進行状態の管理
- `softball_quiz/ui/`: Flet の画面構築と表示コンポーネント

## 注意

プレー判断はチーム方針、ランナーの速さ、グラウンド状況で変わります。このアプリの回答は、子ども向けのきほん練習として使いやすい優先順位で整理しています。問題の正解が絶対ではないこと、実際のプレーでは状況に応じて判断することが大切です。もし明らかに誤った内容や、より良い選択肢があれば、ぜひフィードバックをお寄せください。


## ライセンス

このリポジトリは、コードと教材コンテンツでライセンスを分けています。

- ソースコード: MIT License。詳しくは `LICENSE` を参照してください。
- クイズ本文、解説、場面説明などの教材コンテンツ: CC BY-NC 4.0。詳しくは `CONTENT_LICENSE.md` を参照してください。

第三者ライブラリや依存関係には、それぞれのライセンスが適用されます。
