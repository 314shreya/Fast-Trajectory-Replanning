import timeit
from pathlib import Path
from matplotlib import pyplot as  plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator
import numpy as np
import matplotlib.patches as mpatches

def get_dist(i, j, dim):  
    return abs(dim-1-i) + abs(dim-1-j)

# insertion into priority queue
def openList(i, j, fringeLargeG, f, g, tiebreak): 
    # if len of fringe == 0, then only append into the priority queue!
    if len(fringeLargeG) == 0:
        fringeLargeG.append((i,j))
        # print("fringe len 0, direct append")
    else:
        for x in range(len(fringeLargeG)):
            (I,J) = fringeLargeG[x]
            if f[I][J] == f[i][j]:
                if tiebreak == 'LG' and g[I][J] < g[i][j]:
                    if((i,j) not in fringeLargeG):
                        fringeLargeG.insert(x, (i,j))

                if tiebreak == 'SG' and g[I][J] > g[i][j]:
                    if((i,j) not in fringeLargeG):
                        fringeLargeG.insert(x, (i,j))
                    
                # print("fringe -> ", fringeLargeG)
            #     return
            if f[I][J] > f[i][j]:
                fringeLargeG.insert(x, (i,j))
                # print("fringe if f smaller -> ", fringeLargeG)
                return
        
        fringeLargeG.append((i,j))
    # print("fringe -> ", fringeLargeG)

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


def a_star(dim, grid, si, sj, closedList, tiebreak, traversal):
    
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
    
    
    # pushing the start node into the fringeLargeG
    fringe = [(si,sj)] 
        
    while len(fringe) != 0:
        (i,j) = fringe.pop(0)
        closedList.append((i,j))
        
        # closedListLarge = closedListLarge.append((i,j))
        # true if goal node is reached
        # goal node set to [dim-1,dim-1]
        if(traversal == 'F'):
            if (i,j) == (dim-1, dim-1): 
                result = True
                break
        if(traversal == 'B'):
            if (i,j) == (0,0): 
                result = True
                break
        # print("---------------------------------------------------------")
        # print("(i,j) -> ", (i,j))
        # checking the children of each node popped from fringeLargeG

        if i-1 >= 0 and grid[i-1][j] != 1 and p[i-1][j] == -1 and p[i][j] != (i-1,j): 
            p[i-1][j] = (i,j)
            g[i-1][j] = g[i][j]+1
            f[i-1][j] = g[i-1][j]+h[i-1][j]
            if(tiebreak == 'LG'):
                openList(i-1,j,fringe,f, g, 'LG')
            elif(tiebreak == 'SG'):
                openList(i-1,j,fringe,f, g, 'SG')
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1
            f[i][j+1]=g[i][j+1]+h[i][j+1]
            if(tiebreak == 'LG'):
                openList(i,j+1,fringe,f, g, 'LG')
            elif(tiebreak == 'SG'):
                openList(i,j+1,fringe,f, g, 'LG')

            
            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j] == -1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            f[i+1][j]=g[i+1][j]+h[i+1][j]
            if(tiebreak == 'LG'):
                openList(i+1,j,fringe,f, g, 'LG')
            elif(tiebreak == 'SG'):
                openList(i+1,j,fringe,f, g, 'SG')

            
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1] == -1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            f[i][j-1]=g[i][j-1]+h[i][j-1]
            if(tiebreak == 'LG'):
                openList(i,j-1,fringe,f, g, 'LG')
            elif(tiebreak == 'SG'):
                openList(i,j-1,fringe,f, g, 'SG')
            
        # print("f---->")
        # print(fLarge)
        # print("g---->")
        # print(gLarge)
    return(result, closedList, p, fringe)


def repeated_a_star(grid, dim, tiebreak, traversal):
    
    # recording time stamp to measure run time
    start = timeit.default_timer()
    closedList = []
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
    #comment here to stop viz
    # initialize visualition
    fig, ax = plt.subplots(1,1,figsize=(5,5))
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.tick_params(which='major', grid_linestyle='-')
    plt.xticks(ha='left')
    plt.legend(['black','white','red'],loc ="lower right")
    colormap = colors.ListedColormap(['white','black','red'])
    plt.grid(b=True, which='major',color = 'black',linewidth = 2)   
    #done initialization
        
    while done != True:
        
        # planning stage of repeated A*
        result, closedList, parent, fringe = a_star(dim, dis, si, sj, closedList, tiebreak, traversal)

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
                try:
                    (si, sj) = parent[i][j]
                    final.pop(len(final)-1)
                    flag = False
                    break
                except:
                    print(parent[i][j])
            final.append((i, j))

        if flag:
            done = True
        #comment here to stop viz 
        #------------------- VIZ CODE
        curr_path_copy=np.array(path)
        if len(path)==0:
          curr_path_copy=np.array([0,0])      
        #plotting the agent's position
        result = [[grid[i][j] + dis[i][j]  for j in range(len(grid[0]))] for i in range(len(grid))]
        ax.pcolor(result,cmap=colormap)
        x, y = curr_path_copy.T
        plt.scatter(y+0.5,x+0.5)
        plt.scatter(sj+0.5,si+0.5,marker='s',s=40)
        plt.pause(2)
 
        #------------------- VIZ CODE
           
    # recording time stamp to measure run time
    stop = timeit.default_timer() 
    
    return(fringe, closedList, result, final, dis, cells, start, stop)



