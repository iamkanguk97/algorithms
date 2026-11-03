def factorial(n):
    if n <= 1:
        print("{}! = 1".format(n))
        return 1
    print("{}! = {} * {}!".format(n, n, n - 1))
    return n * factorial(n - 1)

n = int(input())
print(factorial(n))