import pygame

# Định nghĩa lớp Button.
class Button:
    def __init__(self, text, x, y, fontsize=40):
        # Khởi tạo một số thuộc tính: văn bản trên nút, font của văn bản, vị trí của nút
        # và một thuộc tính boolean để kiểm tra xem nút có được nhấn hay không.

        self.font = pygame.font.SysFont('Candara', fontsize, True, False)
        self.text = self.font.render(text, 1, (111, 91, 130))
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = True
    
    def draw(self, screen):
        """Vẽ nút lên màn hình. Trả về True nếu nút được nhấn."""

        action = False
        
        # Lấy vị trí chuột
        pos = pygame.mouse.get_pos()

        # Kiểm tra xem nút có được nhấn hay không
        if self.rect.collidepoint(pos):
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            elif pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.clicked = True

        # Vẽ nút lên màn hình
        screen.blit(self.text, self.rect.topleft)

        return action