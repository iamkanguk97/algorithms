#!/usr/bin/env python3
"""장 파일의 파이썬 코드 블록을 실제로 실행해 본문의 "실행 결과"와 대조한다.

사용법 (책 폴더 docs/python-algorithms 에서):
    python tools/check_outputs.py                  # 모든 장
    python tools/check_outputs.py 19-sorting.html  # 지정한 장만
    python tools/check_outputs.py --python ../../.venv/bin/python 26-dynamic-programming.html

대조 규칙은 assets/code.js 와 같다.
- <pre data-lang="python"> 바로 뒤에 오는 <pre class="stdin"> 은 표준 입력으로 넣고,
  <pre class="output"> 은 기대 출력으로 본다. output 이 없는 코드 블록은 실행하지 않는다.
- 코드, 입력, 출력 모두 앞의 빈 줄과 뒤의 공백을 지운 뒤 글자 단위로 비교한다.
- 표준 라이브러리만 쓴다. 코드는 -I 옵션으로 격리된 임시 폴더에서 실행한다.
"""

from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent
CHAPTER_FILE_PATTERN = re.compile(r"^\d{2}-.*\.html$")
RUN_TIMEOUT_SECONDS = 20


def trim_like_code_js(text: str) -> str:
    """code.js 의 replace(/^\\n+|\\s+$/g, '') 와 같은 정리."""
    return re.sub(r"^\n+|\s+$", "", text)


@dataclass
class CodeBlock:
    title: str
    line: int
    code: str
    stdin: str | None = None
    output: str | None = None


@dataclass
class ChapterParser(HTMLParser):
    """python 코드 블록과 그 뒤에 붙은 stdin/output 을 순서대로 모은다."""

    blocks: list[CodeBlock] = field(default_factory=list)
    _capturing: str | None = None  # 'code' | 'stdin' | 'output'
    _buffer: list[str] = field(default_factory=list)
    _pre_depth: int = 0
    _pending: CodeBlock | None = None  # stdin/output 을 기다리는 코드 블록

    def __post_init__(self) -> None:
        super().__init__(convert_charrefs=True)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._capturing:
            return
        if tag != "pre":
            self._pending = None
            return
        attr = dict(attrs)
        classes = (attr.get("class") or "").split()
        if attr.get("data-lang") == "python":
            self._pending = CodeBlock(
                title=attr.get("data-title") or "Python",
                line=self.getpos()[0],
                code="",
            )
            self.blocks.append(self._pending)
            self._begin("code")
        elif "stdin" in classes and self._pending is not None:
            self._begin("stdin")
        elif "output" in classes and self._pending is not None:
            self._begin("output")
        else:
            self._pending = None

    def handle_endtag(self, tag: str) -> None:
        if not self._capturing:
            return
        if tag != "pre":
            return
        text = trim_like_code_js("".join(self._buffer))
        block = self._pending
        if block is None:
            self._capturing = None
            return
        if self._capturing == "code":
            block.code = text
        elif self._capturing == "stdin":
            block.stdin = text
        elif self._capturing == "output":
            block.output = text
            self._pending = None  # output 이 마지막이다
        self._capturing = None

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._buffer.append(data)

    def _begin(self, kind: str) -> None:
        self._capturing = kind
        self._buffer = []


def parse_chapter(path: Path) -> list[CodeBlock]:
    parser = ChapterParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.blocks


@dataclass
class RunResult:
    block: CodeBlock
    is_pass: bool
    actual: str
    stderr: str


def run_block(block: CodeBlock, python: str) -> RunResult:
    with tempfile.TemporaryDirectory() as work_dir:
        script = Path(work_dir) / "snippet.py"
        script.write_text(block.code + "\n", encoding="utf-8")
        try:
            completed = subprocess.run(
                [python, "-I", str(script)],
                input=(block.stdin or "") + "\n",
                capture_output=True,
                text=True,
                cwd=work_dir,
                timeout=RUN_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return RunResult(block, False, "", f"{RUN_TIMEOUT_SECONDS}초 안에 끝나지 않음")
    actual = trim_like_code_js(completed.stdout)
    is_pass = completed.returncode == 0 and actual == block.output
    return RunResult(block, is_pass, actual, completed.stderr.strip())


def report_failure(path: Path, result: RunResult) -> None:
    block = result.block
    print(f"  FAIL  {block.title}  (line {block.line})")
    if result.stderr:
        print("        stderr:")
        for line in result.stderr.splitlines()[-6:]:
            print(f"          {line}")
    diff = difflib.unified_diff(
        (block.output or "").splitlines(),
        result.actual.splitlines(),
        fromfile="expected (pre.output)",
        tofile="actual (stdout)",
        lineterm="",
    )
    for line in diff:
        print(f"        {line}")


def check_chapter(path: Path, python: str) -> tuple[int, int]:
    blocks = [b for b in parse_chapter(path) if b.output is not None]
    results = [run_block(block, python) for block in blocks]
    failed = [r for r in results if not r.is_pass]
    status = "PASS" if not failed else "FAIL"
    print(f"{status}  {path.name}  ({len(blocks) - len(failed)}/{len(blocks)} blocks)")
    for result in failed:
        report_failure(path, result)
    return len(blocks), len(failed)


def resolve_targets(names: list[str]) -> list[Path]:
    if names:
        return [Path(name) if Path(name).is_absolute() else BOOK_DIR / name for name in names]
    return sorted(p for p in BOOK_DIR.iterdir() if CHAPTER_FILE_PATTERN.match(p.name))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("chapters", nargs="*", help="검사할 장 파일 이름. 비우면 모든 장")
    parser.add_argument("--python", default=sys.executable, help="코드를 실행할 파이썬 (기본: 이 스크립트를 실행한 파이썬)")
    args = parser.parse_args()

    targets = resolve_targets(args.chapters)
    missing = [p for p in targets if not p.exists()]
    if missing:
        for p in missing:
            print(f"파일이 없다: {p}", file=sys.stderr)
        return 2

    print(f"python: {args.python}")
    total_blocks = total_failed = 0
    for path in targets:
        blocks, failed = check_chapter(path, args.python)
        total_blocks += blocks
        total_failed += failed
    print(f"\n{len(targets)} chapters, {total_blocks} blocks, {total_failed} failed")
    return 1 if total_failed else 0


if __name__ == "__main__":
    sys.exit(main())
