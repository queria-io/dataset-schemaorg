"""schema.org の語彙（型とプロパティ）を取り出す。

schema.org は GitHub（schemaorg/schemaorg）でタグを切って版を出し、版ごとに
data/releases/<版>/ に CSV を置いている。最新のタグを 1 つ決め、その版の
schemaorg-current-https-{types,properties}.csv（pending などの拡張を除いた本体）を取る。

出力:
- data/schemaorg/types.csv（1行 = 1 型）
- data/schemaorg/properties.csv（1行 = 1 プロパティ）
- data/schemaorg/source_file.parquet（取得したファイルの記録）

データソース: schema.org https://github.com/schemaorg/schemaorg
"""

import logging
import re
import subprocess
from pathlib import Path

from pipelines.source_file import write_source_files
from shared.fetch import fetch_file

logger = logging.getLogger("pipelines")

REPO = "schemaorg/schemaorg"
OUTPUT_DIR = Path("data/schemaorg")
FILES = {"types": "types", "properties": "properties"}
USER_AGENT = "dataset-schemaorg (+https://github.com/queria-io/dataset-schemaorg)"


def version_of(tag: str) -> str | None:
    # 古いタグは v29.4-release、新しいタグは v30.1
    m = re.fullmatch(r"v(\d+)\.(\d+)(?:-release)?", tag)
    return f"{m[1]}.{m[2]}" if m else None


def latest_tag() -> tuple[str, str]:
    out = subprocess.run(
        ["git", "ls-remote", "--tags", "--refs", f"https://github.com/{REPO}.git"],
        check=True, capture_output=True, text=True,
    ).stdout
    tags = [(t, version_of(t)) for t in (line.split("refs/tags/")[1] for line in out.splitlines())]
    return max(((t, v) for t, v in tags if v), key=lambda tv: tuple(int(n) for n in tv[1].split(".")))


def download_schemaorg(output_dir: Path = OUTPUT_DIR) -> str:
    tag, version = latest_tag()
    logger.info("  schema.org %s (%s)", version, tag)
    output_dir.mkdir(parents=True, exist_ok=True)
    page = f"https://github.com/{REPO}/tree/{tag}/data/releases/{version}"
    rows = []
    for name, kind in FILES.items():
        url = f"https://raw.githubusercontent.com/{REPO}/{tag}/data/releases/{version}/schemaorg-current-https-{kind}.csv"
        path = output_dir / f"{name}.csv"
        rows.append({**fetch_file(url, path, user_agent=USER_AGENT), "page_url": page, "paths": [str(path)]})
    write_source_files(rows, output_dir / "source_file.parquet")
    (output_dir / "version.txt").write_text(version)
    return version