# HERE IS THE BACKWARD A STAR CODE
#backward
def get_dist_back(i, j, dim):  
    return abs(dim-1-i)+abs(dim-1-j) #Manhattan distance

# insertion into priority queue (Fringe)
def openList_back(i, j, fringe, f): 

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

def find_path_back(parent, dim, si, sj, traversal): #used to find the path from the parent data structure
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

def search_size_back(parent, dim): #used to find the size of the search tree that was discovered
    ans = 0
    for i in parent:
        for j in i:
            if j == -1:
                ans = ans + 1
    return ((dim * dim) - ans)


def a_star_back(dim, grid, si, sj, traversal):
    
    result = False
    
    # data structure to store g(n) (list of lists). initialized with -1 for now
    g = [[-1 for i in range(dim)] for j in range(dim)]
    g[si][sj] = 0
    
    # data structure to store h(n) (list of lists).
    h = [[get_dist_back(i,j,dim) for i in range(dim)] for j in range(dim)] 
    
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
            openList_back(i-1,j,fringe,f)
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1
            f[i][j+1]=g[i][j+1]+h[i][j+1]
            openList_back(i,j+1,fringe,f)
            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j] == -1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            f[i+1][j]=g[i+1][j]+h[i+1][j]
            openList_back(i+1,j,fringe,f)
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1] == -1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            f[i][j-1]=g[i][j-1]+h[i][j-1]
            openList_back(i,j-1,fringe,f)

        
    return(result, p)



def repeated_a_star_back(grid, dim, traversal):
    
    # recording time stamp to measure run time
    start = timeit.default_timer()
    
    # used to represent the gridworld that has been discovered (list of lists)
    dis = [[0 for i in range(dim)] for j in range(dim)]
    
    result = False
    done = False
    
    
    # Data structure to store final trajectory
    final = [] 
    
    cells = 0 
    #comment here to stop VIZ
    #----------------------VIZ
    fig, ax = plt.subplots(1,1,figsize=(5,5))
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.tick_params(which='major', grid_linestyle='-')
    plt.xticks(ha='left')
    
    colormap = colors.ListedColormap(['white','black','red','yellow'])
    plt.grid(b=True, which='major',color = 'black',linewidth = 2)
    black_patch = mpatches.Patch(color='Black', label='Blocked cells')
    red_patch = mpatches.Patch(color='Red', label='Discovered blocked cells')
    blue_patch = mpatches.Patch(color='Blue',label = 'A* being recalled')


    plt.legend(handles=[black_patch,red_patch, blue_patch],loc='upper right', bbox_to_anchor=(0.5, -0.05),fancybox = True, shadow = True)
    plt.savefig("test.png",bbox_inches='tight')
    plt.tight_layout()
    #-------------VIZ
    
    # Co-ordinates of the start node for forward
    if(traversal == 'F'):
        si = 0
        sj = 0
        plt.title("Repeated forwared A*",y=-0.08)
    elif(traversal == 'B'):
        si = dim-1
        sj = dim-1
        plt.title("Repeated Backward A*",y=-0.08)
    while done != True:
        
        # planning stage of repeated A*
        result, parent = a_star_back(dim, dis, si, sj, traversal)
        
        # true if grid not solvable
        if result == False:
            break 
        path = find_path_back(parent, dim, si, sj, traversal)

        # used to record total number of cells processed
        cells = cells + search_size_back(parent, dim)

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
                try:
                    (si, sj) = parent[i][j]
                    final.pop(len(final)-1)
                    flag = False
                    break
                except:
                    print(parent[i][j])
            final.append((i, j))

            
        if flag:
            done = True

        #Comment here to stop viz     
        #-------------------
        curr_path_copy=np.array(path)
        if len(path)==0:
          curr_path_copy=np.array([0,0])
        
        #plotting the agent's position
        resultx = [[grid[i][j] + dis[i][j]  for j in range(len(grid[0]))] for i in range(len(grid))]
        resultx[0][0]=3
        resultx[dim-1][dim-1]=3
        ax.pcolor(resultx,cmap=colormap)
        x, y = curr_path_copy.T
        plt.scatter(y+0.5,x+0.5)
        plt.scatter(sj+0.5,si+0.5,marker='s',s=50,color='Blue')
        
        plt.pause(0.01)
 
        #------------------- 
        
    # recording time stamp to measure run time
    stop = timeit.default_timer() 
    p,q=np.array(final).T
    plt.scatter(q+0.5,p+0.5)
    plt.pause(10)

    return(result, final, dis, cells, start, stop)




