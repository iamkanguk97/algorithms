// 코드 블록 꾸미기: <pre data-lang="python" data-title="파일명.py"><code>…</code></pre> 를 찾아
// 머리줄(파일명 + 복사 버튼), 줄 번호, 파이썬 문법 색을 입힌다.
// 바로 뒤에 <pre class="stdin"> 이 있으면 "입력" 칸으로, <pre class="output"> 이 있으면 "실행 결과" 칸으로
// 같은 상자 아래쪽에 합친다. 둘 다 있을 때는 stdin 을 먼저 쓴다.
(function () {
  var PY_KEYWORDS = new Set((
    'and as assert async await break class continue def del elif else except finally for from ' +
    'global if import in is lambda nonlocal not or pass raise return try while with yield match case'
  ).split(' '));
  var PY_CONSTANTS = new Set(['True', 'False', 'None']);
  var PY_BUILTINS = new Set((
    'abs all any bin bool chr dict divmod enumerate filter float format frozenset hash hex id input int ' +
    'isinstance iter len list map max min next object oct open ord pow print range repr reversed round ' +
    'set slice sorted str sum super tuple type zip'
  ).split(' '));

  // 순서가 중요하다: 주석 → 문자열 → 숫자 → 데코레이터 → 이름. 먼저 맞는 쪽이 이긴다.
  var TOKEN_PATTERN = new RegExp([
    '(#[^\\n]*)',
    '((?:[rRbBuUfF]{1,2})?(?:"""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\'|"(?:\\\\.|[^"\\\\\\n])*"|\'(?:\\\\.|[^\'\\\\\\n])*\'))',
    '(\\b\\d[\\d_]*(?:\\.\\d+)?(?:[eE][+-]?\\d+)?\\b)',
    '(@[A-Za-z_]\\w*)',
    '([A-Za-z_]\\w*)'
  ].join('|'), 'g');

  var COPY_FEEDBACK_MS = 1600;

  function classifyName(name, previousName, nextChar) {
    if (previousName === 'def' || previousName === 'class') return 'tk-fn';
    if (PY_CONSTANTS.has(name)) return 'tk-const';
    if (PY_KEYWORDS.has(name)) return 'tk-kw';
    if (name === 'self' || name === 'cls') return 'tk-self';
    if (PY_BUILTINS.has(name) && nextChar === '(') return 'tk-bi';
    return '';
  }

  /** 파이썬 소스를 [{cls, text}] 토큰 목록으로 나눈다. cls 가 빈 문자열이면 색을 입히지 않는다. */
  function tokenizePython(source) {
    var tokens = [];
    var lastIndex = 0;
    var previousName = '';
    var match;
    TOKEN_PATTERN.lastIndex = 0;
    while ((match = TOKEN_PATTERN.exec(source)) !== null) {
      if (match.index > lastIndex) tokens.push({ cls: '', text: source.slice(lastIndex, match.index) });
      var cls = '';
      if (match[1]) cls = 'tk-com';
      else if (match[2]) cls = 'tk-str';
      else if (match[3]) cls = 'tk-num';
      else if (match[4]) cls = 'tk-dec';
      else {
        cls = classifyName(match[5], previousName, source.charAt(TOKEN_PATTERN.lastIndex));
        previousName = match[5];
      }
      tokens.push({ cls: cls, text: match[0] });
      lastIndex = TOKEN_PATTERN.lastIndex;
    }
    if (lastIndex < source.length) tokens.push({ cls: '', text: source.slice(lastIndex) });
    return tokens;
  }

  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /** 토큰을 줄 단위 <span class="ln"> 으로 묶는다. 여러 줄 문자열도 줄마다 같은 색을 유지한다. */
  function renderLines(tokens) {
    var lines = [''];
    tokens.forEach(function (token) {
      token.text.split('\n').forEach(function (part, i) {
        if (i > 0) lines.push('');
        if (!part) return;
        var html = escapeHtml(part);
        lines[lines.length - 1] += token.cls ? '<span class="' + token.cls + '">' + html + '</span>' : html;
      });
    });
    return lines.map(function (line) { return '<span class="ln">' + (line || ' ') + '</span>'; }).join('');
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      var isCopied = document.execCommand('copy');
      document.body.removeChild(area);
      if (isCopied) resolve(); else reject(new Error('execCommand copy failed'));
    });
  }

  function createCopyButton(source) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-btn';
    button.textContent = '복사';
    button.setAttribute('aria-label', '코드 복사');
    button.addEventListener('click', function () {
      copyText(source).then(function () {
        button.textContent = '복사됨';
        button.classList.add('is-done');
      }, function (error) {
        console.error('[code.js] 복사 실패:', error);
        button.textContent = '복사 실패';
      }).then(function () {
        setTimeout(function () {
          button.textContent = '복사';
          button.classList.remove('is-done');
        }, COPY_FEEDBACK_MS);
      });
    });
    return button;
  }

  function buildHead(pre, source) {
    var head = document.createElement('div');
    head.className = 'code-head';
    var title = document.createElement('span');
    title.className = 'code-title';
    title.textContent = pre.dataset.title || (pre.dataset.lang === 'python' ? 'Python' : pre.dataset.lang);
    head.appendChild(title);
    head.appendChild(createCopyButton(source));
    return head;
  }

  // 코드 상자 아래에 붙이는 칸. 입력 예시가 있으면 실행 결과보다 먼저 온다.
  var ATTACHED_PANELS = [
    { selector: 'pre.stdin', label: '입력' },
    { selector: 'pre.output', label: '실행 결과' }
  ];

  function attachPanels(box) {
    ATTACHED_PANELS.forEach(function (panelSpec) {
      var next = box.nextElementSibling;
      if (!next || !next.matches(panelSpec.selector)) return;
      var panel = document.createElement('div');
      panel.className = 'code-output';
      panel.innerHTML = '<span class="code-output-label">' + panelSpec.label + '</span>';
      panel.appendChild(next);
      box.appendChild(panel);
    });
  }

  function enhanceCodeBlock(pre) {
    var code = pre.querySelector('code') || pre;
    // 소스 첫 줄 앞뒤의 빈 줄은 HTML 작성 편의로 생긴 것이라 지운다.
    var source = code.textContent.replace(/^\n+|\s+$/g, '');
    if (pre.dataset.lang === 'python') {
      code.innerHTML = renderLines(tokenizePython(source));
    } else {
      code.innerHTML = renderLines([{ cls: '', text: source }]);
    }
    var box = document.createElement('div');
    box.className = 'code';
    pre.parentNode.insertBefore(box, pre);
    box.appendChild(buildHead(pre, source));
    box.appendChild(pre);
    attachPanels(box);
  }

  function trimOutputs() {
    document.querySelectorAll('pre.stdin, pre.output').forEach(function (pre) {
      pre.textContent = pre.textContent.replace(/^\n+|\s+$/g, '');
    });
  }

  trimOutputs();
  document.querySelectorAll('pre[data-lang]').forEach(enhanceCodeBlock);
})();
