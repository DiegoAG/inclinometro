import pygame, sys, math, serial, threading
from pygame.locals import *

pygame.init()
SCR_WIDTH = 640
SCR_HEIGHT = 480
COLOR1 = (255, 255, 255)
COLOR2 = (0, 0, 0)
COLOR3 = (255, 0, 0)
DISPLAYSURF = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
DISPLAYSURF.fill(COLOR2)
pygame.display.set_caption('Inclinometro Digital!')

def draw_box(x_origin,y_origin,width,height):
  pygame.draw.polygon(
      DISPLAYSURF,
      COLOR1,
        [
          (x_origin-(width/2), y_origin-(height/2)),
          (x_origin+(width/2), y_origin-(height/2)),
          (x_origin+(width/2), y_origin+(height/2)),
          (x_origin-(width/2), y_origin+(height/2)),
          (x_origin-(width/2), y_origin-(height/2))
        ],
      1
    )
  pygame.draw.line(
      DISPLAYSURF,
      COLOR1,
      (x_origin-(width/2), y_origin-(height/2)),
      (x_origin+(width/2),y_origin+(height/2)),
      1
    )
  pygame.draw.line(
      DISPLAYSURF,
      COLOR1,
      (x_origin+(width/2), y_origin-(height/2)),
      (x_origin-(width/2), y_origin+(height/2)),1
    )
  pygame.draw.line(
      DISPLAYSURF,
      COLOR1,
      (x_origin, y_origin-(height/2)),
      (x_origin, y_origin+(height/2)),
      1
    )
  pygame.draw.line(
      DISPLAYSURF,
      COLOR1,
      (x_origin-(height/2),y_origin),
      (x_origin+(height/2),y_origin),
      1
    )

def draw_angle(angle,x_origin,y_origin,lenght):
  x_len = lenght*math.cos(angle*0.01745)
  y_len = lenght*math.sin(angle*0.01745)
  pygame.draw.line(
      DISPLAYSURF,
      COLOR3, 
      (x_origin-x_len,y_origin-y_len), 
      (x_origin+x_len,y_origin+y_len),
      3
      )

global_angle = 0.0
angle_yz = 0.0
angle_xz = 0.0
angle_xy = 0.0
last_received = ''

def store_angle(string):
  global angle_yz, angle_xz, angle_xy
  line = string.split(':')
  if len(line) > 1 :
    if line[0] == "yz":
      angle_yz = float(line[1])
    if line[0] == "xz":
      angle_xz = float(line[1])
    if line[0] == "xy":
      angle_xy = float(line[1])

    print string


def receiving(ser):
  global last_received
  buffer = ''
 
  while True:
    buffer += ser.read(ser.inWaiting())
    if '\n' in buffer:
      lines = buffer.split('\n')
      first = lines[0]
      buffer = "\n".join(lines[1:])
      store_angle(first.strip())
 
  ser.close()
  print "Ending main thread"


ser = serial.Serial(
  '/dev/ttyUSB0',
  baudrate=9600,
  interCharTimeout=None
)
t = threading.Thread(target=receiving,args=(ser,)).start()

while True: # main game loop
  for event in pygame.event.get():
    if event.type == QUIT:
      ser.close()
      pygame.quit()
      sys.exit()

  # Clear screen
  DISPLAYSURF.fill(COLOR2)

  draw_box(SCR_WIDTH/4,SCR_HEIGHT/2,200,200)
  draw_angle(angle_yz,SCR_WIDTH/4,SCR_HEIGHT/2,100)

  draw_box(2*(SCR_WIDTH/4),SCR_HEIGHT/2,200,200)
  draw_angle(angle_xz,2*(SCR_WIDTH/4),SCR_HEIGHT/2,100)

  draw_box(3*SCR_WIDTH/4,SCR_HEIGHT/2,200,200)
  draw_angle(angle_xy,3*SCR_WIDTH/4,SCR_HEIGHT/2,100)

  pygame.display.update()