#ADAPTIVE
# Adaptive new try
def get_dist(i, j, dim):  
    return abs(dim-1-i) + abs(dim-1-j)

def get_distAdaptive(y1, y2, dim, si,sj, g):
    gGoal = g[dim-1][dim-1]
    gCurrent = g[y1][y2]
    return abs(gGoal - gCurrent)
    

# insertion into priority queue
def openListAd(i, j, fringeLargeG, f, g): 
    # if len of fringe == 0, then only append into the priority queue!
    if len(fringeLargeG) == 0:
        fringeLargeG.append((i,j))
    else:
        for x in range(len(fringeLargeG)):
            (I,J) = fringeLargeG[x]
            if f[I][J] == f[i][j]:
                if g[I][J] > g[i][j]:
                    if((i,j) not in fringeLargeG):
                        fringeLargeG.insert(x, (i,j))
                    
            if f[I][J] > f[i][j]:
                fringeLargeG.insert(x, (i,j))
                return
        
        fringeLargeG.append((i,j))

def find_pathAd(parent, dim, si, sj): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1, dim-1)]
    
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

def search_sizeAd(parent, dim): #used to find the size of the search tree that was discovered
    ans = 0
    for i in parent:
        for j in i:
            if j == -1:
                ans = ans + 1
    return ((dim * dim) - ans)

def a_starAd(dim, grid, si, sj, closedListSmall, h):
    
    result = False
    
    # data structure to store g(n) (list of lists). initialized with -1 for now
    g = [[-1 for i in range(dim)] for j in range(dim)]
    g[si][sj] = 0

    # data structure to store f(n) (list of lists). initialized with -1 for now
    f = [[-1 for i in range(dim)] for j in range(dim)] 
    f[si][sj] = g[si][sj]+h[si][sj]

    # data structure to store pointers to parent (list of lists). initialized with -1 for now
    p = [[-1 for i in range(dim)] for j in range(dim)] 
    p[si][sj] = 0
    
    
    # pushing the start node into the fringeLargeG
    fringe = [(si,sj)] 
    
    
    while len(fringe) != 0:
        (i,j) = fringe.pop(0)
        closedListSmall.append((i,j))
        
        
        # true if goal node is reached
        # goal node set to [dim-1,dim-1]
        
        if (i,j) == (dim-1, dim-1):
            result = True
            break
        
        
        # checking the children of each node popped from fringeLargeG

        
        if i-1 >= 0 and grid[i-1][j] != 1 and p[i-1][j] == -1 and p[i][j] != (i-1,j): 
            p[i-1][j] = (i,j)
            g[i-1][j] = g[i][j]+1

            f[i-1][j] = g[i-1][j]+h[i-1][j]
            openListAd(i-1,j,fringe,f, g)
            
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1

            f[i][j+1]=g[i][j+1]+h[i][j+1]
            openListAd(i,j+1,fringe,f, g)
            

            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j] == -1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            

            f[i+1][j]=g[i+1][j]+h[i+1][j]
            openListAd(i+1,j,fringe,f, g)
            
            
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1] == -1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            

            f[i][j-1]=g[i][j-1]+h[i][j-1]
            openListAd(i,j-1,fringe,f, g)
            
        
    for y in closedListSmall:
        # print(y[0], y[1])
        h[y[0]][y[1]] = get_distAdaptive(y[0],y[1],dim,si,sj, g)
    
    return(result, closedListSmall, p, fringe)


def repeated_a_starAd(grid, dim):
    
    # recording time stamp to measure run time
    start = timeit.default_timer()
    closedList = []
    # used to represent the gridworld that has been discovered (list of lists)
    dis = [[0 for i in range(dim)] for j in range(dim)]
    
    result = False
    done = False
    
    # Co-ordinates of the start node for forward
    
    si = 0
    sj = 0
    
    # Data structure to store final trajectory
    final = [] 
    h = [[get_dist(i,j,dim) for i in range(dim)] for j in range(dim)] 
    cells = 0 
    
    while done != True:
        
        # planning stage of repeated A*
        closedListSmall = []    
        result, closedListSmall, parent, fringe = a_starAd(dim, dis, si, sj, closedListSmall, h)
        closedList.extend(closedListSmall)
        # true if grid not solvable
        if result == False:
            break
        
        path = find_pathAd(parent, dim, si, sj)

        
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
                try:
                    (si, sj) = parent[i][j]
                    final.pop(len(final)-1)
                    flag = False
                    break
                except:
                    print(parent[i][j])
            final.append((i, j))

        if flag:
            done = True
    
    # recording time stamp to measure run time
    stop = timeit.default_timer() 
    
    return(fringe, closedList, result, final, dis, cells, start, stop)