// 책 전체 목차의 단일 원본.
// 사이드바, 표지의 목차, 장 머리말, 이전/다음 장 링크가 모두 이 데이터로 그려진다.
// 새 장을 쓰면: 해당 장의 isWritten 을 true 로 바꾸고, 같은 slug 이름의 HTML 파일을 만든다.
window.BOOK = {
  title: '파이썬 알고리즘 노트',
  subtitle: '파이썬 기초부터 자료구조와 알고리즘까지, 직접 정리하는 학습서',
  pythonVersion: '3.13',
  parts: [
    {
      no: 1,
      title: '파이썬 기초',
      desc: '알고리즘을 풀기에 충분한 만큼의 파이썬 문법과, 코드의 속도를 재는 빅오 표기법.',
      chapters: [
        { no: '01', slug: '01-basic-syntax', title: '기본 문법과 입출력', desc: '변수와 연산자, 조건문과 반복문, 빠르게 입력 받기', isWritten: true },
        { no: '02', slug: '02-types-and-big-o', title: '자료형과 빅오', desc: '파이썬 자료형의 특징과 시간복잡도를 읽는 법', isWritten: true },
        { no: '03', slug: '03-list-and-tuple', title: '리스트와 튜플', desc: '인덱싱과 슬라이싱, 정렬, 리스트 컴프리헨션', isWritten: true },
        { no: '04', slug: '04-dict-and-set', title: '딕셔너리와 집합', desc: '해시 기반 자료형으로 빠르게 찾고 세기', isWritten: true },
        { no: '05', slug: '05-string', title: '문자열 다루기', desc: '문자열 메서드, 뒤집기, 포맷팅, 문자와 코드값', isWritten: true },
        { no: '06', slug: '06-function-and-recursion', title: '함수와 재귀', desc: '함수와 람다, 재귀 호출과 재귀 깊이 제한', isWritten: true },
        { no: '07', slug: '07-builtin-modules', title: '자주 쓰는 내장 모듈', desc: 'collections, heapq, itertools, bisect', isWritten: true }
      ]
    },
    {
      no: 2,
      title: '선형 자료구조',
      desc: '데이터를 한 줄로 늘어놓는 구조. 배열에서 시작해 해시 테이블까지.',
      chapters: [
        { no: '08', slug: '08-array', title: '배열', desc: '연속된 메모리, 인덱스 접근, 동적 배열이 커지는 방식', isWritten: true },
        { no: '09', slug: '09-linked-list', title: '연결 리스트', desc: '노드와 포인터, 삽입과 삭제, 뒤집기', isWritten: true },
        { no: '10', slug: '10-stack', title: '스택', desc: '나중에 넣은 것을 먼저 꺼내는 구조(LIFO)', isWritten: true },
        { no: '11', slug: '11-queue-and-deque', title: '큐와 데크', desc: '먼저 넣은 것을 먼저 꺼내는 구조(FIFO)와 양방향 데크', isWritten: false },
        { no: '12', slug: '12-hash-table', title: '해시 테이블', desc: '해시 함수와 충돌 처리, 딕셔너리가 빠른 이유', isWritten: false }
      ]
    },
    {
      no: 3,
      title: '비선형 자료구조',
      desc: '데이터가 여러 갈래로 이어지는 구조. 그래프, 트리, 힙, 트라이.',
      chapters: [
        { no: '13', slug: '13-graph-search', title: '그래프와 탐색', desc: '그래프를 표현하는 법, DFS와 BFS', isWritten: false },
        { no: '14', slug: '14-shortest-path', title: '최단 경로', desc: '다익스트라, 벨만-포드, 플로이드-워셜', isWritten: false },
        { no: '15', slug: '15-tree', title: '트리', desc: '트리 용어, 이진 트리, 전위·중위·후위 순회', isWritten: false },
        { no: '16', slug: '16-binary-search-tree', title: '이진 탐색 트리', desc: '정렬된 트리에서 찾기, 넣기, 지우기', isWritten: false },
        { no: '17', slug: '17-heap', title: '힙과 우선순위 큐', desc: '가장 작은 값을 빠르게 꺼내는 완전 이진 트리', isWritten: false },
        { no: '18', slug: '18-trie', title: '트라이', desc: '문자열 접두사를 빠르게 찾는 트리', isWritten: false }
      ]
    },
    {
      no: 4,
      title: '알고리즘',
      desc: '정렬과 탐색부터 그리디, 분할 정복, 다이나믹 프로그래밍까지 문제를 푸는 방법.',
      chapters: [
        { no: '19', slug: '19-sorting', title: '정렬', desc: '선택·삽입·병합·퀵 정렬과 파이썬의 sort', isWritten: false },
        { no: '20', slug: '20-binary-search', title: '이진 탐색', desc: '절반씩 줄여 찾기, 파라메트릭 서치', isWritten: false },
        { no: '21', slug: '21-two-pointers', title: '투 포인터와 슬라이딩 윈도우', desc: '두 위치를 움직여 구간을 한 번에 훑기', isWritten: false },
        { no: '22', slug: '22-backtracking', title: '완전 탐색과 백트래킹', desc: '모든 경우를 보되, 가망 없는 가지는 일찍 자르기', isWritten: false },
        { no: '23', slug: '23-greedy', title: '그리디', desc: '매 순간의 최선이 전체의 최선이 되는 조건', isWritten: false },
        { no: '24', slug: '24-divide-and-conquer', title: '분할 정복', desc: '문제를 쪼개서 풀고 다시 합치기', isWritten: false },
        { no: '25', slug: '25-dynamic-programming', title: '다이나믹 프로그래밍', desc: '겹치는 부분 문제의 답을 저장해 다시 쓰기', isWritten: false },
        { no: '26', slug: '26-bit-manipulation', title: '비트 조작', desc: '비트 연산자와 자주 쓰는 비트 기법', isWritten: false }
      ]
    }
  ]
};
