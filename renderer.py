import os, sys, pygame
import numpy as np
from pygame.locals import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cellular_automata.PgUtils import *

class App:
    def __init__(self):
        self._running = False
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.box = None
        self.slider = None
        self.held_down = False
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((255, 255, 255))
        # Create UI elements after pygame is initialized
        self.box = Box(0, 0, self.width, self.height)
        self.slider = Slider(self.width - 100, self.height//4, 50, 200, "slider", (150, 150, 150), "blah")
        self._running = True
        
    def on_event(self, event):
        if event.type == QUIT:
            print(event)
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos in self.slider:
                    self.held_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.held_down = False
            
        if self.held_down:
            self.slider.set_ratio(event.pos)
            ratio = self.slider.get_ratio()
            if ratio:
                self.slider.text = f"{ratio:.2f}"
    
    def on_loop(self):
        num_pixels = 80
        points = np.array([[i, j] for j in range(num_pixels) for i in range(num_pixels)])
        points -= np.array([num_pixels//2, num_pixels//2])
        offset = np.array([200, 100])
        radians = (360 * self.slider.ratio) / 180 * np.pi
        rotation_matrix = np.array([
            [np.cos(radians), np.sin(radians)],
            [-np.sin(radians), np.cos(radians)]
        ])
        new_points = points @ rotation_matrix
        new_points = new_points.astype(int)
        color = [150, 0, 0]
        for i in range(len(points)):
            if points[i] in self.box:
                color = [color[0], (i % num_pixels)*3, (i//num_pixels)*3]
                self._display_surf.set_at(new_points[i] + offset, color)
    
    def on_render(self):
        self.slider.draw(self._display_surf)
        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
        
    def on_execute(self):
        self.on_init()
        
        while self._running:
            self._display_surf.fill((255, 255, 255))
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        
    
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
