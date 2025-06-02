from grid import *
import copy
from heuristics import Heuristics
import time


# Định nghĩa lớp ComputerPlayer
class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject
    
    def swappableTiles(self, x, y, grid, player):
        '''Trả về danh sách các ô có thể đổi màu sau một nước đi.'''

        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            run = True
            while run:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    run = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    run = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    run = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles

    def findValidCells(self, grid, curPlayer):
        """Thực hiện kiểm tra để tìm tất cả các ô trống nằm cạnh quân của đối thủ."""

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

    def findAvailMoves(self, grid, currentPlayer):
        """Lấy danh sách các ô hợp lệ và kiểm tra từng ô để xem có thể đi được không.
        Trả về danh sách các nước đi có thể thực hiện."""

        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            # Nếu có quân có thể đổi màu và ô chưa có trong danh sách
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells

    def evaluateMobility(self, grid, player):
        positive = len(self.findAvailMoves(grid, 1))
        negative = len(self.findAvailMoves(grid, -1 ))
        if positive + negative == 0:
            return 0
        else:
            return  100 * (positive - negative) / (positive + negative)
    
    # Các hàm heuristic

    def computerMobility(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(0, 0, 1, 0, grid, depth, alpha, beta, player)       
    
    def computerCoinParity(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(0, 1, 0, 0, grid, depth, alpha, beta, player)

    def computerStability(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(0, 0, 0, 1, grid, depth, alpha, beta, player)

    def computerCornerCapture(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(1, 0, 0, 0, grid, depth, alpha, beta, player)

    def Everything(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(1, 1, 1, 1, grid, depth, alpha, beta, player)
    
        
    def E_coins(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(1, 0, 1, 1, grid, depth, alpha, beta, player)
        
    def E_corner(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(0, 1, 1, 1, grid, depth, alpha, beta, player)

    def E_mobility(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(1, 1, 0, 1, grid, depth, alpha, beta, player)
    def E_stability(self, grid, depth, alpha, beta, player):
        return self.EverythingRate(1, 1, 1, 0, grid, depth, alpha, beta, player)

    def computerStaticBoard(self, grid, depth, alpha, beta, player):
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)

        if depth == 0 or len(availMoves) == 0:
            bestMove, Score = None, Heuristics.evaluateStaticBoard(newGrid, player)
            return bestMove, Score

        if player > 0:
            bestScore = -1000000000
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player
                
                bMove, value = self.computerStaticBoard(newGrid, depth-1, alpha, beta, player*(-1))

                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)
            return bestMove, bestScore

        if player < 0:
            bestScore = 1000000000
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player
                
                bMove, value = self.computerStaticBoard(newGrid, depth-1, alpha, beta, player*(-1))

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)
            return bestMove, bestScore
        
    def normalize_score(self, score):
        """Chuyển đổi điểm từ thang [-100,100] sang [0,1]"""
        return (score + 100) / 200

    def denormalize_score(self, normalized_score):
        """Chuyển đổi điểm từ thang [0,1] sang [-100,100]"""
        return normalized_score * 200 - 100

    def EverythingRate(self, corn, coin, mob, sta, grid, depth, alpha, beta, player):
        start_time = time.time()
        time_limit = 3.0  # 3 seconds time limit
        best_move_so_far = None
        best_score_so_far = float('-inf') if player > 0 else float('inf')
        current_depth = 1

        while time.time() - start_time < time_limit:
            try:
                newGrid = copy.deepcopy(grid)
                availMoves = self.grid.findAvailMoves(newGrid, player)

                if len(availMoves) == 0:
                    return None, 0

                if player > 0:
                    bestScore = float('-inf')
                    bestMove = None

                    for move in availMoves:
                        if time.time() - start_time >= time_limit:
                            return best_move_so_far, best_score_so_far

                        x, y = move
                        swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                        newGrid[x][y] = player
                        for tile in swappableTiles:
                            newGrid[tile[0]][tile[1]] = player
                        
                        # Check if opponent has no moves
                        new_availMoves = self.grid.findAvailMoves(newGrid, player*(-1))
                        if len(new_availMoves) == 0:
                            # Calculate heuristic scores
                            corner_score = Heuristics.evaluateCorner(newGrid, player*(-1))
                            stability_score = Heuristics.evaluate_stability(newGrid, player*(-1))
                            coin_score = Heuristics.evaluateCoinParity(newGrid, player*(-1))
                            mobility_score = self.evaluateMobility(newGrid, player*(-1))

                            # Normalize scores
                            norm_corner = self.normalize_score(corner_score)
                            norm_stability = self.normalize_score(stability_score)
                            norm_coin = self.normalize_score(coin_score)
                            norm_mobility = self.normalize_score(mobility_score)

                            # Calculate current move count
                            total_moves = sum(sum(abs(x) for x in row) for row in newGrid) - 4

                            # Determine phase and weights
                            if total_moves <= 20:  # Opening
                                corner_weight = 5
                                stability_weight = 5
                                mobility_weight = 65
                                coin_weight = 25
                            elif total_moves <= 40:  # Middle
                                corner_weight = 20
                                stability_weight = 25
                                mobility_weight = 30
                                coin_weight = 25
                            else:  # End
                                corner_weight = 40
                                stability_weight = 30
                                mobility_weight = 5
                                coin_weight = 25

                            # Calculate weighted score
                            total_weight = corner_weight + stability_weight + mobility_weight + coin_weight
                            weighted_score = (corner_weight * norm_corner + 
                                            stability_weight * norm_stability + 
                                            mobility_weight * norm_mobility + 
                                            coin_weight * norm_coin) / total_weight

                            value = self.denormalize_score(weighted_score)
                            bestMove = x, y
                            return bestMove, value

                        bMove, value = self.EverythingRate(corn, coin, mob, sta, newGrid, current_depth-1, alpha, beta, player*(-1))

                        if value > bestScore:
                            bestScore = value
                            bestMove = move
                            best_move_so_far = move
                            best_score_so_far = value
                        alpha = max(alpha, bestScore)
                        if beta <= alpha:
                            break

                        newGrid = copy.deepcopy(grid)

                else:  # player < 0
                    bestScore = float('inf')
                    bestMove = None

                    for move in availMoves:
                        if time.time() - start_time >= time_limit:
                            return best_move_so_far, best_score_so_far

                        x, y = move
                        swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                        newGrid[x][y] = player
                        for tile in swappableTiles:
                            newGrid[tile[0]][tile[1]] = player
                        
                        # Check if opponent has no moves
                        new_availMoves = self.grid.findAvailMoves(newGrid, player*(-1))
                        if len(new_availMoves) == 0:
                            # Calculate heuristic scores
                            corner_score = Heuristics.evaluateCorner(newGrid, player*(-1))
                            stability_score = Heuristics.evaluate_stability(newGrid, player*(-1))
                            coin_score = Heuristics.evaluateCoinParity(newGrid, player*(-1))
                            mobility_score = self.evaluateMobility(newGrid, player*(-1))

                            # Normalize scores
                            norm_corner = self.normalize_score(corner_score)
                            norm_stability = self.normalize_score(stability_score)
                            norm_coin = self.normalize_score(coin_score)
                            norm_mobility = self.normalize_score(mobility_score)

                            # Calculate current move count
                            total_moves = sum(sum(abs(x) for x in row) for row in newGrid) - 4

                            # Determine phase and weights
                            if total_moves <= 20:  # Opening
                                corner_weight = 5
                                stability_weight = 5
                                mobility_weight = 65
                                coin_weight = 25
                            elif total_moves <= 40:  # Middle
                                corner_weight = 20
                                stability_weight = 25
                                mobility_weight = 30
                                coin_weight = 25
                            else:  # End
                                corner_weight = 40
                                stability_weight = 30
                                mobility_weight = 5
                                coin_weight = 25

                            # Calculate weighted score
                            total_weight = corner_weight + stability_weight + mobility_weight + coin_weight
                            weighted_score = (corner_weight * norm_corner + 
                                            stability_weight * norm_stability + 
                                            mobility_weight * norm_mobility + 
                                            coin_weight * norm_coin) / total_weight

                            value = self.denormalize_score(weighted_score)
                            bestMove = x, y
                            return bestMove, value

                        bMove, value = self.EverythingRate(corn, coin, mob, sta, newGrid, current_depth-1, alpha, beta, player*(-1))

                        if value < bestScore:
                            bestScore = value
                            bestMove = move
                            best_move_so_far = move
                            best_score_so_far = value
                        beta = min(beta, bestScore)
                        if beta <= alpha:
                            break

                        newGrid = copy.deepcopy(grid)

                current_depth += 1

            except Exception as e:
                # If we encounter any issues during the search, return the best move found so far
                return best_move_so_far, best_score_so_far

        return best_move_so_far, best_score_so_far