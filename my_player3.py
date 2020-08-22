'''9310129803:Saravanan Manoharan'''
from copy import deepcopy

'''reading the input from a file'''
def input(n, path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()
        player_type = int(lines[0])
        previous = [[int(y) for y in line.rstrip('\n')] for line in lines[1:n+1]]
        current = [[int(y) for y in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]
        return player_type, previous, current

'''writing the output to a file'''
def output(result, path="output.txt"):
    out = ""
    if result == "PASS":
    	out = "PASS"
    else:
	    out += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(out)

class Board:
    '''initializing the board'''
    def __init__(self, n):
        self.size = n
        self.died_pieces = []

    '''setting the board from the input'''
    def setboard(self, player_type, previous, board):
        size = self.size
        for i in range(size):
            for j in range(size):
                if previous[i][j] == player_type and board[i][j] != player_type:
                    self.died_pieces.append((i, j))
        self.previous = previous
        self.board = board

    '''comparing the previous board and current board'''
    def compare(self, b1, b2):
        size = self.size
        for i in range(size):
            for j in range(size):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    '''copy function'''
    def copy(self):
        return deepcopy(self)

    '''finding neighbor of the particular index'''
    def find_neighbor(self, i, j):
        board = self.board
        neigh = []
        if i > 0:
            neigh.append((i-1, j))
        if i < len(board) - 1:
            neigh.append((i+1, j))
        if j > 0:
            neigh.append((i, j-1))
        if j < len(board) - 1:
            neigh.append((i, j+1))
        return neigh

    '''finding the similar players that form neighbor'''
    def find_similar_neighbor(self, i, j):
        board = self.board
        neighbors = self.find_neighbor(i, j)
        group = []
        for piece in neighbors:
            if board[piece[0]][piece[1]] == board[i][j]:
                group.append(piece)
        return group

    '''returns the list of index that are of same players and form allies'''
    def similar_neighbor(self, i, j):
        stack = [(i, j)]
        members = []
        while stack:
            top = stack.pop()
            members.append(top)
            neighbors = self.find_similar_neighbor(top[0], top[1])
            for each in neighbors:
                if each not in stack and each not in members:
                    stack.append(each)
        return members

    '''checking liberty for a particular position'''
    def liberty(self, i, j):
        board = self.board
        members = self.similar_neighbor(i, j)
        count = 0
        for member in members:
            neighbors = self.find_neighbor(member[0], member[1])
            for each in neighbors:
                if board[each[0]][each[1]] == 0:
                    return True
        return False

    '''checking the total dead pieces'''
    def total_died_pieces(self, player_type):
        board = self.board
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == player_type:
                    if not self.liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces

    '''removing the dead pieces'''
    def remove_died_pieces(self, player_type):
        died_pieces = self.total_died_pieces(player_type)
        if not died_pieces:
            return []
        self.remove_pieces(died_pieces)
        return died_pieces

    '''removing the pieces'''
    def remove_pieces(self, positions):
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.updateBoard(board)

    '''placing a player at a particular position'''
    def place(self, i, j, player_type):
        board = self.board

        valid = self.valid_place(i, j, player_type)
        if not valid:
            return False
        self.previous = deepcopy(board)
        board[i][j] = player_type
        self.updateBoard(board)
        return True

    '''checking for a valid position'''
    def valid_place(self, i, j, player_type, test_check=False):
        board = self.board

        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False

        if board[i][j] != 0:
            return False

        test_board_obj = self.copy()
        test_board = test_board_obj.board

        test_board[i][j] = player_type
        test_board_obj.updateBoard(test_board)
        if test_board_obj.liberty(i, j):
            return True


        test_board_obj.remove_died_pieces(3 - player_type)
        if not test_board_obj.liberty(i, j):
            return False

        else:
            if self.died_pieces and self.compare(self.previous, test_board_obj.board):
                return False
        return True

    '''updating the board'''
    def updateBoard(self, new_board):
        self.board = new_board

'''evaluation function'''
def evaluate(player,enemy):
    liberty = 0
    edge = 0
    middle = 0
    star_pattern = 0
    enemy_star_pattern = 0
    enemy_edge = 0
    middle_enemy = 0
    enemy_liberty = 0

    board = board_obj.board
    '''liberty calculation'''
    for i in range(board_obj.size):
        for j in range(board_obj.size):
            if board[i][j] == player:
                if board_obj.liberty(i,j):
                    liberty += 1
            if board[i][j] == enemy:
                if board_obj.liberty(i,j):
                    enemy_liberty += 1
    '''death calculation'''
    dead_player = len(board_obj.total_died_pieces(player))
    dead_enemy = len(board_obj.total_died_pieces(enemy))
    for i in range(0,5):
        '''player edge calculation'''
        if board[i][0] == player:
            edge += 1
        if board[i][4] == player:
            edge += 1
        if board[0][i] == player:
            edge += 1
        if board[4][i] == player:
            edge += 1

        '''enemy edge calculation'''
        if board[i][0] == enemy:
            enemy_edge += 1
        if board[i][4] == enemy:
            enemy_edge += 1
        if board[0][i] == enemy:
            enemy_edge += 1
        if board[4][i] == enemy:
            enemy_edge += 1

    '''for creating the I pattern in my move'''
    for i in range(1,4):
        if board[2][i] == player:
            middle += 1
        if board[i][2] == player:
            middle += 1
        if board[2][i] == enemy:
            middle_enemy += 1
        if board[i][2] == enemy:
            middle_enemy += 1

    '''placing the player in the 3x3 middle'''
    for i in range(1,4):
        for j in range(1,4):
            if board[i][j] == player:
                middle += 1
            if board[i][j] == enemy:
                middle_enemy += 1

    '''placing the player alternatively'''
    for i in range(0,5,2):
        for j in range(0,5,2):
            if board[i][j] == player:
                star_pattern += 1
            if board[i][j] == enemy:
                enemy_star_pattern += 1
    for i in range(1,4,2):
        for j in range(1,4,2):
            if board[i][j] == player:
                star_pattern += 1
            if board[i][j] == enemy:
                enemy_star_pattern += 1

    return (129*dead_enemy) - (edge) - (20*dead_player) + (middle) + (liberty) + star_pattern + enemy_edge - middle_enemy - enemy_liberty - enemy_star_pattern

'''minimax function'''
def minimax(depth,isMax,player,enemy,alpha,beta):
    if depth == 1 :
        score = evaluate(player,enemy)
        return score
    if isMax: #always the maximizing player
        best = -1000
        for i in range(board_obj.size):
            for j in range(board_obj.size):
                if board_obj.valid_place(i, j, player, test_check = True):
                    board_obj.place(i,j,player)
                    best = max(best,minimax(depth+1,False,player,enemy,alpha,beta))
                    list_parsing = list()
                    list_parsing.append((i,j))
                    board_obj.remove_pieces(list_parsing)
                    alpha = max(alpha, best)
                    if best >= beta:
                        return best
                    if best > alpha:
                        alpha = best
        if best == -1000:
            return evaluate(player,enemy)
        else:
            return best
    else:
        best = 10000
        no = 1
        for i in range(board_obj.size):
            for j in range(board_obj.size):
                if board_obj.valid_place(i, j, enemy, test_check = True):
                    board_obj.place(i,j,enemy)
                    best = min(best,minimax(depth+1,True,player,enemy,alpha,beta))
                    list_parsing = list()
                    list_parsing.append((i,j))
                    board_obj.remove_pieces(list_parsing)
                    beta = min(beta, best)
                    no += 1
                    if best <= alpha:
                        return best
                    if best < beta:
                        beta = best
        if best == 10000:
            return evaluate(player,enemy)
        else:
            return best

'''finding the bestmove of our player'''
def best_move(possible_indices,player_type):
    alpha = -1000
    beta =  1000
    bestvalue = -1000
    bestPos = None
    if player_type == 1:
        player = 1
        enemy = 2
    else:
        player = 2
        enemy = 1
    sno = 1
    for each in possible_indices:
        board_obj.place(each[0],each[1],player_type)
        moveval = minimax(0,False,player,enemy,alpha,beta)
        list_parsing = list()
        list_parsing.append(each)
        board_obj.remove_pieces(list_parsing)
        if moveval != 10000 and moveval != - 1000:
            if (moveval > bestvalue):
                bestvalue = moveval
                bestPos = each
    if bestPos == None or bestPos == -1000:
        return "PASS"
    else:
        return bestPos

'''Player class'''
class Player:
    def get_output(self, board_obj, player_type):
        possible_indices = []
        for i in range(board_obj.size):
            for j in range(board_obj.size):
                if board_obj.valid_place(i, j, player_type, test_check = True):
                    possible_indices.append((i,j))
        value = best_move(possible_indices,player_type)
        return value

if __name__ == "__main__":
    N = 5
    player_type, previous, board = input(N)
    board_obj = Board(N)
    board_obj.setboard(player_type, previous, board)
    player = Player()
    action = player.get_output(board_obj, player_type)
    output(action)
