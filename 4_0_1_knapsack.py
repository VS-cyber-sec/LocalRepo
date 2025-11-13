def knapsack_dp():
    # Step 1: Take user input
    n = int(input("Enter number of items: "))

    weights = []
    profits = []

    # Step 2: Take input for weights separately
    print("\nEnter weight of each item:")
    for i in range(n):
        w = int(input(f"Weight of item {i+1}: "))
        weights.append(w)

    # Step 3: Take input for profits separately
    print("\nEnter profit of each item:")
    for i in range(n):
        p = int(input(f"Profit of item {i+1}: "))
        profits.append(p)

    # Step 4: Take maximum capacity of knapsack
    W = int(input("\nEnter maximum capacity of knapsack: "))

    # Step 5: Create DP table
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Step 6: Build table bottom-up
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if weights[i - 1] <= w:
                include = profits[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]
                dp[i][w] = max(include, exclude)
            else:
                dp[i][w] = dp[i - 1][w]

    # Step 7: Output the result
    print("\nMaximum profit that can be obtained:", dp[n][W])


if __name__ == "__main__":
    knapsack_dp()
# time = o(nxw)  two nested loop
# space = o(nxw)  the dp table
