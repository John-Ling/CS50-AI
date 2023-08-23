def main():
    arr = [[1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8],
           [1, 2, 3, 4, 5, 6, 7, 8]]
    print(get_neighbors((0, 0)))

def get_neighbors(cell):
    """
    Attempts to extract a cell's neighbors within a 3x3 square
    """
    GRID_SIZE = 8

    startCell = [cell[0] - 1, cell[1] - 1]
    cells = set()

    startCountI = 0 # How many rows are missing due to being out of bounds
    startCountJ = 0 # How many colunmns are missing due to being out of bounds

    # Check if left upper vertical cell is out of bounds and adjust if so
    if cell[0] - 1 < 0: 
        startCell[0] = cell[0]
        startCountI += 1
    if cell[1] - 1 < 0: 
        startCell[1] = cell[1]
        startCountJ += 1

    indexI = startCell[0]
    countI = startCountI
    while indexI < GRID_SIZE and countI != 3:
        countJ = startCountJ
        indexJ = startCell[1]
        while indexJ < GRID_SIZE and countJ != 3:
            cells.add((indexI, indexJ))
            countJ += 1
            indexJ += 1

        indexI += 1
        countI += 1
    
    return cells

if __name__ == "__main__":
    main() 