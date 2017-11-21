import random

BLACK_TILE = "X"
WHITE_TILE = "O"
EMPTY_TILE = "."


class Board:
    def __init__(self):
        self.board = []
        self.letter_to_digit_map = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7
        }
        self.digit_to_letter_map = {
            0 : "a",
            1 : "b",
            2 : "c",
            3 : "d",
            4 : "e",
            5 : "f",
            6 : "g",
            7 : "h"
        }

    def reset(self):
        self.board = [[EMPTY_TILE] * 8 for i in range(8)]
        self.board[3][3] = WHITE_TILE
        self.board[3][4] = BLACK_TILE
        self.board[4][3] = BLACK_TILE
        self.board[4][4] = WHITE_TILE

    def print_board(self):
        print("    a b c d e f g h")
        #print("    0 1 2 3 4 5 6 7")
        print("  *******************")
        for row in range(8):
            print(row + 1, "* ", end = "")
            for col in range(8):
                print(self.board[row][col], "" if col == 7 else "", end = "")
            print("*", end = "")
            print()
        print("  *******************")

    def letter_to_digit(self, coord):
        return [int(coord[1]) - 1, self.letter_to_digit_map[coord[0]]]

    def digit_to_letter(self, coord):
        return self.digit_to_letter_map[coord[0]] + str(int(coord[1]) + 1)

    def is_on_board(self, row, col):
        return (row >= 0) and (row <= 7) and (col >= 0) and (col <= 7)

    def is_valid_move(self, row, col, color):
        if not self.is_on_board(row, col):
            return False
        if self.board[row][col] != EMPTY_TILE:
            return False
        my_tile = BLACK_TILE if color == 1 else WHITE_TILE
        opp_tile = WHITE_TILE if my_tile == BLACK_TILE else BLACK_TILE
        dir = [-1, 0, 1]        
        for dx in dir:
            for dy in dir:
                if ((dx != 0) or (dy != 0)):
                    cnt_to_flip = 0
                    curr_row = row
                    curr_col = col
                    while self.is_on_board(curr_row + dy, curr_col + dx):
                        next_tile = self.board[curr_row + dy][curr_col + dx]
                        if (next_tile != opp_tile):
                            break
                        curr_row += dy
                        curr_col += dx
                        cnt_to_flip += 1
                    if (cnt_to_flip > 0) and self.is_on_board(curr_row + dy, curr_col + dx) and next_tile == my_tile:
                        return True
        return False
        
    def gen_valid_moves(self, color):
        valid_moves = []        
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, color):
                    valid_moves.append([row, col])
        return valid_moves



    def gen_random_move(self, color):        
        valid_moves = self.gen_valid_moves(color)
        return valid_moves[random.randint(0, len(valid_moves) - 1)]

    def make_move(self, move, color):        
        my_tile = BLACK_TILE if color == 1 else WHITE_TILE
        opp_tile = WHITE_TILE if my_tile == BLACK_TILE else BLACK_TILE
        row = move[0]
        col = move[1]
        self.board[row][col] = my_tile
        dir = [-1, 0, 1]
        for dx in dir:
            for dy in dir:
                if (dx != 0) or (dy != 0):
                    tiles_to_flip = []                    
                    curr_row = row
                    curr_col = col
                    while self.is_on_board(curr_row + dy, curr_col + dx):
                        next_tile = self.board[curr_row + dy][curr_col + dx]
                        if (next_tile != opp_tile):
                            break
                        tiles_to_flip.append([curr_row + dy, curr_col + dx])
                        curr_row += dy
                        curr_col += dx
                    if self.is_on_board(curr_row + dy, curr_col + dx) and (next_tile == my_tile) and (len(tiles_to_flip) > 0):
                        for tile in tiles_to_flip:
                            self.board[tile[0]][tile[1]] = my_tile
                        tiles_to_flip.clear()

    def has_valid_move(self, color):        
        return (len(self.gen_valid_moves(color)) > 0)



def main():
    board = Board()
    player_color = 0
    bot_color = 0
    color_to_move = 1#1 stands for black, -1 stands for white
    side_to_move =  0#1 stands for player, -1 stands for bot
    game_is_over = False
    while (True):
        print("Choose your color: X (Black) or O (White)")
        player_color_input = input(">>")
        player_color = 1 if player_color_input == BLACK_TILE else -1
        bot_color = -player_color
        side_to_move = 1 if player_color == 1 else -1;
        print("Player color: {}, bot color: {}".format(player_color, bot_color))
        board.reset()

        while not game_is_over:
            board.print_board()
            if (side_to_move == 1):
                print("it's player move")
                while True:
                    print("Print your next move: ")
                    player_input = input(">>")
                    player_move = board.letter_to_digit(player_input)
                    if board.is_valid_move(player_move[0], player_move[1], player_color):
                        print("player made move: {}".format(player_input))
                        board.make_move(player_move, player_color)            
                        break
                    else:
                        print("Error. Invalid move. Try again.")
            else:
                print("it's bot move")
                bot_move = board.gen_random_move(bot_color)
                bot_string_move = board.digit_to_letter(bot_move)
                print("bot made move: {}".format(bot_string_move))
                board.make_move(bot_move, bot_color)
            if board.has_valid_move(-color_to_move):
                side_to_move = -side_to_move
                color_to_move = -color_to_move
            elif not(board.has_valid_move(color_to_move)):
                print("Game is finished")
                game_is_over = True

if __name__ == "__main__":
    main()