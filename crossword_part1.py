import sys, random, re, os
import random
from random import randint
import copy

def initialize(xheight, xwidth, blockCt, fixedWords):
   numSpaces = xheight*xwidth
   grid = [[0 for x in range(xwidth)] for y in range(xheight)]

   for items in fixedWords:
      
      sX = items[1]
      sY = items[2]
      if items[0] == "V":
         # grid[sX][sY] = "*" #use * instead of tilde, I do not know where that one location
         # if len(items[3])>=3:
         for ind in range(len(items[3])):
            if items[3][ind] == "#":
               grid[sX+ind][sY] = "#"
               # blockCt -= 1
            else:
               grid[sX+ind][sY] = "*"

      if items[0] == "H":
         # grid[sX][sY] = "*" #use * instead of tilde, I do not know where that one location
         # if len(items[3])>=3:
         for ind in range(len(items[3])):
            if items[3][ind] == "#":
               grid[sX][sY+ind] = "#"
               # blockCt -= 1
            else:
               grid[sX][sY+ind] = "*"

   grid = flip(grid, xheight, xwidth)
   
   return grid


def placeBlocks(grid, xheight, xwidth, numBlocks):
   # global varName
   
   #use backtracking, ms kim used random
   #account for number of blocks
   #delete from spaceList if the input does not work
   spaceList = findSpaces(grid, xheight, xwidth)
   
   
   '''print(spaceList)'''
   if (xheight*xwidth)%2==1 and numBlocks%2 ==0:  #if it is odd number of squares and even number of blocks
      midNumIndex = int((xheight*xwidth)/2)
      if (midNumIndex) in spaceList:
         
         #print("odd sq, even blocks")
         spaceList.remove(midNumIndex)
   
   
   if numBlocks == 0:
      #print("im am done")
      #display(grid)
      return grid
   #while numBlocks>0: #if this finishes and there are still blocks left, return no solutions!!
   if len(spaceList)==0: #or numBlocks < 0:
      #print("no open spaces left!")
      return None
   
   oldGrid = [row[:] for row in grid]
   oldNumBlocks = numBlocks
   random.shuffle(spaceList)
   #place = randint(0,len(spaceList)-1) #SHOULD THIS BE -1????
   for place in range(len(spaceList)):
      # print(spaceList[place])
      # check whether index and opposite are empty
      opp = xheight*xwidth - 1 - spaceList[place]
      if grid[int(spaceList[place]/xwidth)][int(spaceList[place]%xwidth)] != 0 or grid[int(opp/xwidth)][int(opp%xwidth)] != 0:
         continue
      # place block and opposite
      grid[int(spaceList[place]/xwidth)][int(spaceList[place]%xwidth)] = "#" #im not sure if this indexing works
      #grid = flip(grid, xheight, xwidth)
      grid[int(opp/xwidth)][int(opp%xwidth)] = '#'
      
      grid, blockList = placeImplied(grid, xheight, xwidth)
      if grid is None:
         grid = [row[:] for row in oldGrid]
         numBlocks = oldNumBlocks
         continue
      numBlocks -= len(blockList)
      numBlocks -= 2
      if numBlocks >= 0 and isValid(grid, xheight, xwidth) == True:
         '''display(grid)
         print('--------------------------------------------')'''
         #display(grid)
         ret_val = placeBlocks(grid, xheight, xwidth, numBlocks)  #careful of number of blocks removed
         if ret_val is not None:
            return ret_val
         else: 
            grid = [row[:] for row in oldGrid]
            numBlocks = oldNumBlocks
         #return(placeBlocks(oldGrid, spaceList, xheight, xwidth, oldNumBlocks))
      else:
         grid = [row[:] for row in oldGrid]
         numBlocks = oldNumBlocks
   return None
       
def findSpaces(grid, xheight, xwidth):
   spaceList = []
   ind = 0
   for row in range(xheight):
      for col in range(xwidth):
         if grid[row][col]==0:
            spaceList.append(ind)
         ind = ind+1
   return spaceList


def flip(grid, xheight, xwidth):
   for rows in range(xheight):
      for cols in range(xwidth):
         if grid[rows][cols] == "*":
            #print(rows, cols)
            grid[abs(xheight - rows-1)][abs(xwidth - cols-1)] = "*"
         if grid[rows][cols] == "#":
            #print(rows, cols)
            grid[abs(xheight - rows-1)][abs(xwidth - cols-1)] = "#"
   return grid

def isValid(grid, xheight, xwidth):
   '''opp = xheight*xwidth - 1 - indBlock
   if grid[int(indBlock/xheight)][int(indBlock%xwidth)] != 0 or grid[int(opp/xheight)][int(opp%xwidth)] != 0:
      return False'''
   #grid[int(indBlock/xheight)][int(indBlock%xwidth)] = "#" #check if already occupied!!!!, not needed, in placeBlock
   # grid[int(opp/xheight)][int(opp%xwidth)] = '#' 
   #return(grid)
   #grid = flip(grid, xheight, xwidth)
   #display(grid)
   for row in range(xheight):
      for col in range(xwidth):
         if grid[row][col] == "*" or grid[row][col] == 0:
            starInd = int(row*xwidth) + int(col%xwidth)
            if checkHor(grid, starInd, xheight ,xwidth)<2:
               return False
            if checkVer(grid, starInd, xheight, xwidth)<2:
               return False
   if checkConnectivity([row[:] for row in grid], xheight, xwidth) == False:
      return False
   
   return True
            
