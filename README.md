# サンプルクローラー＆Azure Functions 実行手順

## 1. セットアップ手順

### 1-1. Python仮想環境の作成・有効化

Windows PowerShellの場合:
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 1-2. 依存パッケージのインストール

```powershell
pip install -r requirements.txt
```

### 1-3. .envファイルの作成

必要な環境変数を`.env`ファイルに記載してください（例：DB接続情報など）。

---

## 2. Scrapyの実行方法

ルートディレクトリで以下のコマンドを実行してください。

```powershell
scrapy crawl WebCrawlSpider
```

---

## 3. Azure Functions のローカル実行（func start）

### 3-1. Azure Functions Core Tools のインストール

npmがインストールされている場合、以下でインストールできます。

```powershell
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

または、[公式ドキュメント](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-run-local)を参照してください。

### 3-2. func start の実行

ルートディレクトリで以下を実行してください。

```powershell
func start
```

---

## 4. 注意事項

- `data/output.json` にクロール結果が追記されます（JSON Lines形式）。
- DB接続やAPIキーなどは`.env`で管理してください。
- Python 3.8 以上推奨。
- TimerTriggerは1時間ごとに自動実行されます。

---
