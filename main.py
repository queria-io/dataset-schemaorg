"""schema.org の語彙データパイプライン。

1. schemaorg: 最新の版の型とプロパティの CSV を取る
2. dbt: dbt ビルド
"""

import logging

from dbt.cli.main import dbtRunner

from pipelines.schemaorg import download_schemaorg

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")


def dbt_build():
    dbt = dbtRunner()
    for command in (["deps"], ["build"], ["docs", "generate"]):
        result = dbt.invoke(command)
        if not result.success:
            raise SystemExit(f"dbt {' '.join(command)} failed")


def main():
    logger.info("1/2: schemaorg (schema.org の語彙)")
    download_schemaorg()

    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
