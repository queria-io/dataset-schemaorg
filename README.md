# dataset-schemaorg

Queria のデータセット `schemaorg`（schema.org の語彙）のリポジトリです。データセットの説明は [docs/index.md](docs/index.md) にあります。

## ビルド

```bash
git submodule update --init
uv sync
scripts/build.sh   # fdl checkout → python main.py → fdl commit
```

PR では `Build` ワークフローが公開せずに取得と dbt build だけを実行します。
