import pygame
from pygame.locals import *

my_name = "Kale"
my_color = Color("Yellow")

your_name = "Alex"
your_color = Color("Green")

eater_color = Color("Purple")
button_color = Color("Red")

import arguments
controller = arguments.option("control", default="keyboard")
