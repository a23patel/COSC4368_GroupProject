from queue import Queue

# temporary representations
maleAgent = 'male agent'
femaleAgent = 'female agent'
action = 'random action'

# main event loop
def main():
    q = Queue(maxsize=2)
    q.put(maleAgent)
    q.put(femaleAgent)
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
        q.put(curAgent)
        nTest += 1

if __name__ == "__main__":
    main()