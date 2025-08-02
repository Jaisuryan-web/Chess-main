import chess as ch
import pygame
import math
import tkinter as tk
from tkinter import messagebox 

def evaluatePosition(board, pieces):
    pass

def showVictoryPopup(winner, game_type):
    """Show a victory popup message using tkinter"""
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    if game_type == "checkmate":
        title = "🏆 CHECKMATE! 🏆"
        message = f"Congratulations!\n\n{winner} WINS by Checkmate!\n\nWell played!"
    elif game_type == "stalemate":
        title = "🤝 STALEMATE 🤝"
        message = "It's a Draw!\n\nStalemate - No legal moves available\nbut the king is not in check."
    else:
        title = "🤝 DRAW 🤝"
        message = "The game ends in a draw!"
    
    # Show the message box
    messagebox.showinfo(title, message)
    root.destroy()  # Clean up the root window
def gameStateCheck(board:ch.board, pieces) -> int:
    """Returns an integer corresponding to game state. 0->Can Continue 1->Checkmate 2->Stalemate 3->Draw.
    Draw condition to be implemented"""
    end = 0
    possibleMoves = board.allPossibleMoves(pieces, board.turn)
    canMove = False
    for values in possibleMoves.values():
        if values:
            canMove = True
            break
    if not canMove:
        if board.checkForcheck(pieces, board.turn):
            #king is in check
            end = 1
            print("Checkmate!", board.fullColour(board.oppositeColour(board.turn)),  "Wins!")
        else:
            #stalemate
            end = 2
            print("Stalemate!")
    return end

def drawBG(win):
    """Draw a modern, elegant chess board with borders and coordinates"""
    # Fill background with dark border color
    win.fill(borderColor)
    
    # Draw main board area
    board_rect = pygame.Rect(boardMargin, boardMargin, boardSize, boardSize)
    pygame.draw.rect(win, boardBorderColor, board_rect)
    pygame.draw.rect(win, boardBorderColor, board_rect, 4)
    
    # Draw squares with gradient effect
    for row in range(rows):
        for col in range(cols):
            x = boardMargin + col * squareSize
            y = boardMargin + row * squareSize
            
            # Alternate colors
            if (row + col) % 2 == 0:
                color = lightSquareColor
                shadow_color = lightSquareShadow
            else:
                color = darkSquareColor
                shadow_color = darkSquareShadow
            
            # Draw square with subtle gradient effect
            square_rect = pygame.Rect(x, y, squareSize, squareSize)
            pygame.draw.rect(win, color, square_rect)
            
            # Add subtle inner shadow for depth
            pygame.draw.rect(win, shadow_color, (x, y, squareSize, 2))
            pygame.draw.rect(win, shadow_color, (x, y, 2, squareSize))
    
    # Draw coordinate labels
    drawCoordinates(win)

def drawCoordinates(win):
    """Draw coordinate labels (a-h, 1-8) around the board"""
    font = pygame.font.Font(None, 24)
    
    # Draw file labels (a-h) at bottom
    for i in range(8):
        letter = chr(ord('a') + i)
        text = font.render(letter, True, coordinateColor)
        text_rect = text.get_rect()
        x = boardMargin + i * squareSize + squareSize // 2 - text_rect.width // 2
        y = boardMargin + boardSize + 10
        win.blit(text, (x, y))
    
    # Draw rank labels (1-8) on left side
    for i in range(8):
        number = str(8 - i)
        text = font.render(number, True, coordinateColor)
        text_rect = text.get_rect()
        x = boardMargin - 25
        y = boardMargin + i * squareSize + squareSize // 2 - text_rect.height // 2
        win.blit(text, (x, y))

def drawPieces(win, pieces):
    """Draw chess pieces with enhanced positioning and shadow effects"""
    for r in range(rows):
        for c in range(cols):
            piece = pieces[r][c]
            if piece is None:
                continue
            else:
                # Calculate position with board margin
                x = boardMargin + c * squareSize + (squareSize - pieceSize) // 2
                y = boardMargin + r * squareSize + (squareSize - pieceSize) // 2
                
                # Load and scale piece image
                img = pygame.transform.scale(pygame.image.load("images/"+ str(piece)+".png"),
                                             (pieceSize, pieceSize))
                
                # Draw subtle shadow for depth
                shadow_offset = 3
                shadow_surface = pygame.Surface((pieceSize, pieceSize), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 50))
                win.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
                
                # Draw the piece
                win.blit(img, (x, y))

