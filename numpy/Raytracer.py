import pygame
from pygame.locals import *

from rt import Raytracer

from figuras import *
from lights import *
from materials import *

width = 512
height = 512
pygame.init() 

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

pygame

raytracer = Raytracer(screen)

raytracer.envMap = pygame.image.load("fondo.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)

earthTexture = pygame.image.load("earthTextureMap.jpg")
jupiterTexture = pygame.image.load("jupiterTextureMap.jpg")
nuveTexture = pygame.image.load("nuveTextureMap.jpg")

#marbleTexture = pygame.image.load("marbleTextureMap.jpg")
brick = Material(diffuse = (1,0.4,0.4), spec = 8, ks = 0.01)
grass = Material(diffuse = (0.4,1,0.4), spec =32, ks = 0.1) 
water = Material(diffuse = (0.4,0.4,1), spec = 256, ks = 0.2 )
snow = Material(diffuse= (1,1,1), spec= 0.2, ks = 0.1)
rock = Material(diffuse=(0,0,0), spec = 3, ks = 0.1)
carot = Material(diffuse=(1,0.5,0), spec = 0.5, ks = 0.3)
eyes = Material(diffuse= (0.9,0.9,0.9), spec= 0.4, ks = 0.1)

mirror = Material(diffuse = (0.9,0.9,0.9), spec = 64, ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse = (0.4,0.4,0.9), spec = 32, ks = 0.15, matType = REFLECTIVE)
earth = Material(texture = earthTexture)
jupiter = Material(texture = jupiterTexture)
nuve = Material(texture = nuveTexture)
#marble = Material(texture = marbleTexture,spec = 64, ks = 0.1, matType=REFLECTIVE )

glass = Material(diffuse= (0.9,0.9,0.9),spec = 64, ks = 0.15, ior = 1.5, matType=TRANSPARENT)
diamond = Material(diffuse = (0.9,0.9,0.9), spec = 128, ks = 0.2, ior= 2.417, matType = TRANSPARENT)
water = Material(diffuse = (0.4,0.4,1.0), spec = 128, ks = 0.2, ior= 1.33, matType = TRANSPARENT)



raytracer.scene.append(Sphere(position=(0, 1.3, -5), radius=0.7, material=jupiter))  # Jupiter
raytracer.scene.append(Sphere(position=(1.6, 1.3, -5), radius=0.7, material=blueMirror))  # Azul reflectante
raytracer.scene.append(Sphere(position=(-1.6, 1.3, -5), radius=0.7, material=water))  # Agua


raytracer.scene.append(Sphere(position=(0, -1.3, -5), radius=0.7, material=nuve))  # nuves
raytracer.scene.append(Sphere(position=(1.6, -1.3, -5), radius=0.7, material=mirror))  # Reflejante
raytracer.scene.append(Sphere(position=(-1.6, -1.3, -5), radius=0.7, material=diamond))  # Diamante



#Luces
raytracer.lights.append(AmbientLight(intensity=0.1))  
raytracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.9))  
#raytracer.lights.append(PointLight(point=(1.5, 0, -5), intensity=1, color=(1, 0, 1)))   

raytracer.rtClear()
raytracer.rtRender()

print("\nrender time", pygame.time.get_ticks()/1000, "secs")
isRunning = True
while isRunning:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False      

pygame.quit()