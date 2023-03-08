from queue import Queue

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
          + abs(locF[1] - locM[1])
          + abs(locF[2] - locM[2]))

# temporary representations
maleAgent = 'male agent'
femaleAgent = 'female agent'
action = 'random action'

# main event loop
def main():
    q = Queue(maxsize=2)
    q.put(femaleAgent) # always goes first
    q.put(maleAgent)
    nTest = 0
    while q.full() and nTest < 10:
        curAgent = q.get()
        # curAgent.chooseAction()
        print(curAgent + " performed " + action)
        # curAgent.updateQtable()
        '''
        if complete():
            break
        '''
        # visualization
        # measure distance between agents after maleAgent moves
        if nTest % 2 != 0:
            print(distance([1,2,3], [4,5,6])) # 9
        q.put(curAgent)
        nTest += 1

if __name__ == "__main__":
    main()