import random

# helper funtions 
def display(ite):
    print("\n  1 2 3")
    for i in range(len(ite)):
        print(i+1, *ite[i])
def reset():
    return [['_']*3, ['_']*3, ['_']*3]
def fill(ite, x, y, filler):
    ite[x-1][y-1] = filler
def choose_player(number):
    print(f'Enter O or X for player {number}: ')
    user_input = input()
    if user_input == 'O':
        return 'O'
    elif user_input == 'X':
        return 'X'
    else:
        print('Invalid input. Try again!')
        return choose_player(number)
def whoes_first(players, player1, player2):
    print(f'Who goes first?\n1. {players[player1]}\n2. {players[player2]} ')
    user_input = input()
    if user_input == '1':
        print('player 1 is goes first.')
        return player1
    elif user_input == '2':
        print('player 2 is goes first.')
        return player2
    else:
        print('Invalid input. Try again!')
        return whoes_first(players, player1, player2)
def check_winner(board):
    ''' It will check in rows, columns and diagonals,
    and returns three type of value: 
    1. None -> game is going on. 
    2. X or O for winner 
    3. tie 
    '''
    def eq(a,b,c):
        return a==b and b==c and a!='_'
    
    winner = None
    
    for i in range(3):
        if eq(board[i][0], board[i][1], board[i][2]):
            winner = board[i][0]
    for i in range(3):
        if eq(board[0][i], board[1][i], board[2][i]):
            winner = board[0][i]
    if eq(board[0][0], board[1][1], board[2][2]):
        winner = board[0][0]
    if eq(board[0][2], board[1][1], board[2][0]):
        winner = board[0][2]
        
    empty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                empty += 1
                
    if winner == None and empty == 0:
        return 'tie'
    else:
        return winner

# player vs player
def player_vs_player():
    print("\n\nPlaying Player VS Player")

    players = {}

    player1 = choose_player(1)
    player2 = 'O' if player1 == 'X' else 'X'
    players[player1] = 'Player 1'
    players[player2] = 'Player 2'
    print(f'\n{players[player1]} is {player1}')
    print(f'{players[player2]} is {player2}')

    available_cords = [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]
    
    turn = whoes_first(players, player1, player2)

    ttt = reset()
    print("Initial Grid: ")
    display(ttt)

    while True:
        if turn == player1:
            print(f"{players[player1]}'s turn ({player1}): ")
            # x, y = list(map(int, list(input())))
            x,y = get_cords_from_number(int(input('Enter number place number: ')))
            if [x,y] in available_cords:
                fill(ttt, x ,y, player1)
                available_cords.remove([x,y])
                turn = player2
            else:
                print('\n!!!!!Place not empty, choose different place.!!!!!')
        else:
            print(f"{players[player2]}'s turn ({player2}): ")
            # x, y = list(map(int, list(input())))
            x,y = get_cords_from_number(int(input('Enter number place number: ')))
            if [x,y] in available_cords:
                fill(ttt, x ,y, player2)
                available_cords.remove([x,y])
                turn = player1
            else:
                print('\n!!!!!Place not empty, choose different place.!!!!!')
        
        display(ttt)
        winner = check_winner(ttt)
        if winner == 'X' or winner == 'O':
            print(f'\n------ {winner} won. ------')
            break
        elif winner == 'tie':
            print('\n------ Tie! ------')
            break


# player vs computer(random pick)               
def player_vs_computer():
    print("\n\nPlaying Player VS Computer(Random Pick)")
    
    players = {}

    player = choose_player(1)
    computer = 'O' if player == 'X' else 'X'
    players[player] = 'Player'
    players[computer] = 'Computer'
    print(f'\n{players[player]} is {player}')
    print(f'{players[computer]} is {computer}')

    available_cords = [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]
    
    turn = whoes_first(players, player, computer)

    ttt = reset()
    print("Initial Grid: ")
    display(ttt)
    
    while True:
        if turn == player:
            print(f"{players[player]}'s turn ({player}):  ")
            # x, y = list(map(int, list(input())))
            x,y = get_cords_from_number(int(input('Enter number place number: ')))
            if [x,y] in available_cords:
                fill(ttt, x, y, player)
                available_cords.remove([x,y])
                turn = computer
            else:
                print('\n!!!!!Place not empty, choose different place.!!!!!')
        else:
            print(f"{players[computer]}'s turn ({computer}): Enter number:  ")
            x, y = available_cords[random.randint(0, len(available_cords)-1)]
            print(f"{x}{y}")
            fill(ttt, x, y, computer)
            available_cords.remove([x,y])
            turn = player

        display(ttt)
        winner = check_winner(ttt)
        if winner == 'X' or winner == 'O':
            print(f'\n------ {winner} won. ------')
            break
        elif winner == 'tie':
            print('\n------ Tie! ------')
            break


