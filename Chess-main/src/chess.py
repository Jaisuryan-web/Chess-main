import copy


class piece:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        if self.colour == 'B':
            return f'Black-{self.name}'
        else:
            return f'White-{self.name}'


class pawn(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class bishop(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 3


class knight(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 3


class rook(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 5


class queen(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 9


class king(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1000


# Convert given standard notation postion like a1 to Pos used by code (0,0)
def getPosFromStdNotation(std):
    column = ord(std[0]) - 97
    row = 8 - int(std[1])
    return [row, column]


# Convert given standard notation postion like a1 to Pos used by code (0,0)
def getStdNotationFromPos(pos):
    column = chr(pos[1] + 97)
    row = str(8 - pos[0])
    return column + row


# noinspection PyUnresolvedReferences
class board:

    #Return full colour given short form
    def fullColour(self, colour):
        self.self_is_not_used()
        if colour == 'W':
            return  "White"
        else:
            return "Black"
    # Print the board
    def printBoard(self, pieces):
        self.self_is_not_used()
        print('\n'.join([' '.join([str(j) for j in i]) for i in pieces]), end='\n\n')

    # Self is not used
    def self_is_not_used(self):
        pass

    # Return Opposite Colour
    def oppositeColour(self, colour):
        self.self_is_not_used()
        if colour == 'W':
            return 'B'
        else:
            return 'W'

    # Get a particular piece on board
    def getPiece(self, pieces, pieceType, colour):
        self.self_is_not_used()
        position = []
        for i in range(8):
            for j in range(8):
                if pieces[i][j] is not None:
                    if pieces[i][j].colour == colour and pieces[i][j].name.lower() == pieceType:
                        position = [i, j]
                        break
        return position

    # Get all positions of pieces of a particular colour
    def getPieces(self, pieces, colour):
        self.self_is_not_used()
        positions = []
        for i in range(8):
            for j in range(8):
                if pieces[i][j] is not None:
                    if pieces[i][j].colour == colour:
                        positions.append([i, j])
        return positions

    # Add a piece of particular type and colour to the board
    def addPiece(self, pieces, pieceType, colour, pos):
        self.self_is_not_used()
        if pieces[pos[0]][pos[1]] is None:
            pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    # Remove a piece of particular type and colour to the board
    def removePiece(self, pieces, pos):
        self.self_is_not_used()
        pieces[pos[0]][pos[1]] = None

    # Move piece, TODO promotion
    def movePiece(self, pieces, currPos, targetPos, temp=False):
        pieceType = pieces[currPos[0]][currPos[1]].name.lower()
        colour = pieces[currPos[0]][currPos[1]].colour
        enpassantAssigned = False
        #Pawn
        if pieceType == 'pawn':
            # Enpassant
            enTargetPos = self.checkEnpassant(currPos, colour)
            if targetPos == enTargetPos and pieceType == 'pawn':
                if colour == 'W':
                    self.removePiece(pieces, [enTargetPos[0] + 1, enTargetPos[1]])
                    self.removePiece(pieces, currPos)
                    self.addPiece(pieces, pieceType, colour, targetPos)
                    self.enpassant = '-'
                else:
                    self.removePiece(pieces, [enTargetPos[0] - 1, enTargetPos[1]])
                    self.removePiece(pieces, currPos)
                    self.addPiece(pieces, pieceType, colour, targetPos)
                    self.enpassant = '-'
            else:
                #Promotion
                if colour == 'W':
                    if targetPos[0] == 0:
                        self.removePiece(pieces, targetPos)
                        self.addPiece(pieces, 'queen', colour, targetPos)
                        self.removePiece(pieces,currPos)
                    else:
                        if pieces[targetPos[0]][targetPos[1]] is None:
                            self.addPiece(pieces, pieceType, colour, targetPos)
                            self.removePiece(pieces, currPos)
                            if currPos[0] - targetPos[0] > 1:
                                self.enpassant = getStdNotationFromPos([currPos[0]-1,currPos[1]])
                                enpassantAssigned = True
                        else:
                            self.removePiece(pieces, targetPos)
                            self.addPiece(pieces, pieceType, colour, targetPos)
                            self.removePiece(pieces, currPos)
                else:
                    if targetPos[0] == 7:
                        self.removePiece(pieces, targetPos)
                        self.addPiece(pieces, 'queen', colour, targetPos)
                        self.removePiece(pieces,currPos)
                    else:
                        if pieces[targetPos[0]][targetPos[1]] is None:
                            self.addPiece(pieces, pieceType, colour, targetPos)
                            self.removePiece(pieces, currPos)
                            if targetPos[0] - currPos[0] > 1:
                                self.enpassant = getStdNotationFromPos([currPos[0]+1,currPos[1]])
                                enpassantAssigned = True
                        else:
                            self.removePiece(pieces, targetPos)
                            self.addPiece(pieces, pieceType, colour, targetPos)
                            self.removePiece(pieces, currPos)
        #King
        if pieceType == 'king':
            if colour == 'W':
                if getStdNotationFromPos(targetPos) == 'c1' and currPos == getPosFromStdNotation('e1'):
                    #White Queen side castling
                    self.removePiece(pieces,currPos)
                    self.removePiece(pieces, getPosFromStdNotation('a1'))
                    self.addPiece(pieces, 'king', colour, getPosFromStdNotation('c1'))
                    self.addPiece(pieces, 'rook', colour, getPosFromStdNotation('d1'))
                    self.castling = self.castling.replace('Q', '')
                    self.castling = self.castling.replace('K', '')
                elif getStdNotationFromPos(targetPos) == 'g1' and currPos == getPosFromStdNotation('e1'):
                    #White King side castling
                    self.removePiece(pieces, currPos)
                    self.removePiece(pieces, getPosFromStdNotation('h1'))
                    self.addPiece(pieces, 'king', colour, getPosFromStdNotation('g1'))
                    self.addPiece(pieces, 'rook', colour, getPosFromStdNotation('f1'))
                    self.castling = self.castling.replace('K', '')
                    self.castling = self.castling.replace('Q', '')
                else:
                    #Else normal move
                    if pieces[targetPos[0]][targetPos[1]] is None:
                        self.addPiece(pieces, pieceType, colour, targetPos)
                        self.removePiece(pieces, currPos)
                    else:
                        self.removePiece(pieces, targetPos)
                        self.addPiece(pieces, pieceType, colour, targetPos)
                        self.removePiece(pieces, currPos)
                    self.castling = self.castling.replace('Q', '')
                    self.castling = self.castling.replace('K', '')
            else:
                if getStdNotationFromPos(targetPos) == 'c8' and currPos == getPosFromStdNotation('e8'):
                    #Black Queen side castling
                    self.removePiece(pieces,currPos)
                    self.removePiece(pieces, getPosFromStdNotation('a8'))
                    self.addPiece(pieces, 'king', colour, getPosFromStdNotation('c8'))
                    self.addPiece(pieces, 'rook', colour, getPosFromStdNotation('d8'))
                    self.castling = self.castling.replace('q', '')
                    self.castling = self.castling.replace('k', '')
                elif getStdNotationFromPos(targetPos) == 'g8' and currPos == getPosFromStdNotation('e8'):
                    #Black King side castling
                    self.removePiece(pieces, currPos)
                    self.removePiece(pieces, getPosFromStdNotation('h8'))
                    self.addPiece(pieces, 'king', colour, getPosFromStdNotation('g8'))
                    self.addPiece(pieces, 'rook', colour, getPosFromStdNotation('f8'))
                    self.castling = self.castling.replace('k', '')
                    self.castling = self.castling.replace('q', '')
                else:
                    #Else normal move
                    if pieces[targetPos[0]][targetPos[1]] is None:
                        self.addPiece(pieces, pieceType, colour, targetPos)
                        self.removePiece(pieces, currPos)
                    else:
                        self.removePiece(pieces, targetPos)
                        self.addPiece(pieces, pieceType, colour, targetPos)
                        self.removePiece(pieces, currPos)
                    self.castling = self.castling.replace('q', '')
                    self.castling = self.castling.replace('k', '')
        #Everything other than king
        if pieceType != 'pawn'  and pieceType != 'king':
            # check if rook has moved to remove castling criteria
            if pieceType == 'rook':
                if currPos == getPosFromStdNotation('a1'):
                    self.castling = self.castling.replace('Q', '')
                elif currPos == getPosFromStdNotation('h1'):
                    self.castling = self.castling.replace('K', '')
                elif currPos == getPosFromStdNotation('a8'):
                    self.castling = self.castling.replace('q', '')
                elif currPos == getPosFromStdNotation('h8'):
                    self.castling = self.castling.replace('k', '')
            if pieces[targetPos[0]][targetPos[1]] is None:
                self.addPiece(pieces, pieceType, colour, targetPos)
                self.removePiece(pieces, currPos)
            else:
                self.removePiece(pieces, targetPos)
                self.addPiece(pieces, pieceType, colour, targetPos)
                self.removePiece(pieces, currPos)
        if not temp:
            if colour == 'W':
                self.turn = 'B'
            else:
                self.turn = 'W'
                self.move += 1
            self.generateFen(pieces)
        if not self.castling:
            self.castling = '-'
        if not enpassantAssigned:
            self.enpassant = '-'

    #Get all possible moves for a given colour
    def allPossibleMoves(self, pieces, colour) -> dict:
        """ Returns all possible moves given a colour"""
        myPieces = self.getPieces(pieces, colour)
        moves = {getStdNotationFromPos(i):self.legalMoves(pieces,i) for i in myPieces}
        return  moves

    #Generate fen from given board position
    def generateFen(self, pieces):
        self.self_is_not_used()
        fen = ''
        for r in range(8):
            x = 0
            for c in range(8):
                p = pieces[r][c]
                if p is None:
                    x+=1
                else:
                    fen += str(x) if x else ''
                    x = 0
                    pDict = {'Pawn': 'p', 'Bishop': 'b', 'Rook': 'r', 'King': 'k', 'Queen': 'q', 'Knight': 'n'}
                    if p.colour == 'W':
                        fen+= pDict[p.name].capitalize()
                    else:
                        fen += pDict[p.name]
            if x:
                fen+=str(x)
            fen+='/'
        #Remove last /
        fen = fen[:-1] + ' '
        fen += self.turn.lower() + ' '
        fen += self.castling + ' ' if self.castling != '' else '- '
        fen += self.enpassant + ' ' if self.enpassant != '' else '- '
        fen += str(self.halfmoves) + ' '
        fen += str(self.move)
        print(fen)

    # Fen notation add pieces and set game
    def fen(self, notation:str):
        """Reads input fen notation and returns pieces on the board and sets board variables related to castling,
        enpassant, half moves, turn and move number"""
        pieces = [[None for _ in range(8)] for _ in range(8)]
        fields = notation.split('/')
        fields += fields.pop().split(' ')
        for row in range(8):
            col = 0
            for s in fields[row]:
                if str(s).isdigit():
                    for i in range(int(s)):
                        pieces[row][col] = None
                        col += 1
                else:
                    piece_dict = {'p': 'Bpawn', 'b': 'Bbishop', 'r': 'Brook', 'n': 'Bknight', 'q': 'Bqueen',
                                  'k': 'Bking', 'P': 'Wpawn', 'B': 'Wbishop', 'R': 'Wrook', 'N': 'Wknight',
                                  'Q': 'Wqueen', 'K': 'Wking'}
                    self.addPiece(pieces, piece_dict[str(s)][1:], piece_dict[str(s)][0], (row, col))
                    col += 1
        self.turn = fields[8].upper()
        self.castling = fields[9]
        self.enpassant = fields[10]
        self.halfmoves = fields[11]
        self.move = int(fields[12])
        return pieces

    #Return enpassant moves if possible
    def checkEnpassant(self, pos, colour):
        self.self_is_not_used()
        move = []
        if self.enpassant == '-':
            return None
        else:
            targetPos = getPosFromStdNotation(self.enpassant)
            if colour == 'W':
                if targetPos[0] == 2:
                    if ([pos[0]-1, pos[1]-1] == targetPos) or ([pos[0]-1, pos[1]+1] == targetPos):
                        move = targetPos
            elif colour == 'B':
                if targetPos[1] == 5:
                    if ([pos[0]+1, pos[1]-1] == targetPos) or ([pos[0]+1, pos[1]+1] == targetPos):
                        move = targetPos
        return  move


    # Find all pawn moves
    def generatePawnMoves(self, pieces, pos, colour):
        """Finds all possible pawn moves for a given pawn including that of possibility of moving 2 squares
        from the beginning rank and diagonal capture of enemy pieces."""
        moves = []
        r, c = pos
        if colour == 'W':
            moves.append([r - 1, c]) if pieces[r - 1][c] is None else None
            if pos[0] == 6:
                # Starting squre rule. Can move 2
                moves.append([r - 2, c]) if pieces[r - 2][c] is None and pieces[r - 1][c] is None else None
            oppositePositions = self.getPieces(pieces, self.oppositeColour('W'))
            moves.append([r - 1, c - 1]) if [r - 1, c - 1] in oppositePositions else None
            moves.append([r - 1, c + 1]) if [r - 1, c + 1] in oppositePositions else None
        else:
            moves.append([r + 1, c]) if pieces[r + 1][c] is None else self.self_is_not_used()
            if pos[0] == 1:
                # Starting squre rule. Can move 2
                moves.append([r + 2, c]) if pieces[r + 2][c] is None and pieces[r + 1][c] is None else None
            oppositePositions = self.getPieces(pieces, self.oppositeColour('B'))
            moves.append([r + 1, c - 1]) if [r + 1, c - 1] in oppositePositions else None
            moves.append([r + 1, c + 1]) if [r + 1, c + 1] in oppositePositions else None
        # En passant
        if self.checkEnpassant(pos, colour):
            moves.append(self.checkEnpassant(pos, colour))
        return moves

    # Find all horizontal and vertical(rook) moves possible from a given square
    def generateLinearMoves(self, pieces, pos, colour):
        self.self_is_not_used()
        moves = []
        r, c = pos
        # Left
        while c - 1 >= 0:
            if pieces[r][c - 1] is None:
                moves.append([r, c - 1])
                c -= 1
            elif pieces[r][c - 1].colour != colour:
                moves.append([r, c - 1])
                c -= 1
                break
            else:
                break
        r, c = pos
        # Bottom
        while r + 1 <= 7:
            if pieces[r + 1][c] is None:
                moves.append([r + 1, c])
                r += 1
            elif pieces[r + 1][c].colour != colour:
                moves.append([r + 1, c])
                r += 1
                break
            else:
                break
        r, c = pos
        # Right
        while c + 1 <= 7:
            if pieces[r][c + 1] is None:
                moves.append([r, c + 1])
                c += 1
            elif pieces[r][c + 1].colour != colour:
                moves.append([r, c + 1])
                c += 1
                break
            else:
                break
        r, c = pos
        # Top
        while r - 1 >= 0:
            if pieces[r - 1][c] is None:
                moves.append([r - 1, c])
                r -= 1
            elif pieces[r - 1][c].colour != colour:
                moves.append([r - 1, c])
                r -= 1
                break
            else:
                break
        return moves

    # Find all possible diagonal(bishop) moves possible from a given square taking into consideration enemy and
    # allied pieces
    def generateDiagonalMoves(self, pieces, pos, colour):
        self.self_is_not_used()
        moves = []
        r, c = pos
        # Top left
        while r - 1 >= 0 and c - 1 >= 0:
            if pieces[r - 1][c - 1] is None:
                moves.append([r - 1, c - 1])
                r -= 1
                c -= 1
            elif pieces[r - 1][c - 1].colour != colour:
                moves.append([r - 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Top Right
        while r - 1 >= 0 and c + 1 <= 7:
            if pieces[r - 1][c + 1] is None:
                moves.append([r - 1, c + 1])
                r -= 1
                c += 1
            elif pieces[r - 1][c + 1].colour != colour:
                moves.append([r - 1, c + 1])
                break
            else:
                break
        r, c = pos
        # Bottom Left
        while r + 1 <= 7 and c - 1 >= 0:
            if pieces[r + 1][c - 1] is None:
                moves.append([r + 1, c - 1])
                r += 1
                c -= 1
            elif pieces[r + 1][c - 1].colour != colour:
                moves.append([r + 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Bottom right
        while r + 1 <= 7 and c + 1 <= 7:
            if pieces[r + 1][c + 1] is None:
                moves.append([r + 1, c + 1])
                r += 1
                c += 1
            elif pieces[r + 1][c + 1].colour != colour:
                moves.append([r + 1, c + 1])
                break
            else:
                break
        return moves

    #Return possbile king moves for caslting
    def checkCaslting(self, pieces, colour):
        moves = []
        if colour == 'W':
            if 'K' in self.castling:
                f1 = getPosFromStdNotation('f1')
                g1 = getPosFromStdNotation('g1')
                if pieces[g1[0]][g1[1]] is None and pieces[f1[0]][f1[1]] is None:
                    moves.append(g1)
            if 'Q' in self.castling:
                b1 = getPosFromStdNotation('b1')
                c1 = getPosFromStdNotation('c1')
                d1 = getPosFromStdNotation('d1')
                if pieces[b1[0]][b1[1]] is None and pieces[c1[0]][c1[1]] is None and pieces[d1[0]][d1[1]] is None:
                    moves.append(c1)
        else:
            if 'k' in self.castling:
                f8 = getPosFromStdNotation('f8')
                g8 = getPosFromStdNotation('g8')
                if pieces[g8[0]][g8[1]] is None and pieces[f8[0]][f8[1]] is None:
                    moves.append(g8)
            if 'q' in self.castling:
                b8= getPosFromStdNotation('b8')
                c8 = getPosFromStdNotation('c8')
                d8 = getPosFromStdNotation('d8')
                if pieces[b8[0]][b8[1]] is None and pieces[c8[0]][c8[1]] is None and pieces[d8[0]][d8[1]] is None:
                    moves.append(c8)
        return  moves

    # Check if the colour can check the opposite colour
    def checkForcheck(self, pieces, colour):
        check = False
        oppPieces = self.getPieces(pieces, self.oppositeColour(colour))
        kingPos = self.getPiece(pieces, 'king', colour)
        for p in oppPieces:
            pseudoLegalMoves = self.pseudoLegalMoves(pieces, p)
            if kingPos in pseudoLegalMoves:
                check = True
                break
        return check

    def pseudoLegalMoves(self, pieces, pos):
        if not pos:
            return None
        selectedPiece = pieces[pos[0]][pos[1]]
        if selectedPiece is None:
            return None
        colour = selectedPiece.colour
        pseudoLegalMoves = []
        if selectedPiece.name == 'Pawn':
            pseudoLegalMoves = self.generatePawnMoves(pieces, pos, colour)
        elif selectedPiece.name == 'Rook':
            pseudoLegalMoves = self.generateLinearMoves(pieces, pos, colour)
            # Code castling
        elif selectedPiece.name == 'Bishop':
            pseudoLegalMoves = self.generateDiagonalMoves(pieces, pos, colour)
        elif selectedPiece.name == 'Knight':
            r, c = pos
            rm = [-2, -1, 1, 2, 2, 1, -1, -2]
            cm = [1, 2, 2, 1, -1, -2, -2, -1]
            for i in range(8):
                pseudoLegalMoves.append([r + rm[i], c + cm[i]] if [r + rm[i], c + cm[i]]
                                        not in self.getPieces(pieces, colour)
                                        and (r + rm[i] in range(0, 8))
                                        and (c + cm[i] in range(0, 8))
                                        else None)
        elif selectedPiece.name == 'Queen':
            pseudoLegalMoves = self.generateLinearMoves(pieces, pos, colour)
            pseudoLegalMoves += self.generateDiagonalMoves(pieces, pos, colour)
        elif selectedPiece.name == 'King':
            r, c = pos
            rm = [-1, -1, 0, 1, 1, 1, 0, -1]
            cm = [0, 1, 1, 1, 0, -1, -1, -1]
            for i in range(8):
                pseudoLegalMoves.append([r + rm[i], c + cm[i]] if [r + rm[i], c + cm[i]]
                                        not in self.getPieces(pieces, colour)
                                        and (r + rm[i] in range(0, 8))
                                        and (c + cm[i] in range(0, 8))
                                        else None)
            #Castling
            pseudoLegalMoves += self.checkCaslting(pieces,colour)
        else:
            print("No piece selected!")
        return pseudoLegalMoves

    # Actual legal moves to check for checks
    def legalMoves(self, pieces, pos):
        if not pos:
            return None
        legalMoves = []
        pseudoLegalMoves = self.pseudoLegalMoves(pieces, pos)
        if pseudoLegalMoves:
            colour = pieces[pos[0]][pos[1]].colour
            move = self.move
            enPassant = self.enpassant
            castling = self.castling
            halfMoves = self.halfmoves
            if colour != self.turn:
                return  None
            while None in pseudoLegalMoves:
                pseudoLegalMoves.remove(None)
            for i in pseudoLegalMoves:
                # print(getStdNotationFromPos(i), end='\n')
                # Make a temporary board and try every pseudo legal move and see if the opposite pieces can check king.
                # then remove said pseudo legal move if check. Basically pinning a piece.
                tempBoard = copy.deepcopy(self.pieces)
                self.movePiece(tempBoard, pos, i, True)
                if not self.checkForcheck(tempBoard, colour):
                    legalMoves.append(i)
                self.turn = colour
                self.move = move
                self.enpassant = enPassant
                self.castling = castling
                self.halfmoves = halfMoves
            #[print(getStdNotationFromPos(i), end=' ') for i in legalMoves]
            return legalMoves
        else:
            return  None

    def __init__(self, notation=None):
        if notation is None:
            self.pieces = [[None for _ in range(8)] for _ in range(8)]
            self.move = 0
            self.turn = 'W'
            self.castling = 'KQkq'
            self.enpassant = '-'
            self.halfmoves = 0
        else:
            self.pieces = self.fen(notation)