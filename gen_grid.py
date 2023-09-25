from build_maze import buildMaze

def gen_grid(worlds):
    print("here")
    adjNode = [0,0]
    stack = []
    stack.append(adjNode)
    #visited[adjNode[0]][adjNode[1]] = 1
    maze_list=[]
    for var in range(worlds):
        maze_arr = []
        rows, cols = 101,101
        maze_arr = [([0]*cols) for i in range(rows)]
        visited = [([0]*cols) for i in range(rows)]
        #known_world = []
        buildMaze(maze_arr, adjNode, visited)
        maze_list.append(maze_arr)
        print(str(var)+"building maze")
    return maze_list