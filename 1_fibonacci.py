# Program to calculate Fibonacci numbers (Recursive and Non-Recursive)
# and analyze their time and space complexity

import time

# ---------- Recursive Fibonacci ----------
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# ---------- Non-Recursive Fibonacci ----------
def fib_iterative(n):
    a, b = 0, 1
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    series = [0, 1]
    for i in range(2, n):
        series.append(series[-1] + series[-2])
    return series

# ---------- Main Program ----------
def main():
    n = int(input("Enter number of terms: "))

    # Recursive method (prints nth term only)
    start = time.time()
    rec_series = [fib_recursive(i) for i in range(n)]
    end = time.time()
    rec_time = end - start

    # Iterative method
    start = time.time()
    iter_series = fib_iterative(n)
    end = time.time()
    iter_time = end - start

    # Display results
    print("\nFibonacci Series using Recursive Method:",rec_series)
    print(f"Time taken (recursive): {rec_time:.6f} seconds")
    print("Time Complexity: O(2^n)")     #uppr bound
    print("Space Complexity: O(n)")         #depth upto n

    print("\nFibonacci Series using Non-Recursive (Iterative) Method:",iter_series)
    print(f"Time taken (iterative): {iter_time:.6f} seconds")
    print("Time Complexity: O(n)")         #single loop
    print("Space Complexity: O(1)")

# ---------- Run ----------
if __name__ == "__main__":
    main()
