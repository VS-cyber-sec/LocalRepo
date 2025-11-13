def fractional_knapsack():
    # Step 1: Take number of items
    n = int(input("Enter number of items: "))

    weights = []
    values = []

    # Step 2: Take weight and value separately
    print("\nEnter weights of each item:")
    for i in range(n):
        w = float(input(f"Weight of item {i+1}: "))
        weights.append(w)

    print("\nEnter values of each item:")
    for i in range(n):
        v = float(input(f"Value of item {i+1}: "))
        values.append(v)

    # Step 3: Take knapsack capacity
    capacity = float(input("\nEnter knapsack capacity: "))

    # Step 4: Fractional knapsack logic
    res = 0.0
    items = sorted(zip(weights, values), key=lambda x: x[1] / x[0], reverse=True)

    print("\nItem selection process:")
    for weight, value in items:
        if capacity <= 0:
            break

        if weight <= capacity:
            res += value
            capacity -= weight
            print(f"  Took full item (weight={weight}, value={value})")
        else:
            res += capacity * (value / weight)
            print(f"  Took {capacity} weight fraction of item (weight={weight}, value={value})")
            capacity = 0

    print(f"\nMaximum value in knapsack = {res:.2f}")


if __name__ == "__main__":
    fractional_knapsack()
# time= o(n log n) due to sorting
# space o(n)
# values to profit 
