# dataset-schemaorg

[schema.org](https://schema.org/) の型とプロパティを Queria のカタログ（[data.queria.io](https://data.queria.io/)）へ取り込むデータセットです。

Queria のデータセットは、一般のデータの列名をこの語彙のプロパティ名（snake_case）に揃えています。
日本の公的データは [dataset-gif](https://github.com/queria-io/dataset-gif) の語彙に揃えます。
決め方は [docs.queria.io のデータセットの規約](https://docs.queria.io/publish/conventions#列名)にあります。

## データ出典

schema.org は GitHub（[schemaorg/schemaorg](https://github.com/schemaorg/schemaorg)）でタグを切って版を出し、
版ごとに `data/releases/<版>/` に配布物を置いています。ビルドのたびに最新のタグを取り、
pending などの拡張を除いた本体の CSV を表にします。取り込んだ版は `version` 列に入ります。

| 原典 | テーブル |
| --- | --- |
| `schemaorg-current-https-types.csv` | `vocab.type` |
| `schemaorg-current-https-properties.csv` | `vocab.property`、`vocab.type_property` |

schema.org の語彙の定義は CC BY-SA 3.0 で提供されています。このデータセットも CC BY-SA 3.0 です。

## 収録テーブル

| テーブル | 内容 | 行数（30.1） |
| --- | --- | ---: |
| `vocab.type` | 型。1行が1型 | 1,485 |
| `vocab.property` | プロパティ。1行が1プロパティ | 1,538 |
| `vocab.type_property` | 型が直接持てるプロパティ。1行が1型の1プロパティ | 2,335 |

## ビルド

```bash
uv sync
uv run python main.py          # 語彙の取得と dbt build（公開ストレージへの書き込みは queria sync が行う）
./scripts/build.sh             # queria sync（pull → ビルド → push）
```

PR では `Build` ワークフローが公開せずに取得と dbt build だけを回します。
