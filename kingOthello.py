from othello import Othello
from othello import EMPTY, BLACK, WHITE, DIRECTIONS
from othello import opposite, is_inbound

BLACK_KING = 3
WHITE_KING = 4


def king(player: int):
    if player == BLACK:
        return BLACK_KING
    elif player == WHITE:
        return WHITE_KING


class KingOthello(Othello):

    def __init__(self):
        super(KingOthello, self).__init__()

    def is_valid_move(self, x, y, is_king=False):
        # if is_king=True, decide whether the move is valid for a king piece, else calculate only for a normal piece
        if is_inbound(x, y) and self.board[x, y] == EMPTY:
            if not is_king: # only valid
                for direction in DIRECTIONS:
                    new_x, new_y = x + direction[0], y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(
                            self.current_player):  # make sure >= 1 opposite
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(self.current_player)]:
                            return True  # find one valid is enough
                return False
            else: # this is a king piece
                opp_king = king(opposite(self.current_player))
                for direction in DIRECTIONS:
                    met_opponent_king = False # whether has enemy king in middle, if so, the two end must be self's two kings to reverse
                    new_x, new_y = x + direction[0], y + direction[1]
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] in \
                            [opposite(self.current_player), opp_king]:
                        if self.board[new_x, new_y] == opp_king:
                            met_opponent_king = True
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] in \
                            [opposite(self.current_player), opp_king]:
                            if self.board[new_x, new_y] == opp_king:
                                met_opponent_king = True
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player,
                                                                                     king(self.current_player)]:
                            if not met_opponent_king:
                                return True  # find one valid is enough
                            else: # have opponent's king in middle
                                if self.board[new_x, new_y] == king(self.current_player):
                                    return True
                return False

        else: # occupied or out of bound
            return False

    def take_move(self, x, y, is_king=False):
        if self.is_valid_move(x, y, is_king=is_king):
            if not is_king:
                self.board[x, y] = self.current_player
            else:
                self.board[x, y] = king(self.current_player)
            pieces_to_reverse = []
            for direction in DIRECTIONS:
                new_x, new_y = x + direction[0], y + direction[1]
                temp_list = [] # temp storage for each direction
                if not is_king:
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] == opposite(self.current_player):
                            temp_list.append((new_x, new_y))
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(self.current_player)]: # valid direction
                            pieces_to_reverse.extend(temp_list) # move to final container
                else: # king
                    met_opponent_king = False
                    if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [opposite(self.current_player), king(opposite(self.current_player))]:
                        if self.board[new_x, new_y] == king(opposite(self.current_player)):
                            met_opponent_king = True
                        while is_inbound(new_x, new_y) and self.board[new_x, new_y] in [opposite(self.current_player), king(opposite(self.current_player))]:
                            if self.board[new_x, new_y] == king(opposite(self.current_player)):
                                met_opponent_king = True
                            temp_list.append((new_x, new_y))
                            new_x, new_y = new_x + direction[0], new_y + direction[1]
                        if is_inbound(new_x, new_y) and self.board[new_x, new_y] in [self.current_player, king(
                                self.current_player)]:  # valid direction
                            if not met_opponent_king:
                                pieces_to_reverse.extend(temp_list)  # move to final container
                            else: # has opponent king in middle, only reverse if two ends of this line are both self's king
                                if self.board[new_x, new_y] == king(self.current_player):
                                    pieces_to_reverse.extend(temp_list)

            for coord in pieces_to_reverse: # all pieces in the middle, no matter king or not, will be turned to normal enemy pieces
                self.board[coord[0], coord[1]] = self.current_player
        else:
            print("Invalid move.")


    def print_board(self):
        # ♔♚♕♛
        # print board in command line, added icons for king pieces for each side
        EMPTY_PIECE = '+'
        BLACK_PIECE = '⚫'
        BLACK_KING_PIECE = '♚'
        WHITE_PIECE = '⚪'
        WHITE_KING_PIECE = '♔'
        icon = {EMPTY:EMPTY_PIECE, WHITE : WHITE_PIECE, BLACK : BLACK_PIECE,
                BLACK_KING : BLACK_KING_PIECE, WHITE_KING : WHITE_KING_PIECE}
        print('================================================')
        for row in self.board:
            for i in range(len(row)):
                print(icon[row[i]], end='     ')
            print('\n')
        print('================================================')



# if __name__ == '__main__':
#
#     # g1.print_board()

