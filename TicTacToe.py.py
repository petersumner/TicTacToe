import sys
import random

# List of spaces
spaces = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

# List of possible ways to win
wins = [['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'], ['A1', 'B1', 'C1'],
        ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3'], ['A1', 'B2', 'C3'], ['A3', 'B2', 'C1']]

# List of corners
corners = ['A1', 'A3', 'C1', 'C3']

class Game:
    def __init__(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]

    def reset(self):
        choice = input("Would you like to try again? (Y/N) ")
        if choice == 'Y' or choice == 'y':
            self.board = [[' ' for i in range(3)] for j in range(3)]
            self.playerTurn()
        elif choice == 'N' or choice == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Hmm ... that wasn't an option.")
            self.reset()

    def printBoard(self):
        col = 'A'
        for row in self.board:
            print("  -------------")
            print(col + " | " + row[0] + " | " + row[1] + " | " + row[2] + " | ")
            col = chr(ord(col) + 1)
        print("  -------------")
        print("    1   2   3")

    def playerTurn(self):
        pick = input("Enter a space: ")

        # Catch inputs that are the wrong length
        if len(pick) != 2:
            print("Something's not right ... try again")
            self.playerTurn()

        # Catch inputs with invalid row
        elif pick[0] != 'A' and pick[0] != 'B' and pick[0] != 'C':
            print("Try picking row 'A', 'B', or 'C'")
            self.playerTurn()

        # Catch inputs with invalid column
        elif pick[1] != '1' and pick[1] != '2' and pick[1] != '3':
            print("Try picking a valid column")
            self.playerTurn()

        # Catch inputs that are already filled
        elif self.board[int(ord(pick[0]) - ord('A'))][int(pick[1])-1] != ' ':
            print('Nice try, that space is already taken')
            self.playerTurn()

        else:
            self.board[int(ord(pick[0])-ord('A'))][int(pick[1])-1] = 'X'
            self.aiTurn()

    def checkWin(self):

        # End game if the board is full
        emptySpaces = 0
        for row in self.board:
            if ' ' in row:
                emptySpaces += 1
        if emptySpaces == 0:
            self.printBoard()
            print("It's a draw.")
            self.reset()

        # End game if AI or player has won
        for trio in wins:
            first = self.board[int(ord(trio[0][0])-ord('A'))][int(trio[0][1])-1]
            second = self.board[int(ord(trio[1][0])-ord('A'))][int(trio[1][1])-1]
            third = self.board[int(ord(trio[2][0])-ord('A'))][int(trio[2][1])-1]
            if first == second == third and first != ' ':
                if first == 'O':
                    print('You lose.')
                    self.reset()
                elif first == 'X':
                    print('You win, you big cheater.')
                    self.reset()

    def checkPair(self):
        choice = ' '

        # Check if the AI can win on this turn and end the game
        for trio in wins:
            count = 0
            for space in trio:
                if self.board[int(ord(space[0])-ord('A'))][int(space[1])-1] == 'O':
                    count += 1
                elif self.board[int(ord(space[0])-ord('A'))][int(space[1])-1] == 'X':
                    count = 0
                    break
                else:
                    choice = space
            if count == 2:
                return choice

        # Block the player from winning on the next turn
        for trio in wins:
            count = 0
            for space in trio:
                if self.board[int(ord(space[0])-ord('A'))][int(space[1])-1] == 'X':
                    count += 1
                elif self.board[int(ord(space[0])-ord('A'))][int(space[1])-1] == 'O':
                    count = 0
                    break
                else:
                    choice = space
            if count == 2:
                return choice
        return choice

    def pickEmpty(self, squares):
        # AI chooses an empty space randomly given a list of options
        choice = random.choice(squares)
        if self.board[int(ord(choice[0]) - ord('A'))][int(choice[1]) - 1] != ' ':
            self.pickEmpty(squares)
        else:
            return choice

    def aiTurn(self):
        choice = ''
        self.checkWin()

        # If player did not choose center on their first turn, AI chooses center
        # If center it taken, AI picks a random corner
        if self.board.count([' ', ' ', ' ']) == 2:
            if self.board[1][1] == ' ':
                self.board[1][1] = 'O'
                choice = 'B2'
            else:
                choice = self.pickEmpty(corners)
        else:
            print('checking pairs')
            choice = self.checkPair()
            if choice == ' ':
                choice = self.pickEmpty(spaces)

        self.board[int(ord(choice[0])-ord('A'))][int(choice[1])-1] = 'O'
        self.printBoard()
        print("I choose " + choice)
        self.checkWin()
        self.playerTurn()

    def run(self):
        self.printBoard()
        self.playerTurn()


Game().run()
