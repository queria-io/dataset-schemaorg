# schema.org の語彙

[schema.org](https://schema.org/) の型とプロパティを、SQL で検索できるテーブルにしたデータセットです。schema.org は検索エンジン各社が共同で作った語彙で、Web ページの構造化データで世界的に使われています。

一般のデータの列名を世界標準の語に統一したいとき、ある概念の英語の呼び方を探したいときに使います。Queria のデータセットは、一般のデータの列名をこの語彙のプロパティ名（snake_case）に統一しています。日本の公的データは [gif データセット](https://github.com/queria-io/dataset-gif)の語彙に統一します。決め方は [docs.queria.io のデータセットの規約](https://docs.queria.io/publish/conventions#列名)にあります。

## 出典と利用条件

schema.org は GitHub（[schemaorg/schemaorg](https://github.com/schemaorg/schemaorg)）でタグを付けてバージョンを出し、バージョンごとに `data/releases/<バージョン>/` に配布物を置いています。ビルドのたびに最新のタグを取得し、pending などの拡張を除いた本体の CSV を加工しています。取り込んだバージョンは `version` 列に入ります。

| 原典 | テーブル |
| --- | --- |
| `schemaorg-current-https-types.csv` | `vocab.type` |
| `schemaorg-current-https-properties.csv` | `vocab.property`、`vocab.type_property` |

- schema.org の語彙の定義は CC BY-SA 3.0 で提供されています。このデータセットも CC BY-SA 3.0 です

## テーブル

| テーブル | 内容 | 行数（30.1） |
| --- | --- | ---: |
| `vocab.type` | 型。1 行が 1 型 | 1,485 |
| `vocab.property` | プロパティ。1 行が 1 プロパティ | 1,538 |
| `vocab.type_property` | 型が直接持てるプロパティ。1 行が 1 型の 1 プロパティ | 2,335 |

## 使い方

住所（PostalAddress）が直接持てるプロパティと、列名にするときの形:

```sql
SELECT p.name, p.snake_case_name, p.range
FROM schemaorg.vocab.type_property AS tp
JOIN schemaorg.vocab.property AS p ON p.name = tp.property_name
WHERE tp.type_name = 'PostalAddress'
ORDER BY p.name;
```

## 収録範囲の注意

- `vocab.type_property` は `vocab.property` の `domain` を 1 行ずつに分けたものです。親の型から受け継ぐプロパティは含みません
- `domain`・`range`・`parent` は、値が複数あるとき `|` 区切りで入っています
- `superseded_by` に値がある型・プロパティは非推奨です
- 説明（`description`）は原典の英語の説明から HTML のタグを除いたものです

## ビルド

```bash
git submodule update --init
uv sync
scripts/build.sh   # fdl checkout → python main.py → fdl commit
```

PR では `Build` ワークフローが公開せずに取得と dbt build だけを実行します。
