import numpy as np
import sys
import timeit

sys.setrecursionlimit(1000000000)
#Declaring Global Variables
maze_arr = []

rows, cols = 101,101
maze_arr = [([0]*cols) for i in range(rows)]
visited = [([0]*cols) for i in range(rows)]
known_world = []
adjNode = [0,0]
stack = []
stack.append(adjNode)
visited[adjNode[0]][adjNode[1]] = 1


def emptyList(list):
  if list == []:
    return True
  else:
    return False
    
def next_cell(maze_arr, row, col, visited):
    neighbors_index = np.array([[-1,-1]])
    
    if(row <= 0 and col <= 0):
        # print("row 0 col 0")
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row+1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
            
        if(visited[row][col+1] == 0):
            arr1 = np.array([[row, col+1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
    
    elif(row >= len(maze_arr)-1 and col >= len(maze_arr)-1):
        # print("last row last col")
        if(visited[row-1][col] == 0):
            arr1 = np.array([[(row-1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[(row), col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
      
    elif(row >= len(maze_arr)-1 and col <= 0):
        # print("last row first col")
        if(visited[row-1][col] == 0):
            arr1 = np.array([[(row-1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col+1] == 0):
            arr1 = np.array([[(row), col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    elif(row <= 0 and col >= len(maze_arr)-1):
        # print("last col first row")
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row-1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[(row), col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    elif(row <= 0):
        # print("first row")
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row+1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[row, col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col+1] == 0):
            arr1 = np.array([[row, col+1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    elif(col <= 0):
        # print("first col")
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row+1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row-1][col] == 0):
            arr1 = np.array([[row-1, col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col+1] == 0):
            arr1 = np.array([[row, col+1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    elif(col >= len(maze_arr)-1):
        # print("last col")
        if(visited[row-1][col] == 0):
            arr1 = np.array([[(row-1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[(row), col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row+1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    elif(row >= len(maze_arr)-1):
        # print("last row")
        if(visited[row-1][col] == 0):
            arr1 = np.array([[(row-1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[(row), col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col+1] == 0):
            arr1 = np.array([[(row), col+1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))

    else:
        # print("else")
        if(visited[row+1][col] == 0):
            arr1 = np.array([[(row+1), col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row-1][col] == 0):
            arr1 = np.array([[row-1, col]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col+1] == 0):
            arr1 = np.array([[row, col+1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
        if(visited[row][col-1] == 0):
            arr1 = np.array([[row, col-1]])
            neighbors_index = np.concatenate((neighbors_index, arr1))
    
    neighbors_index = np.delete(neighbors_index, 0, 0)
    return neighbors_index

def random_cell(neighbors_index):
    if (len(neighbors_index) == 0):
        return []
    else:
        randomRow = np.random.randint(0, len(neighbors_index), size=1)
        return neighbors_index[randomRow][0]

def CallRandomCell(visited):
    for i in range(len(visited)):
        for j in range(len(visited[i])):
            if visited[i][j]==0:
                return [i,j]

def buildMaze(maze_arr, adjNode, visited):
    # selecting neighbor node to visit, that has not yet been visited
    allNeighbors = next_cell(maze_arr, adjNode[0], adjNode[1], visited)
    adjNode = random_cell(allNeighbors)
    
    # ALL neighbors have been visited! so adjNode will be empty!!
    if emptyList(adjNode):
        # backtracking to parent nodes because all the neighbors of the current node have been visited
        # pop from stack
        if emptyList(stack):
            # restart from a random cell that has not been visited
            randomCell = CallRandomCell(visited)
            if randomCell is None:
                # all nodes have been visited!
                return maze_arr
            else:
                visited[randomCell[0]][randomCell[1]] = 1
                # mark the cell as blocked or unblocked
                probability = np.random.choice(np.arange(0, 2), p=[0.7, 0.3])
                if probability == 0: #unblocked
                    stack.append(randomCell)
                    maze_arr[randomCell[0]][randomCell[1]] = 0
                    buildMaze(maze_arr, randomCell, visited)
                else: #blocked
                    maze_arr[randomCell[0]][randomCell[1]] = 1
                    buildMaze(maze_arr, randomCell, visited)
    
        # stack is not empty, hence pop from the stack
        else:
            adjNode = stack.pop()
            # again implement the DFS algo by searching the unvisited neighbors of the parent!
            buildMaze(maze_arr, adjNode, visited)
    else:
        
        visited[adjNode[0]][adjNode[1]] = 1
        # mark the cell as blocked or unblocked
        probability = np.random.choice(np.arange(0, 2), p=[0.7, 0.3])
        if probability == 0: #unblocked
            stack.append(adjNode)
            maze_arr[adjNode[0]][adjNode[1]] = 0
            buildMaze(maze_arr, adjNode, visited)
        else: #blocked
            maze_arr[adjNode[0]][adjNode[1]] = 1
            buildMaze(maze_arr, adjNode, visited)
        
    