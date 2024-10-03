import pygame, time, json
from render import *
from constants import *
from world import *
from util import *

scale = 2

class Game:
    def __init__(self, window):
        pygame.init()
        self.window = window
        self.screen = window.getScreen()
        self.running = True
        self.worldTiles = TileAtlas(12, 12, "cp437_12x12.png")
        self.textTiles = TileAtlas(8, 12, "cp437_8x12_terminal.png")

        self.debug = False
        self.mousepos = pygame.mouse.get_pos()

        self.renderspersecond = 0
        self.lastsecond = time.time()
        self.fps_counter_surface = self.getSurfaceFromString("FPS: UNCALCULATED", LGREEN, 1)

        self.lastupdatetick = time.time()

        self.chunk = Chunk()
        self.chunk.generate()

        self.camerax = 0
        self.cameray = 0
        self.cameraz = 60
        self.cameraMoveMode = False

        self.counter = 0

        self.ticking = True
        paused = self.getSurfaceFromString(" PAUSED", LRED, 1)
        self.pausedUISurface = pygame.surface.Surface((HALF_TILESIZE+TEXT_WIDTH*7, TEXT_HEIGHT))
        self.pausedUISurface.blit(self.worldTiles.getTileSurfaceXY(10, 11, LRED), (0, 0))
        self.pausedUISurface.blit(paused, (HALF_TILESIZE, 0))

        with open("game\\illogistical.json") as fp:
            rules = json.load(fp)

        self.tilenames = loadNames(rules["tiles"], "tilename")
        self.floornames = loadNames(rules["floors"], "tilename")
        self.itemnames = loadNames(rules["items"], "itemname")

        self.tileRenderCodes = list(range(len(rules["tiles"])))
        for id, tile in enumerate(rules["tiles"]):
            self.tileRenderCodes[id] = loadRenderCodeFromJSONStructure(tile)

        self.floorRenderCodes = list(range(len(rules["floors"])))
        for id, floor in enumerate(rules["floors"]):
            self.floorRenderCodes[id] = loadRenderCodeFromJSONStructure(floor)

        self.itemRenderCodes = list(range(len(rules["items"])))
        for id, item in enumerate(rules["items"]):
            self.itemRenderCodes[id] = loadRenderCodeFromJSONStructure(item)

        self.window.show()
        self.run()

    def run(self):
        while self.running:
            self.checkForEvents()
            self.screen.fill("BLACK")

            if self.lastupdatetick + TICK_SPEED < time.time():
                self.update()
                self.lastupdatetick += TICK_SPEED
            self.render()

            self.renderspersecond += 1
            if self.lastsecond + 1 < time.time():
                self.lastsecond += 1
                pygame.display.set_caption("ASCII Factory | FPS: " + str(self.renderspersecond))
                self.fps_counter_surface = self.getSurfaceFromString("FPS: " + str(self.renderspersecond), LGREEN, 1)
                self.renderspersecond = 0

    def update(self):
        pass

    def render(self):
        for y in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                self.renderTile(self.chunk.getTile(x, y, self.cameraz), x, y)

        if self.debug:
            for a in range(16):
                self.renderSurface(self.worldTiles.getTileSurfaceID(219, WHITE), SCREEN_PIXEL_WIDTH-192+HALF_TILESIZE*a, SCREEN_PIXEL_HEIGHT-192)
                self.renderSurface(self.worldTiles.getTileSurfaceXY(a, 0, BLACK), SCREEN_PIXEL_WIDTH-192+HALF_TILESIZE*a, SCREEN_PIXEL_HEIGHT-192)
                for b in range(1, 16):
                    self.screen.blit(self.worldTiles.getTileSurfaceXY(a, b, b), (SCREEN_PIXEL_WIDTH-192+HALF_TILESIZE*a, SCREEN_PIXEL_HEIGHT-192+HALF_TILESIZE*b))
        
        self.renderSurface(self.fps_counter_surface, SCREEN_PIXEL_WIDTH-self.fps_counter_surface.get_width(), 0)
        self.renderString("z-level: " + str(self.cameraz), 0, 0, LGREEN, 1)
        if not self.ticking:
            self.renderSurface(self.pausedUISurface, SCREEN_PIXEL_WIDTH-self.pausedUISurface.get_width(), TEXT_HEIGHT)

        self.renderString(f"x: {int(self.mousepos[0]/TILESIZE)} y: {int(self.mousepos[1]/TILESIZE)-2}", SCREEN_PIXEL_WIDTH-TILESIZE*14, 0, WHITE, 1)
        currentTile = self.chunk.getTile(int(self.mousepos[0]/TILESIZE), int(self.mousepos[1]/TILESIZE)-2, self.cameraz)
        if type(currentTile) == Tile:
            self.renderString("Tile: " + self.tilenames[currentTile.tile_id], SCREEN_PIXEL_WIDTH-TILESIZE*14, TEXT_HEIGHT, WHITE, 1)
            self.renderString("Floor: " + self.floornames[currentTile.floor_id], SCREEN_PIXEL_WIDTH-TILESIZE*14, TEXT_HEIGHT*2, WHITE, 1)

        pygame.display.flip()

    def checkSurroundingTilesForEnvironmental(self, x, y, z):
        if x > 0:
            if y > 0 and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x-1, y-1, z).tile_id][0]):
                return True
            if not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x-1, y, z).tile_id][0]):
                return True
            if y+1 < CHUNK_SIZE and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x-1, y+1, z).tile_id][0]):
                return True
        if y > 0 and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x, y-1, z).tile_id][0]):
            return True
        if y+1 < CHUNK_SIZE and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x, y+1, z).tile_id][0]):
            return True
        if x+1 < CHUNK_SIZE:
            if y > 0 and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x+1, y-1, z).tile_id][0]):
                return True
            if not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x+1, y, z).tile_id][0]):
                return True
            if y+1 < CHUNK_SIZE and not isRenderFlagInCode(ENVIRONMENTAL, self.tileRenderCodes[self.chunk.getTile(x+1, y+1, z).tile_id][0]):
                return True
        return False

    def renderSurface(self, surface, x, y):
        self.screen.blit(surface, (x, y))

    def renderString(self, string, x, y, color, scale):
        self.screen.blit(self.getSurfaceFromString(string, color, scale), (x, y))

    def getSurfaceFromString(self, string, color, scale):
        out = pygame.surface.Surface((len(string)*8*scale, 12*scale))
        for offset, letter in enumerate(string):
            if letter not in CHAR_CODES.keys():
                out.blit(pygame.transform.scale_by(self.textTiles.getTileSurfaceID(255, color), scale), (offset*scale*8, 0))
            else:
                out.blit(pygame.transform.scale_by(self.textTiles.getTileSurfaceID(CHAR_CODES[letter], color), scale), (offset*scale*8, 0))
        return out

    def checkForEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F3:
                    self.debug = not self.debug
                elif event.key == pygame.K_SPACE:
                    self.ticking = not self.ticking
            if event.type == pygame.MOUSEWHEEL:
                self.cameraz += event.y
                if self.cameraz < 0:
                    self.cameraz = 0
                elif self.cameraz >= WORLD_HEIGHT:
                    self.cameraz = WORLD_HEIGHT-1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    self.cameraMoveMode = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    self.cameraMoveMode = False
        self.mousepos = pygame.mouse.get_pos()

    def renderTile(self, tile, x, y):
        if tile.tile_id == NO_RENDER:
            render_code = self.floorRenderCodes[tile.floor_id]
        else:
            render_code = self.tileRenderCodes[tile.tile_id]
        if type(render_code) != list:
            error = self.getSurfaceFromString(f"TILE RENDER CODE ERROR: X: {x} Y: {y}", LRED, 1)
            self.renderSurface(error, SCREEN_PIXEL_WIDTH-error.get_width(), SCREEN_PIXEL_HEIGHT-TEXT_HEIGHT)
        elif render_code[0] == NO_FLAGS:
            self.renderTileFromCode(render_code[0], render_code[1], x,y)
            return
        if isRenderFlagInCode(ENVIRONMENTAL, render_code[0]) and not self.checkSurroundingTilesForEnvironmental(x, y, self.cameraz):
            return
        if isRenderFlagInCode(TRANSPARENT, render_code[0]):
            if isRenderFlagInCode(ENVIRONMENTAL, self.floorRenderCodes[tile.floor_id][0]):
                self.renderTileFromCode(render_code[0], self.floorRenderCodes[tile.floor_id][0], x, y)
        if isRenderFlagInCode(IODIRECTIONAL, render_code[0]):
            self.renderTileFromCode(render_code[0], render_code[tile.direction+1], x, y)
        else:
            self.renderTileFromCode(render_code[0], render_code[1], x, y)

    def renderTileFromCode(self, flags, code, x, y):
        for i in code:
            tile = self.worldTiles.getTileSurfaceID(i[ASCII_CODE], i[COLOR])
            if not isRenderFlagInCode(HALFSCALED, flags):
                self.renderSurface(pygame.transform.scale_by(tile, SCALE),
                    x*TILESIZE, (y+2)*TILESIZE)
            else:
                self.renderSurface(pygame.transform.scale_by(tile, 2-i[SCALE_CODE]), 
                    (x+i[X_OFFSET])*TILESIZE, (y+2+i[Y_OFFSET])*TILESIZE)
        

if __name__ == "__main__":
    import main