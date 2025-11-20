from calendar import TUESDAY
from unittest import TestResult
import pygame
from abc import ABC, abstractmethod

class Box:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border = [(left, left + width), (top, top + height)]
    
    def __contains__(self, item):
        return self.border[0][0] < item[0] and item[0] < self.border[0][1] and self.border[1][0] < item[1] and item[1] < self.border[1][1]

class Button:
    def __init__(self, left, top, width, height, name, color, text, font = None, fontsize = 20):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.name = name
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font, fontsize)
        
        self.border = [(left, left + width), (top, top + height)]
        self.rect = self.get_rect()
        
    def __contains__(self, item):
        return self.border[0][0] < item[0] and item[0] < self.border[0][1] and self.border[1][0] < item[1] and item[1] < self.border[1][1]
    
    def get_rect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)
    
    def get_rel_position(self, coords):
        if coords in self:
            return (coords[0] - self.border[0][0], coords[1] - self.border[1][0])
        return None
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        
        txt = self.font.render(self.text, True, (0, 0, 0))
        txt_size = txt.get_size()
        surf.blit(txt, (self.left + 0.5 * (self.width - txt_size[0]), self.top + 0.5 * (self.height - txt_size[1])))
        

class Slider(Button):
    def __init__(self, left, top, width, height, name, color, text, font = None, fontsize = 20, vertical=True):
        super().__init__(left, top, width, height, name, color, text)
        self.vertical = vertical
        self.ratio = 0
    
    def get_ratio(self, coords):
        if coords in self:
            if self.vertical:
                self.ratio = 1 - (self.get_rel_position(coords)[1] / self.height)
            else:
                self.ratio = self.get_rel_position(coords)[0] / self.width
            return self.ratio
        return None
        
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700,700))
    screen.fill((255,255,255))
    pygame.display.flip()
    
    running = True
    number = 0
    b = Button(200, 200, 200, 100, "textbox", (150,150,150), f"{number}")
    slider = Slider(130, 200, 50, 100, "slider", (200, 200, 200), "", vertical=False)
    
    def render():
        screen.fill((255, 255, 255))
        b.draw(screen)
        slider.draw(screen)
        pygame.display.flip()
    
    held_down = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos in slider:
                    held_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                held_down = False
            
        if held_down:
            ratio = slider.get_ratio(event.pos)
            if ratio:
                slider.text = f"{ratio:.2f}"
        
        render()
    
    pygame.quit()
        