# player vs algo
def best_move(board, computer, player):
    best_score = -float('inf')
    move = None
    
    for i in range(3):
        for j in range(3):
            # print(i,j)
            if board[i][j] == '_':
                board[i][j] = computer
                score = minimax(board, False, computer, player)
                board[i][j] = '_'
                # print(score, i,j)
                if score >= best_score:
                    best_score = score
                    move = [i,j]
    return move
    
def minimax(board, is_maximizing, computer, player):
    ''' is_maximizing is for checking that whether we putting user choice or computer choice,
    if we are on the step where computer need to put value then is_maximizing is false otherwise its true.
    Also it returns best score according to whoes turn its predicting, 
    like if its computers turn max will be used otherwise min will be beneficial. '''
    
    scores = {
        computer: 2,
        player: -1,
        'tie': 0
    }
    res = check_winner(board)
    if res != None:
        return scores[res]
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = computer
                    score = minimax(board, False, computer, player)
                    board[i][j] = '_'
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    score = minimax(board, True, computer, player)
                    board[i][j] = '_'
                    best_score = min(best_score, score)
        return best_score


def get_cords_from_number(number):
    if number > 6:
        return [3, int(number)-3-3]
    elif number > 3:
        return [2, int(number)-1-2] 
    else:
        return [1, int(number)+1-1]


def player_vs_algo():
    print("\n\nPlaying Person VS Algorithm")
    players = {}

    player = choose_player(1)
    computer = 'O' if player == 'X' else 'X'
    players[player] = 'Player'
    players[computer] = 'Computer'
    print(f'\n{players[player]} is {player}')
    print(f'{players[computer]} is {computer}')

    available_cords = [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]
    
    turn = whoes_first(players, player, computer)
    
    ttt = reset()
    print("Initial Grid: ")
    display(ttt)
    
    while True:
        if turn == computer:
            print(f"{players[computer]}'s turn ({computer}):  ")
            i,j = best_move(ttt, computer, player)

            x,y = i+1, j+1
            print(x,y)
            if [x,y] in available_cords: 
                ''' here we dont need to check as this spot is returned,
                    so it must be empty but for safe side i'll do it. '''
                
                fill(ttt, x ,y, computer)
                available_cords.remove([x,y])
                turn = player
            else:
                print('\n!!!!!Place not empty, choose different place.!!!!!')
        else:
            print(f"{players[player]}'s turn ({player}): ")
            # x,y = list(map(int, list(input())))
            x,y = get_cords_from_number(int(input('Enter number place number: ')))
            if [x,y] in available_cords:
                fill(ttt, x ,y, player)
                available_cords.remove([x,y])
                turn = computer
            else:
                print('\n!!!!!Place not empty, choose different place.!!!!!')
        display(ttt)
        winner = check_winner(ttt)
        if winner == 'X' or winner == 'O':
            print(f'\n------ {winner} won. ------')
            break
        elif winner == 'tie':
            print('\n------ Tie! ------')
            break

print('Welcome to Tic Tac Toe\n')
while True:
    user_input = input('1: Player vs Player\n2. Player vs Computer(easy)\n3. Player vs Computer(hard)\nany other input will exit game!')
    if user_input == '1':
        player_vs_player()
    elif user_input == '2':    
        player_vs_computer()
    elif user_input == '3':    
        player_vs_algo()
    else:
        break
print('Bye!!')

