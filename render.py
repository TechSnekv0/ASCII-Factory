import pygame
from util import *
from constants import *

WORLD_HEIGHT = 200
CHUNK_SIZE = 10

class Window:
    def __init__(self, tilesize):
        self.pixels_width = SCREEN_PIXEL_WIDTH
        self.pixels_height = SCREEN_PIXEL_HEIGHT
        self.hide()
        pygame.display.set_caption("ASCII Factory | FPS: [UNCALCULATED]")

    def hide(self):
        self.screen = pygame.display.set_mode((self.pixels_width, self.pixels_height), flags=pygame.HIDDEN)

    def show(self):
        self.screen = pygame.display.set_mode((self.pixels_width, self.pixels_height), flags=pygame.SHOWN)

    def getScreen(self):
        return self.screen

class TileAtlas:
    def __init__(self, basetilewidth, basetileheight, file):
        self.tilewidth = basetilewidth
        self.tileheight = basetileheight
        self.tileset = pygame.image.load(file)
        self.tileset.set_colorkey(self.tileset.get_at((0,0)))
        colors = loadFile("init\\colors.txt")
        self.TILES_BLACK = self.tileset.copy()
        self.TILES_BLACK_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_BLACK)
        self.TILES_BLACK_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "BLACK_B"), loadValueFromFile(colors, "BLACK_G"), loadValueFromFile(colors, "BLACK_R")))
        self.TILES_BLUE = self.tileset.copy()
        TILES_BLUE_PIXEL_ARRAY     = pygame.pixelarray.PixelArray(self.TILES_BLUE)
        TILES_BLUE_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "BLUE_B"), loadValueFromFile(colors, "BLUE_G"), loadValueFromFile(colors, "BLUE_R")))
        self.TILES_GREEN = self.tileset.copy()
        TILES_GREEN_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_GREEN)
        TILES_GREEN_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "GREEN_B"), loadValueFromFile(colors, "GREEN_G"), loadValueFromFile(colors, "GREEN_R")))
        self.TILES_CYAN = self.tileset.copy()
        TILES_CYAN_PIXEL_ARRAY     = pygame.pixelarray.PixelArray(self.TILES_CYAN)
        TILES_CYAN_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "CYAN_B"), loadValueFromFile(colors, "CYAN_G"), loadValueFromFile(colors, "CYAN_R")))
        self.TILES_RED = self.tileset.copy()
        TILES_RED_PIXEL_ARRAY      = pygame.pixelarray.PixelArray(self.TILES_RED)
        TILES_RED_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "RED_B"), loadValueFromFile(colors, "RED_G"), loadValueFromFile(colors, "RED_R")))
        self.TILES_MAGENTA = self.tileset.copy()
        TILES_MAGENTA_PIXEL_ARRAY  = pygame.pixelarray.PixelArray(self.TILES_MAGENTA)
        TILES_MAGENTA_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "MAGENTA_B"), loadValueFromFile(colors, "MAGENTA_G"), loadValueFromFile(colors, "MAGENTA_R")))
        self.TILES_BROWN = self.tileset.copy()
        TILES_BROWN_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_BROWN)
        TILES_BROWN_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "BROWN_B"), loadValueFromFile(colors, "BROWN_G"), loadValueFromFile(colors, "BROWN_R")))
        self.TILES_LGRAY = self.tileset.copy()
        TILES_LGRAY_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_LGRAY)
        TILES_LGRAY_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LGRAY_B"), loadValueFromFile(colors, "LGRAY_G"), loadValueFromFile(colors, "LGRAY_R")))
        self.TILES_DGRAY = self.tileset.copy()
        TILES_DGRAY_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_DGRAY)
        TILES_DGRAY_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "DGRAY_B"), loadValueFromFile(colors, "DGRAY_G"), loadValueFromFile(colors, "DGRAY_R")))
        self.TILES_LBLUE = self.tileset.copy()
        TILES_LBLUE_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_LBLUE)
        TILES_LBLUE_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LBLUE_B"), loadValueFromFile(colors, "LBLUE_G"), loadValueFromFile(colors, "LBLUE_R")))
        self.TILES_LGREEN = self.tileset.copy()
        TILES_LGREEN_PIXEL_ARRAY   = pygame.pixelarray.PixelArray(self.TILES_LGREEN)
        TILES_LGREEN_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LGREEN_B"), loadValueFromFile(colors, "LGREEN_G"), loadValueFromFile(colors, "LGREEN_R")))
        self.TILES_LCYAN = self.tileset.copy()
        TILES_LCYAN_PIXEL_ARRAY    = pygame.pixelarray.PixelArray(self.TILES_LCYAN)
        TILES_LCYAN_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LCYAN_B"), loadValueFromFile(colors, "LCYAN_G"), loadValueFromFile(colors, "LCYAN_R")))
        self.TILES_LRED = self.tileset.copy()
        TILES_LRED_PIXEL_ARRAY     = pygame.pixelarray.PixelArray(self.TILES_LRED)
        TILES_LRED_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LRED_B"), loadValueFromFile(colors, "LRED_G"), loadValueFromFile(colors, "LRED_R")))
        self.TILES_LMAGENTA = self.tileset.copy()
        TILES_LMAGENTA_PIXEL_ARRAY = pygame.pixelarray.PixelArray(self.TILES_LMAGENTA)
        TILES_LMAGENTA_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "LMAGENTA_B"), loadValueFromFile(colors, "LMAGENTA_G"), loadValueFromFile(colors, "LMAGENTA_R")))
        self.TILES_YELLOW = self.tileset.copy()
        TILES_YELLOW_PIXEL_ARRAY   = pygame.pixelarray.PixelArray(self.TILES_YELLOW)
        TILES_YELLOW_PIXEL_ARRAY.replace(pygame.color.Color(255, 255, 255), pygame.color.Color(loadValueFromFile(colors, "YELLOW_B"), loadValueFromFile(colors, "YELLOW_G"), loadValueFromFile(colors, "YELLOW_R")))
        self.TILES_WHITE = self.tileset.copy()

    def getTilesetFromColor(self, color):
        if color ==   BLACK:
            tileset = self.TILES_BLACK
        elif color == BLUE:
            tileset = self.TILES_BLUE
        elif color == GREEN:
            tileset = self.TILES_GREEN
        elif color == CYAN:
            tileset = self.TILES_CYAN
        elif color == RED:
            tileset = self.TILES_RED
        elif color == MAGENTA:
            tileset = self.TILES_MAGENTA
        elif color == BROWN:
            tileset = self.TILES_BROWN
        elif color == LGRAY:
            tileset = self.TILES_LGRAY
        elif color == DGRAY:
            tileset = self.TILES_DGRAY
        elif color == LBLUE:
            tileset = self.TILES_LBLUE
        elif color == LGREEN:
            tileset = self.TILES_LGREEN
        elif color == LCYAN:
            tileset = self.TILES_LCYAN
        elif color == LRED:
            tileset = self.TILES_LRED
        elif color == LMAGENTA:
            tileset = self.TILES_LMAGENTA
        elif color == YELLOW:
            tileset = self.TILES_YELLOW
        elif color == WHITE:
            tileset = self.TILES_WHITE
        else:
            tileset = self.tileset
        return tileset

    def getTileSurfaceXY(self, x, y, color):
        tileset = self.getTilesetFromColor(color)
        
        return tileset.subsurface(x*self.tilewidth, y*self.tileheight, self.tilewidth, self.tileheight)
    
    def getTileSurfaceID(self, ascii_code, color):
        tileset = self.getTilesetFromColor(color)
        
        return tileset.subsurface((ascii_code%16)*self.tilewidth, (ascii_code>>4)*self.tileheight, self.tilewidth, self.tileheight)

if __name__ == "__main__":
    import main