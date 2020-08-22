import time

class GO:



if __name__ == "__main__":
    file = open("input.txt","r")
    player = file.readline().rstrip()
    previous = []
    curr = []
    for i in range(5):
        temp = file.readline().rstrip()
        previous.append([x for x in temp])
    for i in range(5):
        temp = file.readline().rstrip()
        curr.append([x for x in temp])
    print(previous)
    print(curr)
