import pygame


class spritesheet():
    def __init__(self, image, cols, rows):
        # try:
        # 	self.sheet = pygame.image.load(filename).convert_alpha()
        # except:
        # 	self.sheet = pygame.image.load(filename)
        self.sheet = image
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        self.rect_l = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect_l.width / cols)
        h = self.cellHeight = int(self.rect_l.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))

        self.cells = list([
            (index % cols * w, int(index / cols) * h, w, h)
            for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0),
            (-w, 0),
            (0, -hh),
            (-hw, -hh),
            (-w, -hh),
            (0, -h),
            (-hw, -h),
            (-w, -h), ])
        self.rect = self.sheet.get_rect()

    def draw(self, surface, cellIndex, x, y, handle=0):
        self.pos = (x + self.handle[handle][0], y + \
            self.handle[handle][1])
        surface.blit(
            self.sheet, (x + self.handle[handle][0],
                         y + self.handle[handle][1]), 
                         self.cells[cellIndex])
   
    # r_index,index = 0,0
    # @staticmethod
    # def index_change(FPS, reset_index):
    #     global r_index, index
    #     r_index += 1
    #     if r_index % FPS == 0:
    #         index += 1
    #         r_index = 0
    #     if index > (reset_index.cols*reset_index.rows):
    #         index = 0
        # print (reset_index.cols)
