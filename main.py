import pygame
import random


class Game:
    def __init__(self):
        # 9 is Mine
        self.gridCounts = [[0] * gridWidth for _ in range(gridHeight)]
        self.gridDisplay = [[10] * gridWidth for _ in range(gridHeight)]
        self.start = True
        self.pause = False
        self.last = []

        for h in range(gridHeight):
            for w in range(gridWidth):
                self.gridCounts[h][w] = random.choices([0, 9], [0.8, 0.2])[0]
        for h in range(gridHeight):
            for w in range(gridWidth):
                if self.gridCounts[h][w] != 9:
                    self.gridCounts[h][w] = self.countMines(h, w)
        # print(self.gridCounts)

    def open(self, h, w):
        # Pause
        if self.pause:
            return
        # Flag on square
        if self.gridDisplay[h][w] == 11:
            return
        # Here no flags and no pause
        # Start
        if self.start:
            if self.gridCounts[h][w] != 0:
                for i in self.height_iter(h):
                    for j in self.width_iter(w):
                        self.gridCounts[i][j] = 0
                for i in range(max(0, h - 2), min(gridHeight, h + 3)):
                    for j in range(max(0, w - 2), min(gridWidth, w + 3)):
                        if self.gridCounts[i][j] != 9:
                            self.gridCounts[i][j] = self.countMines(i, j)
            self.start = False
        # Bomb
        if self.gridCounts[h][w] == 9:
            self.last = [(h, w)]
            self.pause = True
        # Your Square
        if self.gridDisplay[h][w] != 10:
            flags_near = 0
            for i in self.height_iter(h):
                for j in self.width_iter(w):
                    if self.gridDisplay[i][j] == 11:
                        flags_near += 1
            if flags_near != self.gridCounts[h][w]:
                return
            right = True
            for i in self.height_iter(h):
                for j in self.width_iter(w):
                    if self.gridCounts[i][j] == 9 and self.gridDisplay[i][j] != 11:
                        right = False
            if right:
                for i in self.height_iter(h):
                    for j in self.width_iter(w):
                        if self.gridDisplay[i][j] == 10:
                            self.open(i, j)
            else:
                for i in self.height_iter(h):
                    for j in self.width_iter(w):
                        if self.gridCounts[i][j] == 9 and self.gridDisplay[i][j] == 10:
                            self.gridDisplay[i][j] = self.gridCounts[i][j]
                            self.last.append((i, j))
                self.pause = True
            return

        self.gridDisplay[h][w] = self.gridCounts[h][w]
        if self.gridCounts[h][w] == 0:
            self.rec_open(h, w)

    def make_flag(self, h, w):
        if self.gridDisplay[h][w] == 10:
            self.gridDisplay[h][w] = 11
        elif self.gridDisplay[h][w] == 11:
            self.gridDisplay[h][w] = 10

    def rec_open(self, h, w):
        for h_new in self.height_iter(h):
            for w_new in self.width_iter(w):
                if self.gridCounts[h_new][w_new] != 9 and self.gridDisplay[h_new][w_new] in (10, 11):
                    self.gridDisplay[h_new][w_new] = self.gridCounts[h_new][w_new]
                    if self.gridCounts[h_new][w_new] == 0:
                        self.rec_open(h_new, w_new)

    def openAll(self):
        self.pause = False
        for h in range(gridHeight):
            for w in range(gridWidth):
                self.gridDisplay[h][w] = self.gridCounts[h][w]

    def get_back(self):
        self.pause = False
        for h, w in self.last:
            self.gridDisplay[h][w] = 10
        self.last = []

    def draw(self, win):
        for h in range(gridHeight):
            for w in range(gridWidth):
                k = self.gridDisplay[h][w]
                win.blit(images[k], (w * gridRadius, h * gridRadius))

    def countMines(self, h, w):
        cnt = 0
        for i in self.height_iter(h):
            for j in self.width_iter(w):
                if self.gridCounts[i][j] == 9:
                    cnt += 1
        return cnt

    @staticmethod
    def height_iter(h):
        return range(max(0, h - 1), min(gridHeight, h + 2))

    @staticmethod
    def width_iter(w):
        return range(max(0, w - 1), min(gridWidth, w + 2))


pygame.init()

screenWidth = 32 * 30
screenHeight = 32 * 20
MOUSE_LEFT = 1
MOUSE_RIGHT = 3
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Minesweeper')

gridRadius = 32
gridWidth = screenWidth // gridRadius
gridHeight = screenHeight // gridRadius

image = pygame.image.load('Types.jpg')
images = [pygame.Surface((gridRadius, gridRadius)) for _ in range(12)]
for n in range(12):
    images[n].blit(image, (0, 0), pygame.Rect(n * gridRadius, 0, gridRadius, gridRadius))

game = Game()
game.draw(window)
pygame.display.update()

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            width, height = pos[0] // gridRadius, pos[1] // gridRadius
            if event.button == MOUSE_LEFT:
                game.open(height, width)
            if event.button == MOUSE_RIGHT:
                game.make_flag(height, width)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game()
            if event.key == pygame.K_SPACE:
                game.openAll()
            if event.key == pygame.K_c:
                if game.pause:
                    game.get_back()
    if pygame.key.get_pressed():
        game.draw(window)
        pygame.display.update()

pygame.quit()
