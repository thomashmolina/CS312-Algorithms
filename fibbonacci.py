# polynomial time
def fibbonacci(n: int) -> int:
    if n == 0:
        return 0
    arr = [0 for x in range(n+1)]
    arr[0] = 0
    arr[1] = 1
    for i in range(2, len(arr)):
        arr[i] = arr[i-1] + arr[i-2]
    return arr[i]


print(fibbonacci(3))
