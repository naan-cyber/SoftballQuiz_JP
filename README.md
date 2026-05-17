# ソフトボール まもり方クイズ

まもる場所、ランナー、アウト、打ったボールに合わせて「はじめに何をするか」をクイズ形式で練習する Flet アプリです。
画面でピッチャー、キャッチャー、一るい、二るい、三るい、ショート、レフト、センター、ライトを選べます。

## 起動

```bash
uv run flet run
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

## 構成

- `main.py`: Flet 起動用の薄い入口
- `softball_quiz/models.py`: 問題、選択肢、ランナー、まもる場所などのデータモデル
- `softball_quiz/data/*_questions.py`: まもる場所ごとのクイズ問題データ
- `softball_quiz/services/quiz_engine.py`: 出題順、採点、進行状態の管理
- `softball_quiz/ui/`: Flet の画面構築と表示コンポーネント

まもり方はチーム方針、ランナーの速さ、グラウンド状況で変わります。このアプリの回答は、子ども向けのきほん練習として使いやすい優先順位で整理しています。
