from viz import *
from forward_backward import *
from a_star import *
from build_maze import *
from gen_grid import *
import numpy as np
import sys
import timeit
import platform
from matplotlib import pyplot as  plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator

sys.setrecursionlimit(1000000000)


worlds=int(input("Input Number of Worlds"))
part=int(input("Input part"))
print("before gen grid")
maze_list=gen_grid(worlds)
print("after gen grid")

#snippet to get results
def part2(worlds): #large G forward vs small G forward
    output_list1=[]
    output_list2=[]
    for var in range(worlds):
        #result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101)
        fringe,closedList, result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101, 'LG', 'F')
        output_list1.append([maze_list[var],result,final,closedList,stop-start])
        print("list1 updated")
        fringe,closedList, result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101, 'SG', 'F')
        output_list2.append([maze_list[var],result,final,closedList,stop-start])
        print("list2 updated")
        print(result)
        print(var)
    return [output_list1,output_list2]

def part3(worlds): #Large G forward vs large G Backward
    output_list1=[]
    output_list2=[]
    for var in range(worlds):
        #result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101)
        fringe,closedList, result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101, 'LG', 'F')
        output_list1.append([maze_list[var],result,final,closedList,stop-start])
        print("list1 updated")
        #fringe,closedList, result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101, 'LG', 'B')
        #output_list2.append([maze_list[var],result,final,closedList,stop-start])
        result, final, dis, cells, start, stop = repeated_a_star_back(maze_list[var], 101, 'B')
        output_list2.append([maze_list[var],result,final,stop-start])

        print("list2 updated")
        print(result)
        print(var)
    return [output_list1,output_list2]

def part4(worlds): #Large G forward vs large G Backward
    output_list1=[]
    output_list2=[]
    for var in range(worlds):
        #result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101)
        fringe,closedList, result, final, dis, cells, start, stop = repeated_a_star(maze_list[var], 101, 'LG', 'F')
        output_list1.append([maze_list[var],result,final,closedList,stop-start])
        print("list1 updated")
        fringe,closedList, result, final, dis, cells, start, stop = repeated_a_starAd(maze_list[var], 101)
        output_list2.append([maze_list[var],result,final,closedList,stop-start])
        print("list2 updated")
        print(result)
        print(var)
    return [output_list1,output_list2]


op2=[]
op3=[]
op4=[]
if part==0:
    print("Maze gen")
elif part==1:
    print("hi")
elif part==2:
    op2=part2(worlds)
elif part==3:
    op3=part3(worlds)
elif part==4:
    print("hi this is adaptive a star")
    op4=part4(worlds)
elif part==5:
    print("adaptive a star")
else:
    print("check pdf")



#part2 lg F  sg F
#part3 lg F  lg B
#part4 
#

