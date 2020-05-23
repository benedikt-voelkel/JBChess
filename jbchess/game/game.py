import numpy as np
import turtle as trt

from copy import deepcopy

class PhysicalVolumeManager:
    def __init__(self):
        self.volumes = []

    def add(self, volume):
        volume.id = len(self.volumes)
        self.volumes.append(volume)

PHYSICAL_VOLUME_MANAGER = PhysicalVolumeManager()


class AreaAtt:
    def __init__(self, color="white", fill=False):
        self.boarder_color = color
        self.fill_color = color
        self.boarder_size = 0
        self.fill = fill
        self.fill_style = "AREA"

class AreaBase:
    def __init__(self, name):
        self.name = name


class Rectangle(AreaBase):
    def __init__(self, height, width):
        AreaBase.__init__(self, "Rectangle")
        AreaAtt.__init__(self, "white")
        self.height = height
        self.width = width
        self.lines = [width, height, width, height]
        self.rotations = [90, 90, 90, 90]
        self.center = [width / 2, height / 2]



    def draw(self, backend, translation):
        backend.penup()

        backend.goto(translation[0] - self.height / 2, translation[1] + self.width / 2)
        backend.fillcolor(self.color)
        backend.begin_fill()
        backend.pendown()
        sides = (self.height, self.width)
        for i in range(4):
            backend.forward(sides[i%2])
            backend.right(90)
        backend.end_fill()


    def is_inside(self, x, y):
        x_trans = x + self.height / 2
        y_trans = y + self.width / 2
        return x_trans >= 0 and x_trans < self.height and y_trans >= 0 and y_trans < self.width



class Square(Rectangle):
    def __init__(self, length):
        super().__init__(length, length)


class Symbol(Rectangle):
    def __init__(self, height, width, symbol):
        super().__init__(height, width)
        self.symbol = symbol
        self.name = "Symbol"



 
class PhysicalArea:
    def __init__(self, volume, parent=None):
        self.id = None
        self.volume = volume
        self.translation = np.zeros((2,), dtype=float)
        self.children = []
        self.parent = parent

        if parent:
            parent.add_child(self)

        PHYSICAL_VOLUME_MANAGER.add(self)

    def add_child(self, child_volume):
        self.children.append(child_volume)


    def draw(self, backend):
        self.volume.draw(backend, self.translation)


    def get_children(self):
        return self.children


    def is_inside(self, x, y):
        return self.volume.is_inside(self.translation[0] - x, self.translation[1] - y)


class Game:
    def __init__(self, game_front_end, game_backend):
        self.game_front_end = game_front_end
        self.game_backend = game_backend
        self.draw_backend = trt.Turtle()
        trt.speed(1000)
        trt.tracer(False)


    def click(self, x, y):
        self.game_front_end.find_volume(x, y, self.game_front_end.current_volume)
        if not self.game_front_end.current_volume:
            self.game_front_end.find_volume(x, y)
        if not self.game_front_end.current_volume:
            self.game_front_end.unmark_volumes()
            return
        
        if self.game_front_end.current_volume is not self.game_front_end.previous_volume:
            self.game_front_end.unmark_volumes()
            self.game_front_end.mark_volumes()

        current_id = self.game_front_end.current_volume.id


    def start(self):
        self.game_front_end.draw_backend = self.draw_backend
        self.game_front_end.draw_world()
        trt.onscreenclick(self.click)
        trt.mainloop()



class Frontend:

    def __init__(self):
        self.world = None
        self.interface = None
        self.last_marked = []
        self.draw_backend = None


        self.current_search_tree = None
        self.current_offset = None
        self.current_volume = None
        self.previous_volume = None

    def draw_volume(self, phys_vol):
        print("DRAW")

        self.draw_backend.penup()
        vol = phys_vol.volume
        translation = phys_vol.translation
        self.draw_backend.goto(translation[0] - vol.center[0], translation[1] + vol.center[1])

        if vol.fill:
            self.draw_backend.begin_fill()
            self.draw_backend.fillcolor(vol.fill_color)
        if vol.boarder_size > 0:
            self.draw_backend.pendown()
            self.draw_backend.width(vol.boarder_size)
        for l, r in zip(vol.lines, vol.rotations):
            self.draw_backend.forward(l)
            self.draw_backend.right(r)

        self.draw_backend.end_fill()
        self.draw_backend.penup()
        self.draw_backend.home()
        for pv in phys_vol.get_children():
            self.draw_volume(pv)


    def update_volume(self, next_volume):
        if self.current_volume:
            self.previous_volume = self.current_volume
        self.current_volume = next_volume

    def find_volume_(self, x, y, start, volumes_found):
        if start.is_inside(x, y):
            volumes_found.append(start)
            for v in start.get_children():
                self.find_volume_(x, y, v, volumes_found)



    def find_volume(self, x, y, start=None, offset=0):

        if not self.world.is_inside(x, y):
            print(f"(x, y) = ({x}, {y}) not in world volume")
            self.update_volume(None)
            return

        if start and not start.is_inside(x, y):
            print(f"(x, y) = ({x}, {y}) not in volume")
            self.update_volume(None)
            return


        volumes_found = []

        if not start:
            start = self.world

        self.find_volume_(x, y, start, volumes_found)
        if offset >= len(volumes_found):
            print(f"No volume with offset {offset} from deepest found. Maximum offset is {len(volumes_found) - 1}")
            return volumes_found[0]

        self.current_search_tree = volumes_found
        self.current_offset = offset
        self.update_volume(volumes_found[-1 - offset])


    def draw_world(self):
        self.draw_volume(self.world)


    def unmark_volumes(self):
        for v in self.last_marked:
            self.draw_volume(v)
        self.last_marked = []

    def mark_volume_(self, volume):
        print(f"Marked: {volume.id}")

        color_tmp = volume.volume.fill_color
        volume.volume.fill_color = "green"
        volume.volume.fill = True
        self.draw_volume(volume)
        volume.volume.fill_color = color_tmp
        self.last_marked.append(volume)


    def mark_volumes(self, *volumes):
        if not volumes and self.current_volume:
            # Mark only current one
            self.mark_volume_(self.current_volume)
            return
        for v in volumes:
            self.mark_volume_(v)





