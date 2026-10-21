// 표지(index.html) 전용: book.js 데이터로 숫자 요약, 부 카드, 전체 목차를 그린다.
(function () {
  var book = window.BOOK;
  var helpers = window.PyAlgo;
  if (!book || !helpers) {
    console.error('[home.js] book.js 와 app.js 를 먼저 불러와야 한다.');
    return;
  }
  var escapeHtml = helpers.escapeHtml;

  function countChapters() {
    var total = 0;
    var written = 0;
    book.parts.forEach(function (part) {
      part.chapters.forEach(function (chapter) {
        total += 1;
        if (chapter.isWritten) written += 1;
      });
    });
    return { total: total, written: written };
  }

  function renderStats(container) {
    var counts = countChapters();
    var percent = counts.total ? Math.round((counts.written / counts.total) * 100) : 0;
    container.innerHTML =
      '<div><dt>부</dt><dd>' + book.parts.length + '</dd></div>' +
      '<div><dt>장</dt><dd>' + counts.total + '</dd></div>' +
      '<div class="stat-progress"><dt>작성한 장</dt><dd>' + counts.written + '<small> / ' + counts.total + '</small></dd>' +
      '<span class="meter" role="img" aria-label="작성 진행률 ' + percent + '%"><span style="width:' + percent + '%"></span></span></div>';
  }

  function chapterRange(part) {
    var first = part.chapters[0].no;
    var last = part.chapters[part.chapters.length - 1].no;
    return first + '–' + last;
  }

  function renderParts(container) {
    container.innerHTML = book.parts.map(function (part) {
      return '<a class="part-card" data-part="' + part.no + '" href="#part-' + part.no + '">' +
        '<span class="part-card-no">' + part.no + '</span>' +
        '<span class="part-card-kicker">Part ' + part.no + '</span>' +
        '<h3>' + escapeHtml(part.title) + '</h3>' +
        '<p>' + escapeHtml(part.desc) + '</p>' +
        '<span class="part-card-foot">' + part.chapters.length + '개 장 · ' + chapterRange(part) + '</span></a>';
    }).join('');
  }

  function contentsRowHtml(chapter) {
    var body = '<span class="n">' + chapter.no + '</span>' +
      '<span class="t"><span class="t-title">' + escapeHtml(chapter.title) + '</span>' +
      '<span class="t-desc">' + escapeHtml(chapter.desc) + '</span></span>' +
      '<span class="status">' + (chapter.isWritten ? '읽기 →' : '예정') + '</span>';
    if (chapter.isWritten) {
      return '<li><a class="contents-row" href="' + helpers.chapterHref(chapter) + '">' + body + '</a></li>';
    }
    return '<li><div class="contents-row is-planned"' + helpers.plannedAttr(chapter) + '>' + body + '</div></li>';
  }

  function renderContents(container) {
    container.innerHTML = book.parts.map(function (part) {
      return '<div class="contents-part" id="part-' + part.no + '" data-part="' + part.no + '">' +
        '<div class="contents-part-head"><span class="contents-part-no">' + part.no + '부</span>' +
        '<div><h3>' + escapeHtml(part.title) + '</h3><p>' + escapeHtml(part.desc) + '</p></div></div>' +
        '<ol class="contents-list">' + part.chapters.map(contentsRowHtml).join('') + '</ol></div>';
    }).join('');
  }

  var stats = document.getElementById('home-stats');
  var parts = document.getElementById('home-parts');
  var contents = document.getElementById('home-contents');
  if (stats) renderStats(stats);
  if (parts) renderParts(parts);
  if (contents) renderContents(contents);
})();