'''def checkConnectivity(grid, xheight, xwidth):
   for row in range(xheight):
      for col in range(xwidth):
         wayOut = 0
         if grid[row][col] != "#":
            if row-1>=0:
               if grid[row-1][col] != "#":
                  wayOut = wayOut +1
            if row+1<xheight:
               if grid[row+1][col] != "#":
                  wayOut = wayOut +1
            if col-1>=0:
               if grid[row][col-1] != "#":
                  wayOut = wayOut +1
            if row+1<xwidth:
               if grid[row][col+1] != "#":
                  wayOut = wayOut +1
            if wayOut == 0:
               return False
   return True'''
   
   
def checkConnectivity(grid, xheight, xwidth):
   charCounter = 0
   findFirst = True
   firstRow = 0
   firstCol  = 0
   for row in range(xheight):
      for col in range(xwidth):
         if grid[row][col] != "#":
            if findFirst:
               firstRow = row
               firstCol = col
               findFirst = False
            charCounter = charCounter +1
   sectionCount = fillAndCount(grid, firstRow, firstCol)
   #display(fillGrid)
   #display(grid)
   #print("SectionCount: ", sectionCount)
   #print("charCounter: ", charCounter)
   if sectionCount == charCounter:
      return True
   return False
   

   
#public static int fillAndCount(char[][] g, int r, int c, char ch){
def fillAndCount(g, r, c):
   
      if((r<0) or (c<0) or (r>= len(g)) or (c>=len(g[0])) or (g[r][c] != 0 and g[r][c] != "*")):
         return 0
      
      
      num = 0

      g[r][c] = '-'
      num = num + (fillAndCount(g,r, c+1));
      num = num + (fillAndCount(g,r-1, c));
      num = num + (fillAndCount(g,r, c-1));
      num = num + (fillAndCount(g,r+1, c));
      
      num+=1;
      return num;
   
   
   
            
def display(grid):
   for lists in grid:
      print(lists)

