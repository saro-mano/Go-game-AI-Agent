from copy import deepcopy

class Board:
    def __init__(self,n):
        self.size = n
        self.died = []

    #unsure whether to use or not
    def initialize_board():
        board = [[0 for x in range(n)] for y in range(n)]
        self.board = board
        self.previous = deepcopy(board)


    def setboard(self,piece,previous,board):
        for i in range(5):
            for j in range(5):
                if previous[i][j] == piece and board[i][j] != piece:
                    self.died.append((i,j))
        self.previous = previous
        self.board = board

    def compare(self,b1,b2):
        for i in range(5):
            for j in range(5):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    def find_neightbour(self,i,j):
        board = self.board
        nei = []
        if i > 0 :
            nei.append((i-1,j))
        if i < len(board) - 1:
            nei.append((i+1,j))
        if j > 0:
            nei.append((i, j-1))
        if j < len(board) - 1:
            nei.append((i, j+1))
        return nei

    def find_neightbours_same_nei(self,i,j):
        board = self.board
        nei = self.find_neightbour(i,j)
        members = []
        for each in nei:
            if board[each[0]each[1]] == board[i][j]:
                members.append(each)
        return members

    def deid_pieces(self,piece):
        board = self.board
        died = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == piece:
                    if not self.liberty(i,j):
                        died.append((i,j))

        return died

    def remove_died(self,piece):
        died = self.died_pieces(piece)
        if not died:
            return []
        self.remove_peices(died)
        return died

    def surrounding(i,j):
        stack = [(i,j)]
        members = []
        while stack:
            top = stack.pop()
            members.append(top)
            nei = self.find_neightbours_same_nei(top[0],top[1])
            for each in nei:
                if nei not in stack and ally not in members:
                    stack.append(nei)
        return members

    def libery(self,i,j):
        board = self.board
        surrounding_same_piece = self.surrounding(i,j)
        for each in surrounding_same_piece:
            nei = self.find_neightbour(each[0],each[1])
            for each_nei in nei:
                if board[each_nei[0]][each_nei[1]] == 0:
                    return True
        return False

    def update(self,new):
        self.board = new

    def remove_peices(self,pos):
        board = self.board
        for each in positions:
            board[each[0]][each[1]] = 0
        self.board = board

    def valid_place(self,i,j,piece,test = False):
        board = self.board

        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        if board[i][j] != 0:
            return False

        t_go = deepcopy(self)
        copy_board = t_go.board

        copy_board[i][j] = piece
        t_go.update(copy_board)
        if t_go.libery(i,j):
            return True

        t_go.remove_died(3-piece)
        if not t_go.libery(i,j):
            return False
        else:
            if self.died_pieces and self.compare(self.previous,t_go.board):
                return False
        return True
