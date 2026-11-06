# https://jungol.co.kr/problem/1161?cursor=IjYiLDgsNA==

def hanoi(n, start, via, end):
    if n == 0:
        return
    hanoi(n-1, start, end, via) # 시작점에서 마지막 원판 빼고 나머지 원판들을 한꺼번에 중간에 잠깐 넣어놓음
    print(f"{n} : {start} -> {end}") # 큰 원판을 마지막 기둥으로 옮기기
    hanoi(n-1, via, start, end) # 중간에 넣어놓은걸 마지막 기둥으로 옮기기

n = int(input())
hanoi(n, 1, 2, 3)