// 공통 화면 틀: 테마 전환은 모든 페이지에, 나머지(사이드바·상단 막대·절 번호·이 페이지 목차·
// 이전/다음 장·읽기 진행 막대)는 <body data-chapter="NN"> 인 장 페이지에서만 그린다.
(function () {
  var THEME_KEY = 'pyalgo-theme';
  var READING_CHARS_PER_MIN = 500;     // 한국어 설명문을 읽는 대략적인 속도
  var ACTIVE_SECTION_RATIO = 0.3;      // 제목이 화면 위쪽 30% 안으로 들어오면 "지금 읽는 절"로 본다
  var TOAST_VISIBLE_MS = 2400;         // "준비 중" 알림을 읽을 만큼만 띄웠다가 지운다

  var ICONS = {
    moon: '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    sun: '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
  };

  var book = window.BOOK;

  function escapeHtml(text) {
    return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function chapterHref(chapter) {
    return chapter.slug + '.html';
  }

  /** 링크가 없는 "예정" 장 요소에 붙이는 속성. 누르면 준비 중 알림에 이 이름이 뜬다. */
  function plannedAttr(chapter) {
    return ' data-planned="' + escapeHtml(chapter.no + '. ' + chapter.title) + '"';
  }

  /** 모든 장을 순서대로 [{part, chapter}] 로 펼친다. 이전/다음 장 계산에 쓴다. */
  function flattenChapters() {
    var entries = [];
    book.parts.forEach(function (part) {
      part.chapters.forEach(function (chapter) { entries.push({ part: part, chapter: chapter }); });
    });
    return entries;
  }

  // ---------- 테마 ----------
  function currentTheme() {
    var explicitTheme = document.documentElement.getAttribute('data-theme');
    if (explicitTheme) return explicitTheme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function toggleTheme() {
    var nextTheme = currentTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    try {
      localStorage.setItem(THEME_KEY, nextTheme);
    } catch (e) {
      console.warn('[app.js] 테마를 저장하지 못했다. 이번 방문에만 적용된다.', e);
    }
  }

  function themeButtonHtml() {
    return '<button type="button" class="icon-btn" data-theme-toggle aria-label="라이트/다크 전환" title="라이트/다크 전환">' +
      ICONS.moon + ICONS.sun + '</button>';
  }

  function setupThemeButtons() {
    document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
      button.addEventListener('click', toggleTheme);
    });
  }

  // ---------- 사이드바와 상단 막대 ----------
  function brandHtml() {
    return '<a class="brand" href="index.html"><span class="brand-mark">Py</span>' +
      '<span class="brand-text"><span class="brand-title">' + escapeHtml(book.title) + '</span>' +
      '<span class="brand-sub">자료구조 · 알고리즘 학습 노트</span></span></a>';
  }

  function tocItemHtml(chapter, currentNo) {
    var isCurrent = chapter.no === currentNo;
    var searchText = escapeHtml(chapter.no + ' ' + chapter.title + ' ' + chapter.desc);
    var inner = '<span class="n">' + chapter.no + '</span><span>' + escapeHtml(chapter.title) + '</span>';
    var stateClass = isCurrent ? ' is-current' : (chapter.isWritten ? '' : ' is-planned');
    if (chapter.isWritten) {
      return '<a class="toc-item' + stateClass + '" href="' + chapterHref(chapter) + '" data-search="' + searchText + '"' +
        (isCurrent ? ' aria-current="page"' : '') + '>' + inner + '</a>';
    }
    // 아직 파일이 없는 장은 링크를 걸지 않는다. 견본 페이지처럼 "현재 장"이어도 마찬가지다.
    return '<span class="toc-item' + stateClass + '" data-search="' + searchText + '"' + plannedAttr(chapter) +
      (isCurrent ? ' aria-current="page"' : ' title="아직 작성 전인 장"') + '>' + inner + '</span>';
  }

  function renderSidebar(sidebar, currentNo) {
    var partsHtml = book.parts.map(function (part) {
      return '<div class="toc-part" data-part="' + part.no + '">' +
        '<p class="toc-part-title">' + part.no + '부 · ' + escapeHtml(part.title) + '</p>' +
        part.chapters.map(function (chapter) { return tocItemHtml(chapter, currentNo); }).join('') + '</div>';
    }).join('');
    sidebar.innerHTML =
      '<div class="side-head">' + brandHtml() + themeButtonHtml() + '</div>' +
      '<label class="search">' +
      '<input type="search" id="toc-search" placeholder="장 제목으로 찾기" autocomplete="off" aria-label="목차 검색"><kbd>/</kbd></label>' +
      '<nav class="toc" aria-label="책 목차">' + partsHtml + '<p class="toc-empty" hidden>찾는 장이 없습니다.</p></nav>' +
      '<div class="side-foot"><a href="index.html">표지와 전체 목차</a> · Python ' + escapeHtml(book.pythonVersion) + ' 기준</div>';
  }

  function renderTopbar(topbar) {
    topbar.innerHTML = '<button type="button" class="icon-btn" id="menu-btn" aria-label="목차 열기" aria-expanded="false">' +
      ICONS.menu + '</button>' + brandHtml() + themeButtonHtml();
  }

  function setDrawerOpen(isOpen) {
    document.body.classList.toggle('is-drawer-open', isOpen);
    var menuButton = document.getElementById('menu-btn');
    if (menuButton) menuButton.setAttribute('aria-expanded', String(isOpen));
  }

  function setupDrawer(sidebar) {
    var menuButton = document.getElementById('menu-btn');
    var backdrop = document.getElementById('backdrop');
    if (menuButton) menuButton.addEventListener('click', function () {
      setDrawerOpen(!document.body.classList.contains('is-drawer-open'));
    });
    if (backdrop) backdrop.addEventListener('click', function () { setDrawerOpen(false); });
    sidebar.addEventListener('click', function (event) {
      if (event.target.closest('a')) setDrawerOpen(false);
    });
  }

  function setupSearch(sidebar) {
    var input = sidebar.querySelector('#toc-search');
    var emptyMessage = sidebar.querySelector('.toc-empty');
    input.addEventListener('input', function () {
      var query = input.value.trim().toLowerCase();
      var visibleCount = 0;
      sidebar.querySelectorAll('.toc-part').forEach(function (part) {
        var partVisibleCount = 0;
        part.querySelectorAll('.toc-item').forEach(function (item) {
          var isMatch = !query || item.dataset.search.toLowerCase().indexOf(query) !== -1;
          item.hidden = !isMatch;
          if (isMatch) partVisibleCount += 1;
        });
        part.hidden = partVisibleCount === 0;
        visibleCount += partVisibleCount;
      });
      emptyMessage.hidden = visibleCount > 0;
    });
  }

  function setupKeyboard() {
    document.addEventListener('keydown', function (event) {
      var isTyping = /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName);
      if (event.key === '/' && !isTyping) {
        var input = document.getElementById('toc-search');
        if (!input) return;
        event.preventDefault();
        if (window.matchMedia('(max-width: 959px)').matches) setDrawerOpen(true);
        input.focus();
      } else if (event.key === 'Escape') {
        setDrawerOpen(false);
      }
    });
  }

  // ---------- 작성 전인 장 안내 ----------
  /** 알림 상자는 미리 만들어 둔다. 스크린 리더는 이미 있던 role="status" 상자의 내용 변화만 읽어 준다. */
  function setupPlannedNotice() {
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'status');
    document.body.appendChild(toast);
    var hideTimer = null;

    document.addEventListener('click', function (event) {
      var item = event.target.closest('[data-planned]');
      if (!item) return;
      toast.innerHTML = '<b>' + escapeHtml(item.getAttribute('data-planned')) + '</b><span>아직 준비 중인 장입니다.</span>';
      toast.classList.add('is-visible');
      clearTimeout(hideTimer);
      hideTimer = setTimeout(function () { toast.classList.remove('is-visible'); }, TOAST_VISIBLE_MS);
    });
  }

  // ---------- 장 본문 ----------
  function fillChapterHead(entry, article) {
    var pill = article.querySelector('.part-pill');
    if (pill) {
      pill.textContent = entry.part.no + '부 · ' + entry.part.title;
      pill.href = 'index.html#part-' + entry.part.no;
    }
    var label = article.querySelector('.chapter-label');
    if (label) label.textContent = 'Chapter ' + entry.chapter.no;
    var meta = article.querySelector('.chapter-meta');
    if (meta) {
      var minutes = Math.max(1, Math.round(article.textContent.replace(/\s+/g, '').length / READING_CHARS_PER_MIN));
      meta.insertAdjacentHTML('afterbegin', '<span>읽는 시간 약 ' + minutes + '분</span><span class="sep"></span>');
    }
  }

  /** 장의 최상위 절(h2)에 "10.1" 같은 번호를 붙이고, 이 페이지 목차용으로 돌려준다. */
  function numberSections(article, chapterNo) {
    var headings = Array.prototype.slice.call(article.querySelectorAll(':scope > section > h2'));
    headings.forEach(function (heading, i) {
      var section = heading.parentElement;
      if (!heading.id) heading.id = section.id || 'sec-' + (i + 1);
      heading.insertAdjacentHTML('afterbegin', '<span class="sec-no">' + Number(chapterNo) + '.' + (i + 1) + '</span>');
    });
    return headings;
  }

  function renderOnThisPage(nav, headings) {
    nav.innerHTML = headings.map(function (heading) {
      return '<a href="#' + heading.id + '">' + heading.innerHTML + '</a>';
    }).join('');
    return Array.prototype.slice.call(nav.querySelectorAll('a'));
  }

  function pagerCardHtml(entry, direction) {
    var label = direction === 'prev' ? '← 이전 장' : '다음 장 →';
    var body = '<span class="pager-dir">' + label + (entry.chapter.isWritten ? '' : ' · 작성 예정') + '</span>' +
      '<span class="pager-title"><span class="n">' + entry.chapter.no + '</span>' + escapeHtml(entry.chapter.title) + '</span>';
    if (entry.chapter.isWritten) {
      return '<a class="pager-card ' + direction + '" href="' + chapterHref(entry.chapter) + '">' + body + '</a>';
    }
    return '<div class="pager-card ' + direction + ' is-planned"' + plannedAttr(entry.chapter) + '>' + body + '</div>';
  }

  function renderPager(pager, entries, index) {
    var html = '';
    if (index > 0) html += pagerCardHtml(entries[index - 1], 'prev');
    if (index < entries.length - 1) html += pagerCardHtml(entries[index + 1], 'next');
    pager.innerHTML = html;
  }

  /** 스크롤 한 번에 읽기 진행 막대와 "지금 읽는 절" 표시를 함께 갱신한다. */
  function setupScrollTracking(headings, railLinks) {
    var bar = document.querySelector('.progress span');
    var isScheduled = false;
    function update() {
      isScheduled = false;
      var scrollable = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = 'scaleX(' + (scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0) + ')';
      var activeLine = window.innerHeight * ACTIVE_SECTION_RATIO;
      var activeIndex = -1;
      headings.forEach(function (heading, i) {
        if (heading.getBoundingClientRect().top <= activeLine) activeIndex = i;
      });
      railLinks.forEach(function (link, i) { link.classList.toggle('is-active', i === activeIndex); });
    }
    window.addEventListener('scroll', function () {
      if (!isScheduled) { isScheduled = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  function initChapterPage(chapterNo) {
    var entries = flattenChapters();
    var index = entries.findIndex(function (entry) { return entry.chapter.no === chapterNo; });
    if (index === -1) {
      console.error('[app.js] book.js 에 없는 장 번호다: ' + chapterNo);
      return;
    }
    var entry = entries[index];
    document.body.setAttribute('data-part', String(entry.part.no));

    var sidebar = document.getElementById('sidebar');
    renderSidebar(sidebar, chapterNo);
    renderTopbar(document.getElementById('topbar'));
    setupDrawer(sidebar);
    setupSearch(sidebar);
    setupKeyboard();

    var article = document.querySelector('.chapter');
    fillChapterHead(entry, article);
    var headings = numberSections(article, chapterNo);
    var railNav = document.getElementById('onthispage');
    var railLinks = railNav ? renderOnThisPage(railNav, headings) : [];
    var pager = article.querySelector('.pager');
    if (pager) renderPager(pager, entries, index);
    setupScrollTracking(headings, railLinks);
  }

  if (!book) {
    console.error('[app.js] book.js 를 app.js 보다 먼저 불러와야 한다.');
    return;
  }
  var chapterNo = document.body.getAttribute('data-chapter');
  if (chapterNo) initChapterPage(chapterNo);
  setupThemeButtons();
  setupPlannedNotice();

  // 표지(home.js)가 같은 도우미를 다시 쓰도록 내보낸다.
  window.PyAlgo = { escapeHtml: escapeHtml, chapterHref: chapterHref, plannedAttr: plannedAttr };
})();
