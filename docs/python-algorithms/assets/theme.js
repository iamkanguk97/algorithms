// <head>에서 동기로 불러, 첫 화면부터 저장된 테마를 적용한다 (흰 화면 깜빡임 방지).
(function () {
  try {
    var savedTheme = localStorage.getItem('pyalgo-theme');
    if (savedTheme === 'light' || savedTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', savedTheme);
    }
  } catch (e) {
    // 저장소가 막힌 환경(시크릿 창 등)에서는 시스템 설정을 그대로 따른다.
  }
})();
