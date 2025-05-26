import pygame
from button import *
from heuristics import *
from computer_player import ComputerPlayer
from grid import *
from tokens import *
from color import Color

# Định nghĩa lớp game Othello
class Othello:
    def __init__(self):

        pygame.init()
        self.color = Color()
        # Đặt kích thước màn hình
        self.screen = pygame.display.set_mode((1000, 800))

        # Đặt tiêu đề cửa sổ
        pygame.display.set_caption('Othello')

        self.player1 = -1
        self.player2 = 1

        # Màu của người chơi
        self.playerSide = -1

        self.currentPlayer = -1
        self.time = 0
        self.lastMove = None

        self.rows = 8
        self.columns = 8

        # Một số thuộc tính để vẽ menu chính, chọn đối thủ, chọn độ sâu
        # và menu chọn màu.
        self.menu = False
        self.opponentSelected = False
        self.depthSelected = False
        self.sideSelected = False

        self.gameOver = False
        self.paused = False
        self.passGame = False

        # Khởi tạo lưới, người chơi máy, heuristic và độ sâu đã chọn.
        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.computerPlayer = ComputerPlayer(self.grid)
        self.heuristic = None
        self.depth = 1

        self.RUN = True

    def run(self):
        '''Chạy vòng lặp game.'''

        while self.RUN == True:
            self.input()
            self.update()
            self.draw()

    def input(self):
        '''Xử lý đầu vào từ người dùng.'''

        for event in pygame.event.get():
            # Thoát game
            if event.type == pygame.QUIT:
                self.RUN = False

            if self.sideSelected:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Nếu nhấn chuột phải, in lưới logic.
                    if event.button == 3:
                        self.grid.printGameLogicBoard()

                    # Nếu nhấn chuột trái
                    if event.button == 1:
                        if self.currentPlayer == self.playerSide and not self.gameOver and not self.passGame and not self.paused:
                            x, y = pygame.mouse.get_pos()
                            x, y = (x - 80) // 80, (y - 80) // 80
                            validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
                            if not validCells:
                                pass
                            else:
                                # Nếu click vào ô hợp lệ
                                if (y, x) in validCells:
                                    self.lastMove = (y, x)
                                    # Đặt token vào ô
                                    self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                                    swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                                    # Đổi màu tất cả các ô có thể đổi
                                    for tile in swappableTiles:
                                        self.grid.animateTransitions(tile, self.currentPlayer)
                                        self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                    self.currentPlayer *= -1
                                    self.time = pygame.time.get_ticks()

                        # Nếu game kết thúc
                        if self.gameOver:
                            x, y = pygame.mouse.get_pos()
                            if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                                self.grid.newGame()
                                self.gameOver = False
                        
                        # Nếu người chơi không còn nước đi
                        if self.passGame:                        
                            x, y = pygame.mouse.get_pos()
                            if x >= 775 and x <= 855 and y >= 300 and y <= 340:
                                self.passGame = False

    def update(self):
        '''Cập nhật trạng thái game.'''

        if self.sideSelected:
            new_time = pygame.time.get_ticks()
            if new_time - self.time >= 100:
                if self.currentPlayer != self.playerSide:
                    if not self.passGame:
                        # Nếu đối thủ không còn nước đi
                        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                            # Nếu người chơi cũng không còn nước đi, kết thúc game
                            if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer * (-1)):
                                self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
                                self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)
                                self.gameOver = True
                                return
                            # Ngược lại, chuyển lượt cho người chơi
                            else:
                                self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
                                self.grid.player2Score = self.grid.calculatePlayerScore(self.player2) 
                                self.currentPlayer *= -1
                                return
                        # Nước đi tiếp theo của đối thủ
                        if self.heuristic == self.computerPlayer.EverythingRate:
                            cell, score = self.computerPlayer.EverythingRate(1, 1, 1, 1, self.grid.gridLogic, self.depth, -1000000000, 1000000000, self.currentPlayer)
                        else:
                            cell, score = self.heuristic(self.grid.gridLogic, self.depth, -1000000000, 1000000000, self.currentPlayer)
                        self.lastMove = cell

                        # Đặt token cho nước đi cuối và đổi màu các ô
                        self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                        swappableTiles = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)
                        for tile in swappableTiles:
                            self.grid.animateTransitions(tile, self.currentPlayer)
                            self.grid.gridLogic[tile[0]][tile[1]] *= -1

                        self.currentPlayer *= -1

        # Tính lại điểm số của 2 người chơi
        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)

        # Nếu người chơi không còn nước đi
        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            # Nếu đối thủ cũng không còn nước đi
            if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer * (-1)):
                self.gameOver = True
                return
            # Ngược lại, chuyển lượt cho đối thủ
            else:
                self.currentPlayer *= -1
                self.passGame = True
        
    def draw(self):
        '''Vẽ màn hình game.'''
        bg_color = self.color.pinkBg
        self.screen.fill(bg_color)
        self.grid.drawGrid(self.screen)
        pygame.display.update()