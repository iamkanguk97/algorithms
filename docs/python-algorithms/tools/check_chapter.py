#!/usr/bin/env python3
"""장 HTML을 검사한다: 코드 블록 실행 결과가 적힌 출력과 같은지, 장 구조가 책의 규격을 지키는지.

사용법:
    python tools/check_chapter.py 08-array.html [09-linked-list.html ...]
    python tools/check_chapter.py --no-run 0*.html      # 구조만 검사
    python tools/check_chapter.py --python .venv/bin/python 0*.html

규칙:
  · <pre data-lang="python" data-title="이름.py"><code>…</code></pre> 바로 뒤에는 <pre class="output">가 와야 하고
    (표준 입력이 필요하면 그 사이에 <pre class="stdin">), 실행한 stdout 이 output 과 같아야 한다.
  · 한 장의 블록은 같은 임시 폴더에 data-title 이름으로 쓰인 뒤 문서 순서대로 실행되므로,
    앞 블록이 정의한 것을 뒤 블록이 `from 이름 import …` 로 가져다 쓸 수 있다.
  · 장 구조(절 순서, 문제 풀이의 접기 3개, 스스로 확인 4문, 분량 등)는 lint_structure 의 규칙을 따른다.
표준 라이브러리만 쓴다.
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent
TITLE_PATTERN = re.compile(r'^(\d{2})\. .+ — 파이썬 알고리즘 노트$')
TAIL_SECTIONS = [('pitfalls', '자주 하는 실수'), ('problem', '대표 문제'), ('recall', '스스로 확인'), ('summary', '정리')]
REVEAL_TITLES = ['접근 방법', '풀이 코드', '복잡도']
CONCEPT_SECTIONS = (5, 8)
GOALS = (4, 5)
CHIPS = (3, 6)
WARN_CALLOUTS = (3, 6)
FIGURES = (1, 3)
RECALL_QUESTIONS = 4
SUMMARY_ITEMS = (4, 8)
CHARS = (8_500, 10_500)
CODE_LINES_WARN = 30
CODE_LINES_MAX = 45
RUN_TIMEOUT_SEC = 10


@dataclass
class Node:
    tag: str | None                      # None 이면 텍스트 노드
    attrs: dict[str, str] = field(default_factory=dict)
    children: list['Node'] = field(default_factory=list)
    text: str = ''
    parent: 'Node | None' = None

    def classes(self) -> set[str]:
        return set(self.attrs.get('class', '').split())

    def text_content(self) -> str:
        if self.tag is None:
            return self.text
        return ''.join(child.text_content() for child in self.children)

    def find_all(self, tag: str | None = None, cls: str | None = None, attr: str | None = None) -> list['Node']:
        found = []
        for child in self.children:
            if child.tag is None:
                continue
            tag_ok = tag is None or child.tag == tag
            cls_ok = cls is None or cls in child.classes()
            attr_ok = attr is None or attr in child.attrs
            if tag_ok and cls_ok and attr_ok:
                found.append(child)
            found.extend(child.find_all(tag, cls, attr))
        return found

    def find(self, tag: str | None = None, cls: str | None = None, attr: str | None = None) -> 'Node | None':
        found = self.find_all(tag, cls, attr)
        return found[0] if found else None

    def element_children(self) -> list['Node']:
        return [child for child in self.children if child.tag is not None]

    def next_element(self) -> 'Node | None':
        """공백 텍스트를 건너뛴 다음 형제 요소. 그 사이에 글자가 있으면 None."""
        siblings = self.parent.children if self.parent else []
        for sibling in siblings[siblings.index(self) + 1:]:
            if sibling.tag is not None:
                return sibling
            if sibling.text.strip():
                return None
        return None


VOID_TAGS = {'meta', 'link', 'br', 'hr', 'img', 'input'}


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.current = self.root

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {k: v or '' for k, v in attrs}, parent=self.current)
        self.current.children.append(node)
        if tag not in VOID_TAGS:
            self.current = node

    def handle_endtag(self, tag: str) -> None:
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data: str) -> None:
        self.current.children.append(Node(None, text=data, parent=self.current))


def parse(path: Path) -> Node:
    builder = TreeBuilder()
    builder.feed(path.read_text(encoding='utf-8'))
    return builder.root


def normalize(text: str) -> str:
    """code.js 가 화면에 보여 주기 전에 하는 정리와 같다: 앞 줄바꿈과 뒤 공백을 지운다."""
    return re.sub(r'^\n+|\s+$', '', text)


@dataclass
class CodeBlock:
    title: str
    source: str
    stdin: str | None
    output: str | None
    index: int


def collect_code_blocks(article: Node, errors: list[str]) -> list[CodeBlock]:
    blocks = []
    for index, pre in enumerate(article.find_all('pre', attr='data-lang'), start=1):
        title = pre.attrs.get('data-title', '')
        label = f'코드 {index}({title or "제목 없음"})'
        if pre.attrs['data-lang'] != 'python':
            continue
        if not title.endswith('.py'):
            errors.append(f'{label}: data-title 은 ".py" 로 끝나는 파일명이어야 한다')
        code = pre.find('code')
        source = normalize(code.text_content() if code else pre.text_content())
        line_count = source.count('\n') + 1
        if line_count > CODE_LINES_MAX:
            errors.append(f'{label}: {line_count}줄. 코드 블록은 {CODE_LINES_MAX}줄을 넘을 수 없다')
        elif line_count > CODE_LINES_WARN:
            print(f'  주의 {label}: {line_count}줄 (권장 {CODE_LINES_WARN}줄 이하)')
        stdin = None
        following = pre.next_element()
        if following is not None and following.tag == 'pre' and 'stdin' in following.classes():
            stdin = normalize(following.text_content()) + '\n'
            following = following.next_element()
        if following is None or following.tag != 'pre' or 'output' not in following.classes():
            errors.append(f'{label}: 바로 뒤에 <pre class="output"> 가 없다')
            blocks.append(CodeBlock(title, source, stdin, None, index))
            continue
        blocks.append(CodeBlock(title, source, stdin, normalize(following.text_content()), index))
    return blocks


def run_code_blocks(blocks: list[CodeBlock], python: str, errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix='chapter-') as workdir:
        for block in blocks:
            if block.output is None:
                continue
            label = f'코드 {block.index}({block.title})'
            script = Path(workdir) / (block.title or f'block_{block.index}.py')
            script.write_text(block.source + '\n', encoding='utf-8')
            try:
                result = subprocess.run(
                    [python, '-E', '-s', script.name], cwd=workdir, input=block.stdin or '',
                    capture_output=True, text=True, timeout=RUN_TIMEOUT_SEC,
                )
            except subprocess.TimeoutExpired:
                errors.append(f'{label}: {RUN_TIMEOUT_SEC}초 안에 끝나지 않았다')
                continue
            if result.returncode != 0:
                errors.append(f'{label}: 실행 실패\n{indent(result.stderr.strip())}')
                continue
            actual = normalize(result.stdout)
            if actual != block.output:
                errors.append(f'{label}: 출력이 다르다\n--- 적힌 출력\n{indent(block.output)}\n--- 실제 출력\n{indent(actual)}')


def indent(text: str) -> str:
    return '\n'.join('      ' + line for line in text.splitlines())


def check_range(name: str, count: int, bounds: tuple[int, int], errors: list[str]) -> None:
    low, high = bounds
    if not low <= count <= high:
        errors.append(f'{name}: {count}개 (허용 {low}~{high})')


def lint_head(doc: Node, path: Path, errors: list[str]) -> None:
    title_node = doc.find('title')
    title = title_node.text_content().strip() if title_node else ''
    match = TITLE_PATTERN.match(title)
    if not match:
        errors.append(f'<title> 형식: "NN. 제목 — 파이썬 알고리즘 노트" 여야 한다 (현재 "{title}")')
        return
    chapter_no = match.group(1)
    if not path.name.startswith(chapter_no + '-'):
        errors.append(f'<title> 의 장 번호 {chapter_no} 가 파일명 {path.name} 과 다르다')
    body = doc.find('body')
    if body is None or body.attrs.get('data-chapter') != chapter_no:
        errors.append(f'<body data-chapter="{chapter_no}"> 여야 한다')


def lint_sections(article: Node, errors: list[str]) -> None:
    sections = [child for child in article.element_children() if child.tag == 'section']
    for section in sections:
        heading = section.find('h2')
        if 'id' not in section.attrs or heading is None:
            errors.append('모든 <section> 에는 id 와 <h2> 가 있어야 한다')
            return
    tail = sections[-len(TAIL_SECTIONS):]
    for section, (expected_id, expected_title) in zip(tail, TAIL_SECTIONS):
        actual_id, actual_title = section.attrs['id'], section.find('h2').text_content().strip()
        if (actual_id, actual_title) != (expected_id, expected_title):
            errors.append(f'마지막 네 절은 {[t for _, t in TAIL_SECTIONS]} 순서여야 한다 (#{actual_id} "{actual_title}")')
    check_range('개념 절', len(sections) - len(TAIL_SECTIONS), CONCEPT_SECTIONS, errors)
    ids = [node.attrs['id'] for node in article.find_all(attr='id')]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        errors.append(f'id 가 겹친다: {duplicates}')


def lint_components(article: Node, errors: list[str]) -> None:
    if article.find(cls='notice'):
        errors.append('.notice (견본 안내문) 가 남아 있다')
    if article.find(cls='callout-key') is None:
        errors.append('"핵심" callout(.callout-key) 이 없다')
    goals = article.find(cls='goals')
    check_range('이 장에서 배울 것 항목', len(goals.find_all('li')) if goals else 0, GOALS, errors)
    meta = article.find(cls='chapter-meta')
    check_range('chip', len(meta.find_all(cls='chip')) if meta else 0, CHIPS, errors)
    check_range('그림(.fig)', len(article.find_all('figure', cls='fig')), FIGURES, errors)
    by_id = {node.attrs['id']: node for node in article.find_all('section', attr='id')}
    pitfalls, problem, recall, summary = (by_id.get(key) for key, _ in TAIL_SECTIONS)
    if pitfalls:
        check_range('자주 하는 실수 callout', len(pitfalls.find_all(cls='callout-warn')), WARN_CALLOUTS, errors)
    if problem:
        lint_problem(problem, errors)
    if recall:
        questions = recall.find_all('details')
        if len(questions) != RECALL_QUESTIONS or any(q.find('summary') is None or q.find(cls='answer') is None for q in questions):
            errors.append(f'스스로 확인은 summary 와 .answer 를 갖춘 <details> {RECALL_QUESTIONS}개여야 한다')
    if summary:
        items = summary.find('ol', cls='summary-list')
        check_range('정리 항목', len(items.find_all('li')) if items else 0, SUMMARY_ITEMS, errors)
    if article.find('nav', cls='pager') is None:
        errors.append('<nav class="pager"> 가 없다')


def lint_problem(problem: Node, errors: list[str]) -> None:
    if len(problem.find_all(cls='problem')) != 1:
        errors.append('대표 문제(.problem) 는 정확히 하나여야 한다')
    reveals = problem.find_all('details', cls='reveal')
    titles = [r.find('summary').text_content().strip() if r.find('summary') else '' for r in reveals]
    if len(reveals) != len(REVEAL_TITLES) or any(not t.startswith(e) for t, e in zip(titles, REVEAL_TITLES)):
        errors.append(f'대표 문제의 접기는 {REVEAL_TITLES} 순서로 3개여야 한다 (현재 {titles})')


def lint_structure(doc: Node, path: Path, errors: list[str]) -> None:
    lint_head(doc, path, errors)
    article = doc.find('article', cls='chapter')
    if article is None:
        errors.append('<article class="chapter"> 가 없다')
        return
    chars = len(re.sub(r'\s+', '', article.text_content()))
    low, high = CHARS
    if not low <= chars <= high:
        errors.append(f'분량 {chars:,}자 (허용 {low:,}~{high:,}자, 태그·공백 제외)')
    lint_sections(article, errors)
    lint_components(article, errors)


def resolve(name: str) -> Path:
    path = Path(name)
    return path if path.exists() else BOOK_DIR / name


def check(path: Path, python: str, run: bool) -> bool:
    print(f'▶ {path.name}')
    errors: list[str] = []
    doc = parse(path)
    lint_structure(doc, path, errors)
    article = doc.find('article', cls='chapter') or doc
    blocks = collect_code_blocks(article, errors)
    if run:
        run_code_blocks(blocks, python, errors)
    for error in errors:
        print(f'  ✗ {error}')
    if not errors:
        print(f'  OK — 코드 블록 {len(blocks)}개 {"실행·대조" if run else "구조만 검사"}')
    return not errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('files', nargs='+', help='검사할 장 HTML (파일명만 주면 책 폴더에서 찾는다)')
    parser.add_argument('--python', default=sys.executable, help='코드 블록을 실행할 파이썬 (기본: 이 스크립트를 실행한 파이썬)')
    parser.add_argument('--no-run', action='store_true', help='코드를 실행하지 않고 구조만 검사한다')
    args = parser.parse_args()
    results = [check(resolve(name), args.python, not args.no_run) for name in args.files]
    failed = results.count(False)
    print(f'\n{len(results)}개 중 {len(results) - failed}개 통과' + (f', {failed}개 실패' if failed else ''))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
