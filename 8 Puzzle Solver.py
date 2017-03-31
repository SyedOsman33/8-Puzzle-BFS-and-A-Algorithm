#!/usr/bin/env python
 
import sys
from optparse import OptionParser
import math
from struct import pack
import heapq
 
class Solver:
    def __init__(self, n):
        self.N = n
        self.L = n * n
 
        self.GOAL = list (range(1, self.L))
        self.GOAL.append(0)
 
        # slide rules
        self.SR = {}
        for i in range(self.L):
            s = []
            if i - self.N >= 0:
                s.append(i - self.N)
            if (i % self.N) - 1 >= 0:
                s.append(i - 1)
            if (i % self.N) + 1 < self.N:
                s.append(i + 1)
            if i + self.N < self.L:
                s.append(i + self.N)
            self.SR[i] = s
 
        # queue
        self.queue = []
        self.enqueued = {}
 
        self.verbose = 8963
 
        # h
        self.w = 1
        self.h = self.heuristics

    def is_solvable(self, tiles):    #to be thrown out if impossible
        x = 0
        for p in range(len(tiles)):
            a = tiles[p]
            if a < 2 :
                continue
            for b in tiles[p:]:
                if b == 0:
                    continue
                if a > b:
                    x = x + 1
        return (x & 1) == 0
 
    def neighbors(self, tiles):
        n = []
        a = tiles.index(0)
        for b in self.SR[a]:
            n.append(self.swap(list(tiles), a, b))
        return n
 
    def swap(self, tiles, a, b):
        tiles[a], tiles[b] = tiles[b], tiles[a]
        return tiles
 
    def display(self, tiles):
        for i in range(self.L):
            if tiles[i]:
                print  ( tiles[:3], "\n", tiles[3:6], "\n", tiles[6:9], "\n", "\n")
            else:
                print (' ')
            if i % self.N == self.N - 1:
                print
 
    def enqueue(self, state):
        (tiles, parent, h, g) = state
 
        if self.verbose > 0 and len(self.enqueued) % self.verbose == self.verbose - 1:
            print (" -->", len(self.enqueued), g)
 
        f = h * self.w + g;
        heapq.heappush(self.queue, (f, state))
 
    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state
 
    def heuristics(self, tiles):
        return 0;
 
    def manhattan(self, tiles): #manhattan algorithm
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n == 0:
                continue
            h += int(abs(n - 1 - i) / self.N) + (abs(n - 1 - i) % self.N)
        return h
 
    def hamming(self, tiles): #misplaced tiles algorithm
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n > 0 and n - 1 != i:
                h += 1
        return h

    
    def solve(self, initial): #BFS algorithm
        if not self.is_solvable(initial):
            return None
 
        state = (initial, None, self.h(initial), 0);
        if initial == self.GOAL:
            return state
 
        self.enqueue(state)
 
        while True:
            state = self.dequeue()
            if (not state):
                break
 
            (tiles, parent, h, g) = state
            neighbors = self.neighbors(tiles)
            for n_tiles in neighbors:
                if n_tiles == self.GOAL:
                    return (n_tiles, state, 0, g + 1)
 
                packed = pack(self.L*"B", *n_tiles)
                if (packed in self.enqueued):
                    continue;
                self.enqueued[packed] = True                       
 
                n_state = (n_tiles, state, self.h(n_tiles), g + 1)
                self.enqueue(n_state)
 
def main(options, args):
    initial = []
    goal = [1,2,3,4,5,6,7,8,0]
    
    while 1:
        print("Enter Your String with spaces and 0 as empty space")

        str_arr = input().split(' ') #will take in a string of numbers separated by a space

        arr = [int(num) for num in str_arr]
        initial = arr

        break
    else:
        initial = [8,7,6,5,4,3,2,1,0] #default string
 
    solver = Solver(int(math.sqrt(len(initial))))
 
    solver.verbose = int(options.verbose)
    solver.w = float(options.weight)
    if int(options.function) == 1:
        solver.h = solver.hamming
    elif int(options.function) == 2:
        solver.h = solver.manhattan
        
    state = solver.solve(initial) 
    if not state:
        print ("No solution possible")
        return 1
 
    solution = []
    while state:
        (tiles, parent, h, g) = state
        solution.insert(0, tiles)
        state = parent
 
    n = 0
    for tiles in solution:
        print (("#"), n)
        solver.display(tiles)
        print
        n += 1
 
    print (("Number of states enqueued ="), len(solver.enqueued))
    return 0

def algorithm():

    #taking input for algoritm from user
    print ("Choice of algorithms to use:")
    print ("0: BFS")
    print ("1. A* with misplaced tile heuristic")
    print ("2: A* with Manhattan distance heuristic")
    
    # infinite loop until correct input of algorithm choice
    while 1:
        pickAlgo = input("Enter: ")
        if(pickAlgo == '1'):
            value = 1
            break
        elif(pickAlgo == '2'):
            value = 2
            break
        elif(pickAlgo == '0'):
            value = 0
            break

    return value



 
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-v", "--verbose", metavar="<level>",
            default=8963)
    parser.add_option("-f", "--function", metavar="<fid>",
            help="heuristics function.0 for BFS. 1 for hamming, 2 for manhattan",
            default= algorithm())
    parser.add_option("-w", "--weight", metavar="<n>",
            help="if no function selected [default: 1]",
            default=1)
    (options, args) = parser.parse_args()
 
    sys.exit(main(options, args))
