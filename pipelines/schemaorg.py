"""schema.org の語彙（型とプロパティ）を取り出す。

schema.org は GitHub（schemaorg/schemaorg）でタグを切って版を出し、版ごとに
data/releases/<版>/ に CSV を置いている。最新のタグを 1 つ決め、その版の
schemaorg-current-https-{types,properties}.csv（pending などの拡張を除いた本体）を取る。

出力:
- data/schemaorg/types.csv（1行 = 1 型）
- data/schemaorg/properties.csv（1行 = 1 プロパティ）

データソース: schema.org https://github.com/schemaorg/schemaorg
"""

import logging
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger("pipelines")

REPO = "schemaorg/schemaorg"
OUTPUT_DIR = Path("data/schemaorg")
FILES = {"types": "types", "properties": "properties"}


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


def checkout(tag: str, version: str, dest: Path) -> Path:
    # リポジトリは全版の配布物を抱えていて大きいので、その版のディレクトリだけ取る
    subprocess.run(
        ["git", "-c", "advice.detachedHead=false", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse",
         "--branch", tag, f"https://github.com/{REPO}.git", str(dest)],
        check=True,
    )
    subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", f"data/releases/{version}"], check=True)
    return dest / "data" / "releases" / version


def download_schemaorg(output_dir: Path = OUTPUT_DIR) -> str:
    tag, version = latest_tag()
    logger.info("  schema.org %s (%s)", version, tag)
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        release = checkout(tag, version, Path(tmp) / "schemaorg")
        for name, kind in FILES.items():
            src = release / f"schemaorg-current-https-{kind}.csv"
            if not src.exists():
                raise SystemExit(f"{REPO}@{tag}: {src.name} が無い")
            shutil.copyfile(src, output_dir / f"{name}.csv")
    (output_dir / "version.txt").write_text(version)
    return version
