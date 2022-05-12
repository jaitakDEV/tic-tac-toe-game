#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from IPython.display import clear_output
from IPython.display import HTML as html_print


# In[ ]:


class Tapatan:
  """ 
  AI playing Achi as your opponent 
  Solving it using MINMAX Algorithm
  state 1 = X
  state 2 = O
  state 0 = empty block
  """
  def __init__(self):
    self.size = 3
    self.state = np.zeros( (self.size,self.size),dtype = np.int8)
    self.bot = 1
    self.count = 0
    self.pos = (2,2)

  def isComplete(self,state):
    """ Check wheather game is over and return the winner
    0 if its Draw
    -1 not complete """
    li = [1,2]
    for i in li:
      # horizontal check
      for k in range(self.size):
        res = [True if h == i else False for h in state[k,:] ]
        if all(res):
          return i
      # vertical check
      for k in range(self.size):
        res = [True if h == i else False for h in state[:,k] ]
        if all(res):
          return i

      for k in range(self.size):
        res = [True if state[k][k] == i else False for k in range(self.size) ]
        res1 = [True if state[k][self.size-k-1] == i else False for k in range(self.size) ]
        if all(res) or all(res1):
          return i
    return -1

  def getDragMoves(self, state, player):
    up = [1, -1, 0] 
    down = [1, -1, 0]
    moves = {}
    pid = 1 if player else 2
    for i in range(self.size):
      for j in range(self.size):
        if state[i][j] == pid:
          moves[(i,j)] = []
          for k in up:
            for l in down:
             if k==0 and l==0:
               continue
             if i+k>=0 and j+l>=0 and i+k<self.size and j+l<self.size and state[i+k][j+l]==0:
               moves[(i,j)].append((i+k, j+l))  
    return moves  
  def getMove(self, state):
    move = []
    for i in range(self.size):
      for j in range(self.size):
        if(state[i][j] == 0): 
          move.append([i,j])
    return move
  def countSquare(self,state):
    count = 0
    for i in range(self.size):
      for j in range(self.size):
        if(state[i][j] == 0): 
          count+=1
    return count  
  def printState(self,state):

    """ Display the board state """
    
    for i in range(self.size-1,-1,-1): # printing states in reverse
      for j in range(self.size): 
        if state[i][j] == 0 :
          curr = ' '
        elif state[i][j] == 1:
          curr = self.printColor(True)
        else:
          curr = self.printColor(False)
        if j != self.size-1:
          print(f"{curr} | ",end = '')
        else:
          print(f"{curr}")
      if i != 0:
        print("--"*self.size*2)                                                                                                                                   
  def printColor(self,a):
    if a:
      return "\x1b[34mO\x1b[0m"
    return "\x1b[31mO\x1b[0m"
  def minMax(self,depth,isMaxPlayer, alpha, beta):
    if depth > 7:
      return {'position' : None, 'prize' : 0}
    ss = self.isComplete(self.state)
    
    if ss in [1,2]:
      if ss == 1:
        return {'position' : None, 'prize' : 10-depth}
      else:
        return {'position' : None, 'prize' : -10+depth}
    
    if isMaxPlayer:
      best = -90
    else:
      best = 90
    
    if self.count > 5:
      allmoves = self.getDragMoves(self.state, isMaxPlayer)
      for moves in allmoves.keys():
        ip, jp = moves
        for move in allmoves[moves]:
          i, j = move
          self.state[ip][jp] = 0 
          self.state[i][j] = 1 if isMaxPlayer else 2
          self.count+=1
          recur = self.minMax(depth+1,not isMaxPlayer, alpha, beta)
          self.state[ip][jp] = 1 if isMaxPlayer else 2
          self.count-=1
          self.state[i][j] = 0
    
          if isMaxPlayer:
            if recur['prize'] > best:
              best = recur['prize']
              pos = (ip,jp,i,j)
              alpha = max(alpha,best)
              if alpha>=beta:
                break
          
          else:
            if recur['prize'] < best:
              best = recur['prize']
              pos = (ip, jp,i,j)
              beta = min(beta,best)
              if alpha>=beta:
                break
      
        
      return {'position': pos, 'prize': best}
        
        
    
    else:
      moves = self.getMove(self.state)
      
      for move in moves:
        i, j = move
        self.count+=1
        self.state[i][j] = 1 if isMaxPlayer else 2
        recur = self.minMax(depth+1,not isMaxPlayer, alpha, beta)
        self.state[i][j] = 0
        self.count-=1
    
        if isMaxPlayer:
          if recur['prize'] > best:
            best = recur['prize']
            pos = (-1,-1,i,j)
            alpha = max(alpha,best)
            if alpha>=beta:
              break
          
        else:
          if recur['prize'] < best:
            best = recur['prize']
            pos = (-1,-1,i,j)
            beta = min(beta,best)
            if alpha>=beta:
              break
      return {'position': pos, 'prize': best}
        
#     return {'position': pos, 'prize': best}
            


  def play(self,youFirst = True):
    print("\t TicTacToe \n Bot = X \n You = O ")
    turn = youFirst
    while True:
      res = self.isComplete(self.state)
      if res in [0,1,2]:
        if res == 0:
          print("Draw")
          self.printState(self.state)
        elif res == 1:
          print("Bot Win ")
          self.printState(self.state)
        else:
          print("You Win - very unlikely ")
          self.printState(self.state)
        break

      self.printState(self.state)
      if turn:
        if(self.count>5):
          a, b = map(int, input("Your Two numbers form 1-9 \n").split())
          a-=1
          b-=1
          if self.state[a//self.size][ (a)%self.size]!=2 or self.state[b//self.size][ (b)%self.size]!=0:
            print("Invalid Input! Please enter another number")
            continue
          self.state[a//self.size][ (a)%self.size] = 0
          self.state[b//self.size][ (b)%self.size] = 2
        else:
          n = int(input("Your turn entern number form 1-9 \n"))-1
          if self.state[n//self.size][ (n)%self.size]!=0:
            print("Invalid Input! Please enter another number")
            continue
          if n == -1:
            print("Exiting")
            break
          self.state[n//self.size][ (n)%self.size] = 2
        
      else:
        print("Bots Turn")
        d = self.minMax(0,True, -1000 , 1000)
        self.pos = d['position']
        if self.pos[0] == -1: 
          self.state[self.pos[2]][ self.pos[3] ] = 1
        else:
          self.state[self.pos[0]][ self.pos[1] ] = 0
          self.state[self.pos[2]][ self.pos[3] ] = 1
    

      turn = not turn
      self.count+=1
      
      clear_output(True)


# In[ ]:


t = Tapatan()
t.play(youFirst = True)


# In[ ]:


getmove 


# In[ ]:




