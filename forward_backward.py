from viz import *
import numpy as np
import sys
sys.setrecursionlimit(1000000000)
import timeit

def get_dist(i, j, dim):  
    return abs(dim-1-i)+abs(dim-1-j) #Manhattan distance

# insertion into priority queue (Fringe)
def openList(i, j, fringe, f): 

    # if len of fringe == 0, then only append into the priority queue!
    if len(fringe) == 0:
        fringe.append((i,j))
    # else 
    else:
        for x in range(len(fringe)):
            (I,J) = fringe[x]
            if f[I][J] > f[i][j]:
                fringe.insert(x, (i,j))
                return
        fringe.append((i,j))

def find_path(parent, dim, si, sj, traversal): #used to find the path from the parent data structure
    if(traversal == 'F'):
        i,j = dim-1, dim-1
        path = [(dim-1, dim-1)]
    elif(traversal == 'B'):
        i,j = 0, 0
        path = [(0, 0)]
    
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

def search_size(parent, dim): #used to find the size of the search tree that was discovered
    ans = 0
    for i in parent:
        for j in i:
            if j == -1:
                ans = ans + 1
    return ((dim * dim) - ans)

def a_star(dim, grid, si, sj, traversal):
    
    result = False
    
    # data structure to store g(n) (list of lists). initialized with -1 for now
    g = [[-1 for i in range(dim)] for j in range(dim)]
    g[si][sj] = 0
    
    # data structure to store h(n) (list of lists).
    h = [[get_dist(i,j,dim) for i in range(dim)] for j in range(dim)] 
    
    # data structure to store f(n) (list of lists). initialized with -1 for now
    f = [[-1 for i in range(dim)] for j in range(dim)] 
    f[si][sj] = g[si][sj]+h[si][sj]

    # data structure to store pointers to parent (list of lists). initialized with -1 for now
    p = [[-1 for i in range(dim)] for j in range(dim)] 
    p[si][sj] = 0
    
    
    # pushing the start node into the fringe
    fringe = [(si,sj)] 
    
    while len(fringe) != 0:
        
        (i,j) = fringe.pop(0)
        # true if goal node is reached
        # goal node set to [dim-1,dim-1]
        if(traversal == 'F'):
            if (i,j) == (dim-1, dim-1): 
                result = True
                break
        elif(traversal == 'B'):
            if (i,j) == (0,0): 
                result = True
                break
        
        
        # checking the children of each node popped from fringe

        if i-1 >= 0 and grid[i-1][j] != 1 and p[i-1][j] == -1 and p[i][j] != (i-1,j): 
            p[i-1][j] = (i,j)
            g[i-1][j] = g[i][j]+1
            f[i-1][j] = g[i-1][j]+h[i-1][j]
            openList(i-1,j,fringe,f)
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1
            f[i][j+1]=g[i][j+1]+h[i][j+1]
            openList(i,j+1,fringe,f)
            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j] == -1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            f[i+1][j]=g[i+1][j]+h[i+1][j]
            openList(i+1,j,fringe,f)
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1] == -1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            f[i][j-1]=g[i][j-1]+h[i][j-1]
            openList(i,j-1,fringe,f)

        
    return(result, p)

def repeated_a_star(grid, dim, traversal):
    
    # recording time stamp to measure run time
    start = timeit.default_timer()
    
    # used to represent the gridworld that has been discovered (list of lists)
    dis = [[0 for i in range(dim)] for j in range(dim)]
    
    result = False
    done = False
    
    # Co-ordinates of the start node for forward
    if(traversal == 'F'):
        si = 0
        sj = 0
    elif(traversal == 'B'):
        si = dim-1
        sj = dim-1
    
    # Data structure to store final trajectory
    final = [] 
    
    cells = 0 
    
    while done != True:
        
        # planning stage of repeated A*
        result, parent = a_star(dim, dis, si, sj, traversal)

        # true if grid not solvable
        if result == False:
            break
        
        path = find_path(parent, dim, si, sj, traversal)
        
        # used to record total number of cells processed
        cells = cells + search_size(parent, dim)
        
        flag = True
        for (i, j) in path:  # agent traversing the planned path
            try:
                # recording the discovered grid
                dis[i-1][j] = grid[i-1][j] 
            except:
                pass
            try:
                dis[i][j+1] = grid[i][j+1]
            except:
                pass
            try:
                dis[i+1][j] = grid[i+1][j]
            except:
                pass
            try:
                dis[i][j-1] = grid[i][j-1]
            except:
                pass
            # true if current planned path has blocks
            if grid[i][j] == 1: 
                dis[i][j] = 1
                (si, sj) = parent[i][j]
                final.pop(len(final)-1)
                flag = False
                break
            final.append((i, j))

        if flag:
            done = True
    
    # recording time stamp to measure run time
    stop = timeit.default_timer() 
    MazePlotter(grid,path,si,sj)
    return(result, final, dis, cells, start, stop)







