def print_board(board):
    for row in board:
        print(" ".join("Q" if x else "." for x in row))
    print()

def is_safe(board, row, col, n):
    # Check all existing queens anywhere on the board
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1 and not (r == row and c == col):
                if c == col or r == row or abs(r - row) == abs(c - col):
                    return False
    return True

def solve(board, row, n):
    if row == n:
        print_board(board)
        return
    # If a queen is already in this row (pre-placed), validate it and move on
    if 1 in board[row]:
        col = board[row].index(1)
        if is_safe(board, row, col, n):
            solve(board, row + 1, n)
        return
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            solve(board, row + 1, n)
            board[row][col] = 0

def n_queens():
    try:
        n = int(input("Enter N: ").strip())
        if n <= 0:
            print("N must be positive."); return
    except ValueError:
        print("Invalid N."); return

    board = [[0]*n for _ in range(n)]
    pos = input("Enter first queen position (row col) or press Enter to skip: ").strip()
    if pos:
        try:
            r, c = map(int, pos.split())
            if not (1 <= r <= n and 1 <= c <= n):
                print("Position out of range."); return
            board[r-1][c-1] = 1
        except ValueError:
            print("Invalid position format."); return

    print("\nInitial board:")
    print_board(board)
    print("Solutions:\n")
    solve(board, 0, n)

if __name__ == "__main__":
    n_queens()
# space o(n 2)