def drawPossibleMoves(win, legalMoves):
    """Draw enhanced possible move indicators with glowing effects"""
    if legalMoves is not None:
        for i in legalMoves:
            # Calculate position with board margin
            center_x = boardMargin + i[1] * squareSize + squareSize // 2
            center_y = boardMargin + i[0] * squareSize + squareSize // 2
            
            # Draw glowing effect with multiple circles
            for radius_offset in range(3, 0, -1):
                alpha = 30 + (3 - radius_offset) * 20
                glow_surface = pygame.Surface((squareSize, squareSize), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*possibleMoveClr, alpha), 
                                 (squareSize // 2, squareSize // 2), 
                                 squareSize // 6 + radius_offset * 2)
                win.blit(glow_surface, (center_x - squareSize // 2, center_y - squareSize // 2))
            
            # Draw main indicator circle
            pygame.draw.circle(win, possibleMoveClr, (center_x, center_y), squareSize // 8)
            pygame.draw.circle(win, possibleMoveOutline, (center_x, center_y), squareSize // 8, 2)

def main():
    clock = pygame.time.Clock()
    run = True
    selectedPiece = []
    legalMoves = None
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                # Adjust for board margin
                adjusted_x = loc[0] - boardMargin
                adjusted_y = loc[1] - boardMargin
                
                # Check if click is within the board
                if 0 <= adjusted_x < boardSize and 0 <= adjusted_y < boardSize:
                    c = int(adjusted_x // squareSize)
                    r = int(adjusted_y // squareSize)
                else:
                    continue  # Click outside board, ignore
                if selectedPiece == [r, c]:
                    selectedPiece = []
                else:
                    if selectedPiece:
                        if b.legalMoves(p, selectedPiece) is not None:
                            if [r, c] in b.legalMoves(p, selectedPiece):
                                b.movePiece(p, selectedPiece, [r, c])
                                gameStateCheck(b, p)
                                selectedPiece = []
                            else:
                                selectedPiece = [r, c]
                        else:
                            selectedPiece = [r, c]
                    else:
                        selectedPiece = [r, c]
                legalMoves = b.legalMoves(p, selectedPiece)
        drawBG(WIN)
        drawPieces(WIN, p)
        drawPossibleMoves(WIN, legalMoves)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    #Modern Design Constants
    width = 1000
    height = 1000
    rows = cols = 8
    boardMargin = 80  # Space around the board for coordinates
    boardSize = 800   # Size of the actual chess board
    squareSize = boardSize // cols
    pieceSize = int(squareSize * 0.85)  # Slightly smaller pieces for better fit
    
    # Classic Black and White Color Scheme
    borderColor = (25, 25, 35)           # Dark background
    boardBorderColor = (60, 60, 70)      # Board border
    lightSquareColor = (255, 255, 255)   # Light squares - pure white
    darkSquareColor = (0, 0, 0)          # Dark squares - pure black
    lightSquareShadow = (235, 235, 235)  # Light square shadow
    darkSquareShadow = (20, 20, 20)      # Dark square shadow
    coordinateColor = (200, 200, 210)    # Coordinate labels
    possibleMoveClr = (76, 175, 80)      # Green for possible moves
    possibleMoveOutline = (56, 142, 60)  # Darker green outline
    FPS = 60
    #Init
    b = ch.board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    p = b.pieces
    b.generateFen(p)
    #p = b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #for checking enpassant 8/p7/8/1P6/8/8/6k1/R3K3 b - - 0 1
    '''
    b.addPiece(p, 'queen', 'W', ch.getPosFromStdNotation('b2'))
    b.addPiece(p, 'king', 'W', ch.getPosFromStdNotation('a1'))
    b.addPiece(p, 'queen', 'B', ch.getPosFromStdNotation('h8'))
    b.legalMoves(p, ch.getPosFromStdNotation('b2'))
    print(str([[str(j) for j in i] for i in p]).split("-"))
    '''

    #Pygame initialization and render
    pygame.init()  # Initialize all pygame modules
    pygame.font.init()  # Initialize font module specifically
    WIN = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chess by Jai')
    pygame.display.update()
    main()