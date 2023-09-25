from pathlib import Path
from matplotlib import pyplot as  plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator
import numpy as np

def MazePlotter(maze_arr,path,si,sj):
    #expcting maze_arr to be a 2D matrix of size 101x101
    #expecting path_arr to be a 2D array containing coordinates of the path

    for i,j in path:
        maze_arr[i][j]=2
    path=np.array(path)
    fig, ax = plt.subplots(1,1,figsize=(20,20))
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    ax.tick_params(which='major', grid_linestyle='-')
    plt.xticks(ha='left')
    colormap = colors.ListedColormap(['white','black','grey'])

    #plotting the maze and known world
    ax.pcolor(maze_arr, cmap=colormap)
    ax.grid(which='both',color = 'black',linewidth = 1)

    #plotting the agent's position
    x, y = path.T
    plt.scatter(y+0.5,x+0.5,marker='*',s=30)
    plt.scatter(si,sj,marker='X',s=40)
    plt.show()
    return 
