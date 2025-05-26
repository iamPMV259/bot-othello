# Định nghĩa lớp Token.
class Token:
    def __init__(self, player, gridX, gridY, image, main):
        # Khởi tạo một số thuộc tính của token: màu (player), vị trí, game, hình ảnh.
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 85 + (gridY * 80)
        self.posY = 85 + (gridX * 80)
        self.GAME = main
        self.image = image

    def transition(self, transitionImages, tokenImage):
        '''Cho việc chuyển đổi token.'''

        for i in range(30):
            # Thay đổi hình ảnh của token và vẽ nó lên màn hình.
            self.image = transitionImages[i // 10]
            self.GAME.draw()

        # Hình ảnh cuối cùng của token.
        self.image = tokenImage

    def draw(self, window):
        '''Vẽ token lên màn hình.'''
        window.blit(self.image, (self.posX, self.posY))