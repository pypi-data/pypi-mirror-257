# Notion Util

このプロジェクトは、Notion.soの非公式Python APIクライアントです。
NotionページのMarkdown変換やNotion Databaseのcsv変換が可能です。

## インストール

このパッケージをインストールするには、以下のコマンドを実行してください。
```bash
pip install notion-util
```

## 使い方

```bash
export NOTION_SECRET=secret_xxxxxxxxxxxx
```

```python
from notion.util import get_page_markdown
# notion page url
url = "https://www.notion.so/xxxx"
# ページのブロックを取得
markdown_content = get_page_markdown(url, recursive=False)
print(markdown_content)
```
