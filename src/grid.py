import pygame
from button import Button
from tokens import Token
from color import Color
import os
import sys

# Lấy đường dẫn tuyệt đối đến thư mục gốc của dự án
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'images')

# Các hàm tiện ích
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Kiểm tra để xác định các hướng hợp lệ từ ô hiện tại."""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x != maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections

def loadImages(path, size):
    """Tải một hình ảnh vào game và thay đổi kích thước hình ảnh."""
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """Tải và xử lý sprite sheet."""
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image


class Grid:
    def __init__(self, rows, columns, size, main):
        self.color = Color()
        
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        token_size = (size[0]*7/8, size[1]*7/8)

        # Tải hình ảnh token và hình ảnh chuyển đổi sử dụng đường dẫn tuyệt đối
        self.whitetoken = loadImages(os.path.join(IMAGES_DIR, 'WhiteToken_New.png'), token_size)
        self.blacktoken = loadImages(os.path.join(IMAGES_DIR, 'BlackToken_New.png'), token_size)
        self.transitionWhiteToBlack = [loadImages(os.path.join(IMAGES_DIR, f'BlackToWhite{i}_New.png'), self.size) for i in range(1, 4)]
        self.transitionBlackToWhite = [loadImages(os.path.join(IMAGES_DIR, f'WhiteToBlack{i}_New.png'), self.size) for i in range(1, 4)]
       
        self.tokens = {}

        # Tải nền lưới.
        self.gridBg = self.createbgimg()

        # Lưới cho việc sử dụng logic.
        self.gridLogic = self.regenGrid(self.y, self.x)

        # Điểm số của hai người chơi.
        self.player1Score = 0
        self.player2Score = 0

        # Danh sách các nút trong lưới.
        self.play_button = Button('Play', 460, 380)
        self.quit_menu_button = Button('Quit', 460, 480)
        self.resume_button = Button('Resume', 420, 350)
        self.retry_button = Button('Retry', 440, 450)
        self.quit_pause_button = Button('Quit', 450, 550)
        self.pause_button = Button('Pause', 775, 400)
        self.black_button = Button('Black', 440, 350)
        self.white_button = Button('White', 440, 450)
        self.CoinParity_button = Button('Coin Parity', 200, 200)
        self.Corner_button = Button('Corner', 200, 300)
        self.Mobility_button = Button('Mobility', 200, 400)
        self.Stability_button = Button('Stability', 200, 500)
        self.StaticBoard_button = Button('Static Board', 200, 600)
        self.E_coins_button = Button('E-coins', 600, 200)
        self.E_corner_button = Button('E-corner', 600, 300)
        self.E_mobility_button = Button('E-mobility', 600, 400)
        self.E_stability_button = Button('E-stability', 600, 500)
        self.Everything_button = Button('Everything', 600, 600)
        self.depth1_button = Button('1', 300, 200)
        self.depth2_button = Button('2', 300, 300)
        self.depth3_button = Button('3', 300, 400)
        self.depth4_button = Button('4', 300, 500)
        self.depth5_button = Button('5', 700, 200)
        self.depth6_button = Button('6', 700, 300)
        self.depth7_button = Button('7', 700, 400)
        self.depth8_button = Button('8', 700, 500)

        # Font được sử dụng.
        self.font = pygame.font.SysFont('Candara', 40, True, False)


        
    def newGame(self):
        '''Khởi động lại game.'''

        # Đặt lại một số thuộc tính của game
        self.GAME.time = pygame.time.get_ticks()
        self.GAME.opponentSelected = False
        self.GAME.depthSelected = False
        self.GAME.sideSelected = False
        self.GAME.gameOver = False
        self.GAME.paused = False
        self.GAME.passGame = False
        self.GAME.currentPlayer = -1
        self.GAME.playerSide = -1

        # Xóa các token và tạo lại lưới logic.
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)
        
        pygame.time.delay(100)
    
    def createbgimg(self):
        '''Tạo nền cho lưới.'''
        
        image = pygame.Surface((730, 730))
        color = self.color.grey
        image.fill(color)
        
        image0 = pygame.Surface((76, 76))
        image0.fill(self.color.lightPink)
        for i in range (8):
            for j in range (8):
                image.blit(image0, (2 + (i+1) * self.size[0], 2 + (j+1) * self.size[1])) 
        
        image1 = pygame.Surface((70, 730))
        image1.fill(self.color.pinkBg)
        
        image2 = pygame.Surface((730, 70))
        image2.fill(self.color.pinkBg)
        
        image.blit(image1, (0,0))
        image.blit(image2, (0,0))
        return image

    def regenGrid(self, rows, columns):
        """Tạo lưới với vị trí bắt đầu cho việc sử dụng logic."""
        
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid

    def calculatePlayerScore(self, player):
        '''Tính điểm số của 2 người chơi.'''
        
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        '''Vẽ điểm số của 2 người chơi lên màn hình.'''
        
        textImg = self.font.render(f'{player} : {score}', 1, self.color.purple)
        return textImg

    def drawMoveCount(self):
        '''Vẽ số nước đi hiện tại lên màn hình.'''
        total_moves = self.player1Score + self.player2Score - 4  # Trừ đi 4 quân ban đầu
        textImg = self.font.render(f'Move: {total_moves}/60', 1, self.color.purple)
        return textImg

    def drawMenu(self, window):
        '''Vẽ màn hình menu chính.'''
        
        if self.play_button.draw(window):
            self.GAME.menu = True
            pygame.time.delay(100)
        if self.quit_menu_button.draw(window):
            self.GAME.RUN = False
            return

    def drawOpponentSelection(self, window):
        '''Vẽ màn hình chọn đối thủ.'''
        
        description = self.font.render('Choose your opponent!', 1, self.color.purple)
        window.blit(description, (300, 100))
        if self.CoinParity_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.computerCoinParity
            self.GAME.opponentSelected = True
        if self.Corner_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.computerCornerCapture
            self.GAME.opponentSelected = True
        if self.Mobility_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.computerMobility
            self.GAME.opponentSelected = True
        if self.Stability_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.computerStability
            self.GAME.opponentSelected = True
        if self.StaticBoard_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.computerStaticBoard
            self.GAME.opponentSelected = True
        if self.E_coins_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.E_coins
            self.GAME.opponentSelected = True
        if self.E_corner_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.E_corner
            self.GAME.opponentSelected = True
        if self.E_mobility_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.E_mobility
            self.GAME.opponentSelected = True
        if self.E_stability_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.E_stability
            self.GAME.opponentSelected = True
        if self.Everything_button.draw(window):
            self.GAME.heuristic = self.GAME.computerPlayer.Everything
            self.GAME.opponentSelected = True

    def drawSideSelection(self, window):
        '''Draw the side selection screen.'''
        
        description = self.font.render('Choose your color!', 1, self.color.purple)
        window.blit(description, (330, 100))
        if self.black_button.draw(window):
            self.GAME.playerSide = -1
            self.GAME.sideSelected = True
        if self.white_button.draw(window):
            self.GAME.playerSide = 1
            self.GAME.sideSelected = True

    def drawDepthSelection(self, window):
        '''Draw the depth selection screen.'''
        
        description = self.font.render('Choose the depth of your opponent!', 1, self.color.purple)
        window.blit(description, (200, 100))
        if self.depth1_button.draw(window):
            self.GAME.depth = 1
            self.GAME.depthSelected = True
        if self.depth2_button.draw(window):
            self.GAME.depth = 2
            self.GAME.depthSelected = True
        if self.depth3_button.draw(window):
            self.GAME.depth = 3
            self.GAME.depthSelected = True
        if self.depth4_button.draw(window):
            self.GAME.depth = 4
            self.GAME.depthSelected = True
        if self.depth5_button.draw(window):
            self.GAME.depth = 5
            self.GAME.depthSelected = True
        if self.depth6_button.draw(window):
            self.GAME.depth = 6
            self.GAME.depthSelected = True
        if self.depth7_button.draw(window):
            self.GAME.depth = 7
            self.GAME.depthSelected = True
        if self.depth8_button.draw(window):
            self.GAME.depth = 8
            self.GAME.depthSelected = True

    def endScreen(self):
        '''Draw the game over screen.'''
        
        if self.GAME.gameOver:
            if self.GAME.playerSide == -1:
                player_score = self.player1Score
                computer_score = self.player2Score
            else:
                player_score = self.player2Score
                computer_score = self.player1Score
        
            # Print the game over screen.    
            endScreenImg = pygame.Surface((400, 240))
            endScreenImg.fill(self.color.red)
            endText = self.font.render(f'{"Congrats, You Won!!" if player_score > computer_score else "Bad Luck, You Lost" if player_score < computer_score else "       Draw       "}', 1, self.color.lightPink)
            endScreenImg.blit(endText, (40, 40))
            newGame = pygame.draw.rect(endScreenImg, self.color.lightPink, (120, 120, 160, 80))
            newGameText = self.font.render(' Retry', 1, self.color.red)
            endScreenImg.blit(newGameText, (142, 145))
        return endScreenImg

    def drawPauseScreen(self, window):
        '''Draw the pause screen.'''
        
        description = self.font.render('Game Paused', 1, self.color.purple)
        window.blit(description, (380, 100))
        if self.resume_button.draw(window):
            self.GAME.paused = False
            pygame.time.delay(100)
        if self.retry_button.draw(window):
            pygame.time.delay(100)
            self.newGame()
        if self.quit_pause_button.draw(window):
            self.GAME.RUN = False 

    def passScreen(self):
        '''Draw the pass button.'''
        
        passScreenImg = pygame.Surface((80, 40))
        passScreenImg.fill(self.color.pinkBg)
        passGameText = self.font.render('Pass', 1, self.color.purple)
        passScreenImg.blit(passGameText, (0, 0))
        return passScreenImg            

    def drawGrid(self, window):
        '''Draw everything (grid, tokens, buttons) on the screen.'''
        
        # Draw the menu if the game has not started yet
        if not self.GAME.menu:
            self.drawMenu(window)
            return

        # Draw the opponent selection menu
        if self.GAME.menu and not self.GAME.opponentSelected:
            self.drawOpponentSelection(window)
            return

        # Draw the depth selection menu
        if self.GAME.opponentSelected and not self.GAME.depthSelected:
            self.drawDepthSelection(window)
            return

        # Draw the side selection menu
        if self.GAME.depthSelected and not self.GAME.sideSelected:
            self.drawSideSelection(window)
            return

        # Draw the pause screen if the game is paused
        if self.GAME.paused:
            self.drawPauseScreen(window)
            return

        # Draw the grid background.
        window.blit(self.gridBg, (0, 0))

        # Draw the score of 2 players.
        window.blit(self.drawScore('Black', self.player1Score), (775, 100))
        window.blit(self.drawScore('White', self.player2Score), (775, 200))
        window.blit(self.drawMoveCount(), (775, 300))  # Hiển thị số nước đi

        # Draw the tokens.
        for token in self.tokens.values():
            token.draw(window)

        # Indicate all available moves.
        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)

        # Indicate the last move on the board.
        if self.GAME.lastMove != None:
            x = self.GAME.lastMove[1]
            y = self.GAME.lastMove[0]
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) - 1, 80 + (y * 80) - 1), (80 + (x * 80) - 1, 80 + (y * 80) + 9), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) - 1, 80 + (y * 80) - 1), (80 + (x * 80) + 9, 80 + (y * 80) - 1), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) - 1, 80 + (y * 80) + 79), (80 + (x * 80) + 9, 80 + (y * 80) + 79), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) - 1, 80 + (y * 80) + 79), (80 + (x * 80) - 1, 80 + (y * 80) + 69), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) + 79, 80 + (y * 80) - 1), (80 + (x * 80) + 69, 80 + (y * 80) - 1), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) + 79, 80 + (y * 80) - 1), (80 + (x * 80) + 79, 80 + (y * 80) + 9), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) + 79, 80 + (y * 80) + 79), (80 + (x * 80) + 79, 80 + (y * 80) + 69), 2)
            pygame.draw.line(window, self.color.indicateColor, (80 + (x * 80) + 79, 80 + (y * 80) + 79), (80 + (x * 80) + 69, 80 + (y * 80) + 79), 2)
        if self.GAME.currentPlayer == self.GAME.playerSide:
            for move in availMoves:
                pygame.draw.rect(window, (215, 136, 109), (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))
        
        # Draw the pause button
        if self.pause_button.draw(window):
            self.GAME.paused = True

        # Draw the game over screen if the game is over.
        if self.GAME.gameOver:            
            window.blit(self.endScreen(), (200, 280))

        # Draw the pass button if a player has no moves available.
        if self.GAME.passGame:            
            window.blit(self.passScreen(), (775, 300))

    def printGameLogicBoard(self):
        '''Print the logical grid to the terminal.'''
        
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:
                        continue

                    validCellToClick.append((gridX, gridY))
        return validCellToClick

    def swappableTiles(self, x, y, grid, player):
        '''Return list of tiles that can be swapped after a move.'''
        
        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles

    def findAvailMoves(self, grid, currentPlayer):
        """Takes the list of validCells and checks each to see if playable.
        Return the list of available moves."""
        
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            #if len(swapTiles) > 0 and cell not in playableCells:
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells

    def insertToken(self, grid, curplayer, y, x):
        '''Insert a token.'''
        
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def animateTransitions(self, cell, player):
        '''Animate the transitions when swapping tiles.'''
        
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)

