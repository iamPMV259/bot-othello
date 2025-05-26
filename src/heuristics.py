from grid import *

class Heuristics:
    # Các hàm đánh giá heuristic

    @staticmethod
    def evaluateCoinParity(grid, player):
        score = 0
        abs_grid = [list(abs(x) for x in grid[i]) for i in range(len(grid))]
        score += 100*sum(sum(x) for x in grid) / (sum(sum(x) for x in abs_grid))
        return score

    @staticmethod
    def evaluateCorner(grid, player):
        # Chiến thuật chiếm góc
        
        # Kiểm tra tất cả các góc, 100 điểm cho mỗi góc
        score_1 = 0
        score_1 += (grid[0][0] + grid[0][7] + grid[7][0] + grid[7][7])

        # độ gần góc, nếu một góc trống, tìm số ô dẫn đến việc chiếm góc đó
        # Có 3 ô xung quanh góc, vì vậy cho 100/3 điểm cho mỗi ô thuộc về đối thủ
        score_2 = 0
        if grid[0][0] == 0:
            score_2 -= (grid[0][1] + grid[1][1] + grid[1][0])
        if grid[0][7] == 0:
            score_2 -= (grid[0][6] + grid[1][6] + grid[1][7])
        if grid[7][0] == 0:
            score_2 -= (grid[6][0] + grid[6][1] + grid[7][1])
        if grid[7][7] == 0:
            score_2 -= (grid[6][6] + grid[6][7] + grid[7][6])    
            
        return 100*score_1 + 100/3*score_2

    @staticmethod
    def checkFlankNextMove(grid, position):
        '''Kiểm tra xem một quân có thể bị bao vây trong nước đi tiếp theo không.'''

        r, c = position

        # Nếu vị trí không có quân, trả về False
        if grid[r][c] == 0:
            return False
        
        player = grid[r][c]
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        # Duyệt tất cả các hướng có thể
        for (i, j) in directions:
            row, col = r, c
            
            # Tìm ô đầu tiên không chứa quân của người chơi theo hướng đó
            while 0 <= row <= 7 and 0 <= col <= 7 and grid[row][col] == player:
                row, col = row + i, col + j
            
            # Nếu có toàn quân của người chơi theo hướng đó hoặc ô đầu tiên tìm thấy trống,
            # tiếp tục với hướng tiếp theo
            if row in {-1, 8} or col in {-1, 8} or grid[row][col] == 0:
                continue

            # Ngược lại, tìm ô đầu tiên không chứa quân của người chơi theo hướng ngược lại.
            # Nếu ô đó trống, thì quân ban đầu có thể bị bao vây trong nước đi tiếp theo.
            else:
                row, col = r, c
                while 0 <= row <= 7 and 0 <= col <= 7 and grid[row][col] == player:
                    row, col = row - i, col - j
                if 0 <= row <= 7 and 0 <= col <= 7 and grid[row][col] == 0:
                    return True
        return False

    @staticmethod
    def stabilityValue(grid):
        """Trả về danh sách giá trị ổn định."""

        # 1 cho ổn định, 0 cho bán ổn định, và -1 cho không ổn định

        # Đầu tiên, chúng ta xác định các quân không ổn định.
        ans = [[0 for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                # Nếu quân có thể bị bao vây trong nước đi tiếp theo, nó không ổn định
                if Heuristics.checkFlankNextMove(grid, (i, j)):
                    ans[i][j] = -1

        # Tiếp theo, chúng ta xác định các quân ổn định.
        # Một quân được gọi là 'ổn định' trong một hướng cụ thể nếu nó không thể bị lật trong hướng đó,
        # tức là, ít nhất 1 trong 3 điều kiện sau thỏa mãn:
        # (i) Tất cả các ô trong hướng đó không trống.
        # (ii) Quân là một trong hai điểm cuối của hướng.
        # (iii) Quân nằm cạnh (theo hướng) một quân ổn định khác trong hướng đó.
        # Một quân được gọi là 'ổn định' nếu nó ổn định trong tất cả 4 hướng (ngang, dọc, chéo lên và chéo xuống)

        # Ở đây, mỗi giá trị của danh sách trả về là một bộ 4 boolean (x, y, z, t), trong đó (x, y, z, t) đại diện cho độ ổn định
        # trong 4 hướng ngang, dọc, chéo lên và chéo xuống, tương ứng.
        # Một quân ổn định nếu giá trị ổn định của nó là (True, True, True, True)

        stability = [[[0, 0, 0, 0] for j in range(8)] for i in range(8)]

        # Gán giá trị ổn định theo điều kiện (ii).

        # Tất cả các góc đều ổn định trong tất cả 4 hướng.
        for i, j in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if grid[i][j] != 0:
                stability[i][j] = [1, 1, 1, 1]
        
        # Tất cả các ô ở cạnh đều ổn định trong ít nhất 3 hướng.
        # Cạnh trên và cạnh dưới.
        for i in [0, 7]:
            for j in range(1, 7):
                if grid[i][j] != 0:
                    stability[i][j] = [0, 1, 1, 1]
        
        # Cạnh trái và cạnh phải.
        for j in [0, 7]:
            for i in range(1, 7):
                if grid[i][j] != 0:
                    stability[i][j] = [1, 0, 1, 1]
        
        horizontal = [(0, 1), (0, -1)]
        vertical = [(1, 0), (-1, 0)]
        upward_diagonal = [(1, 1), (-1, -1)]
        downward_diagonal = [(1, -1), (-1, 1)]

        # Gán giá trị ổn định theo điều kiện (i).
        for i in range(8):
            for j in range(8):
                # Nếu ô không có quân, tiếp tục. 
                if grid[i][j] == 0:
                    continue

                # Nếu ô là góc, tiếp tục.
                if (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                    continue

                # Nếu quân không ổn định trong một hướng, chúng ta kiểm tra xem hướng đó có đầy quân không.
                # Nếu có, thì cập nhật giá trị ổn định của quân.

                # Hướng ngang
                if stability[i][j][0] == 0:
                    x, y = horizontal[0]
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r + x, c + y
                    if 0 <= r <= 7 and 0 <= c <= 7:
                        continue
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r - x, c - y
                    if r in {-1, 8} or c in {-1, 8}:
                        stability[i][j][0] = 1
                
                # Hướng dọc
                if stability[i][j][1] == 0:
                    x, y = vertical[0]
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r + x, c + y
                    if 0 <= r <= 7 and 0 <= c <= 7:
                        continue
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r - x, c - y
                    if r in {-1, 8} or c in {-1, 8}:
                        stability[i][j][1] = 1
                
                # Hướng chéo lên
                if stability[i][j][2] == 0:
                    x, y = upward_diagonal[0]
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r + x, c + y
                    if 0 <= r <= 7 and 0 <= c <= 7:
                        continue
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r - x, c - y
                    if r in {-1, 8} or c in {-1, 8}:
                        stability[i][j][2] = 1

                # Hướng chéo xuống
                if stability[i][j][3] == 0:
                    x, y = downward_diagonal[0]
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r + x, c + y
                    if 0 <= r <= 7 and 0 <= c <= 7:
                        continue
                    r, c = i, j
                    while 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] != 0:
                        r, c = r - x, c - y
                    if r in {-1, 8} or c in {-1, 8}:
                        stability[i][j][3] = 1


        # Duyệt tất cả các quân và cập nhật giá trị ổn định của chúng cho đến khi không có gì thay đổi.
        change = True
        while change:
            change = False
            for i in range(8):
                for j in range(8):
                    # Nếu ô không có quân, tiếp tục. 
                    if grid[i][j] == 0:
                        continue

                    # Nếu ô là góc, tiếp tục.
                    if (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        continue

                    # Nếu quân không ổn định trong một hướng, chúng ta duyệt 2 ô lân cận trong hướng đó.
                    # Nếu ít nhất 1 ô lân cận có cùng màu và ổn định trong hướng đó, chúng ta cập nhật giá trị ổn định của quân.

                    # Hướng ngang.
                    if stability[i][j][0] == 0:
                        for x, y in horizontal:
                            r, c = i + x, j + y
                            if 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] == grid[i][j] and stability[r][c][0] == 1:
                                stability[i][j][0] = 1
                                change = True
                    
                    # Hướng dọc.
                    if stability[i][j][1] == 0:
                        for x, y in vertical:
                            r, c = i + x, j + y
                            if 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] == grid[i][j] and stability[r][c][1] == 1:
                                stability[i][j][1] = 1
                                change = True

                    # Hướng chéo lên.
                    if stability[i][j][2] == 0:
                        for x, y in upward_diagonal:
                            r, c = i + x, j + y
                            if 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] == grid[i][j] and stability[r][c][2] == 1:
                                stability[i][j][2] = 1
                                change = True

                    # Hướng chéo xuống.
                    if stability[i][j][3] == 0:
                        for x, y in downward_diagonal:
                            r, c = i + x, j + y
                            if 0 <= r <= 7 and 0 <= c <= 7 and grid[r][c] == grid[i][j] and stability[r][c][3] == 1:
                                stability[i][j][3] = 1
                                change = True

        for i in range(8):
            for j in range(8):
                # Nếu stability[i][j] là (True, True, True, True), thì quân ở (i, j) ổn định.
                if stability[i][j] == [1, 1, 1, 1]:
                    ans[i][j] = 1
        
        return ans

    @staticmethod
    def evaluate_stability(grid, player):
        a = 0
        b = 0

        stabilityVal = Heuristics.stabilityValue(grid)

        for i in range(8):
            for j in range(8):
                if grid[i][j] == -1:
                    a += stabilityVal[i][j]
                elif grid[i][j] == 1:
                    b += stabilityVal[i][j]
        
        if a + b == 0:
            return 0
        return 100*(a-b)/(a+b)

    @staticmethod
    def evaluateStaticBoard(grid, player):
        score = 0
        staticBoard = [
            [100, -20, 10, 5, 5, 10, -20, 100], 
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
        for i in range(8):
            for j in range(8):
                score += grid[i][j]*staticBoard[i][j]
        return score

    @staticmethod
    def evaluateMobility(grid, player):
        positive = len(Heuristics.findAvailMoves(grid, 1))
        negative = len(Heuristics.findAvailMoves(grid, -1))
        if positive + negative == 0:
            return 0
        else:
            return 100 * (positive - negative) / (positive + negative)

    @staticmethod
    def findAvailMoves(grid, player):
        # Phương thức này cần được triển khai hoặc import từ module khác
        # Hiện tại, trả về một danh sách rỗng làm placeholder
        return []