def placeImplied(grid, xheight, xwidth):
   impliedListInds = []
   #for number in range((xheight*xwidth)): 
   for iterator__ in range(2):
      for row in range(xheight):
         for col in range(xwidth):
            curr_ind = row*xwidth + col
            opp = xheight*xwidth - 1 - curr_ind
            if grid[row][col]==0 or grid[row][col] == "*":
               '''if grid[row][col] == "*" or grid[row][col] == 0:
                  starInd = int(row*xwidth) + int(col%xwidth)'''
               if checkHor(grid, curr_ind, xheight, xwidth)<2:
                  if grid[row][col] == "*" or grid[opp//xwidth][opp%xwidth] == '*':
                     return None, []
                  grid[row][col] = "#"
                  impliedListInds.append(curr_ind)
                  impliedListInds.append(opp)
               if checkVer(grid, curr_ind, xheight, xwidth)<2:
                  if grid[row][col] == "*" or grid[opp//xwidth][opp%xwidth] == '*':
                     return None, []
                  grid[row][col] = "#"
                  impliedListInds.append(curr_ind)
                  impliedListInds.append(opp)
   return grid, list(set(impliedListInds))

def checkHor(grid, starInd, xheight, xwidth):
   #grid[int(starInd/xheight)][int(starInd%xwidth)] = "#" #REMOVE LATER!!!!, why?? 
   validHor = 0
   xInd = int(starInd%xwidth)
   while xInd>0:
      if grid[int(starInd/xwidth)][xInd-1] == "#":
         break
      if grid[int(starInd/xwidth)][xInd-1]== 0 or grid[int(starInd/xwidth)][xInd-1]== "*":
         #grid[int(starInd/xheight)][xInd-1] = "!"
         validHor = validHor +1
         xInd = xInd -1
   
   xInd = int(starInd%xwidth)
   while xInd<xwidth-1:
      #print(int(starInd/xheight), xInd+1)
      if grid[int(starInd/xwidth)][xInd+1] == "#":
         break
      if grid[int(starInd/xwidth)][xInd+1]== 0 or grid[int(starInd/xwidth)][xInd+1]== "*":
         validHor = validHor +1
         #grid[int(starInd/xheight)][xInd+1] = "^"
         xInd = xInd+1
   #display(grid)
   return validHor



def checkVer(grid, starInd, xheight, xwidth):
   #grid[int(starInd/xheight)][int(starInd%xwidth)] = "#" #REMOVE LATER!!!!, why??
   validVer = 0
   yInd = int(starInd/xwidth)
   while yInd>0:
      if grid[yInd-1][int(starInd%xwidth)] == "#":
         break
      #if grid[yInd-1][int(starInd%xwidth)]== 0 or grid[yInd-1][int(starInd%xwidth)]== "*":
      if grid[yInd-1][int(starInd%xwidth)] != "#":
         #grid[yInd-1][int(starInd%xwidth)] = "!"
         validVer = validVer +1
         yInd = yInd - 1
   
   yInd = int(starInd/xwidth)
   while yInd<xheight-1:
      if grid[yInd+1][int(starInd%xwidth)] == "#":
         break
      if grid[yInd+1][int(starInd%xwidth)]== 0 or grid[yInd+1][int(starInd%xwidth)]== "*":
         validVer = validVer +1
         #grid[yInd+1][int(starInd%xwidth)] = "^"
         yInd = yInd+1
   return validVer
      



def printBoard(grid, xheight, xwidth):
   for row in range(xheight):
      for col in range(xwidth):
         if grid[row][col] == 0:
            print("-", end=" ")
         else: 
            print(grid[row][col], end = " ")
      print()
   
#MY GUY, THIS PROGRAM NOT WORKING WITH THE NON SQUARES DOEEEEEE!!!!!

'''xheight = 7
xwidth = 7
grid = [[0 for x in range(xheight)] for y in range(xwidth)]
grid[0][0] = "*"
grid[1][0] = "*"
grid[2][0] = "*"
indBlock = 3
#grid[0][3] = "#"
#indBlock = 19 #(2, 2)
numBlocks = 8
#display(grid)

#print(display(isValid(grid, 32, 7, 7)))
#print(display(checkHor(grid, 18, 7, 7)[0]))
#print(checkHor(grid, 0, xheight, xwidth))
#print(checkHor(grid, 18, 7, 7))

grid = flip(grid, xheight, xwidth)
#display(grid)
#print(isValid(grid, indBlock, xheight, xwidth))

#grid = flip(grid, xheight, xwidth)
spaceList = findSpaces(grid, xheight, xwidth)
newGrid = placeBlocks(grid, spaceList, xheight, xwidth, numBlocks)
for row in range(xheight):
      for col in range(xwidth):
         if newGrid[row][col]=="*":
            newGrid[row][col]="-"

printBoard(newGrid, xheight, xwidth)'''



def main():
   intTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]
   xheight, xwidth, blockCt, dictSeen = 4, 4, 0, False
   fixedWords = []
   for arg in sys.argv[1:]:
      #print(arg)
      if os.path.isfile(arg):
         dictLines = open(arg, 'r').read().splitlines()
         dictSeen = True
         #print(arg)
         #print(dictSeen)
         continue
      for testNum, retest in enumerate(intTest):
         match = re.search(retest, arg, re.I)
         if not match: continue
         if testNum == 0:
            xheight, xwidth = int(match.group(1)), int(match.group(2))
         elif testNum == 1:
            blockCt = int(arg)
         else:
            vpos = int(match.group(2))
            hpos = int(match.group(3))
            word = match.group(4).upper()
            fixedWords.append([arg[0].upper(), vpos, hpos, word])
   #print(fixedWords)
   #print(xheight, xwidth, blockCt, fixedWords)
   grid = initialize(xheight, xwidth, blockCt, fixedWords)
   #display(grid)
   if (xheight*xwidth)%2==1 and blockCt%2 ==1:  #if it is odd number of squares and odd number of blocks
      midNumIndex = int((xheight*xwidth)/2)
      ##if (midNumIndex) in spaceList:
      grid[int(midNumIndex/xwidth)][int(midNumIndex%xwidth)] = "#"
         ##spaceList.remove(midNumIndex)
   grid, tempVar = placeImplied(grid, xheight, xwidth)
   blockCt -= sum(x.count('#') for x in grid)
   
   
   spaceList = findSpaces(grid, xheight, xwidth)
   newGrid = placeBlocks(grid, xheight, xwidth, blockCt)
   for row in range(xheight):
         for col in range(xwidth):
            if newGrid[row][col]=="*":
               newGrid[row][col]="-"
   
   for items in fixedWords:
      sX = items[1]
      sY = items[2]
      if items[0] == "V":
         newGrid[sX][sY] = items[3][0] #use * instead of tilde, I do not know where that one location
         #if len(items[3])>=3:
         for ind in range(len(items[3])):
            newGrid[sX+ind][sY] = items[3][ind]
         
      if items[0] == "H":
         newGrid[sX][sY] = items[3][0] #use * instead of tilde, I do not know where that one location
         if len(items[3])>=3:
            for ind in range(len(items[3])):
               newGrid[sX][sY+ind] = items[3][ind]
         
   
   
   printBoard(newGrid, xheight, xwidth)
   # grid, blockList = placeImplied(grid, xheight, xwidth)
   # display(grid)
   # print(blockList)
   
   
   
   #initialize(7, 7, blockCt, fixedWords)
   #if not dictSeen: exit("whatever...")
   
   
main() 