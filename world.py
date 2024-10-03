from constants import *

class Tile:
    def __init__(self, tile_id, floor_id, direction):
        self.tile_id = tile_id
        self.floor_id = floor_id
        self.direction = direction

class Chunk:
    def __init__(self):
        self.tile_list = []
        for z in range(WORLD_HEIGHT):
            for y in range(CHUNK_SIZE):
                for x in range(CHUNK_SIZE):
                    self.tile_list.append(Tile(1, 1, 0))

    def generate(self):
        for z in range(61):
            for y in range(CHUNK_SIZE):
                for x in range(CHUNK_SIZE):
                    self.tile_list[x+CHUNK_SIZE*(y+z*CHUNK_SIZE)] = Tile(2, 2, 0)
            for y in range(0, 11):
                for x in range(7, 18):
                    self.tile_list[x+CHUNK_SIZE*(y+z*CHUNK_SIZE)] = Tile(3, 3, 0)
            for y in range(8, 16):
                for x in range(8, 16):
                    self.tile_list[x+CHUNK_SIZE*(y+z*CHUNK_SIZE)] = Tile(1, 2, 0)
            self.tile_list[12+CHUNK_SIZE*(12+z*CHUNK_SIZE)] = Tile(4, 2, 0)

    def getTile(self, x, y, z):
        if x >= 0 and x < CHUNK_SIZE and y >= 0 and y < CHUNK_SIZE and z >= 0 and z < WORLD_HEIGHT:
            return self.tile_list[x+y*CHUNK_SIZE+z*CHUNK_SIZE*CHUNK_SIZE]
        else: 
            return -1
    
    def addTile(self, tile, x, y, z):
        self.tile_list[x+CHUNK_SIZE*(y+z*CHUNK_SIZE)] = tile

if __name__ == "__main__":
    import main