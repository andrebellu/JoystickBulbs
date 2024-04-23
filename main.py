import pygame
import miio as m
import os
from dotenv import load_dotenv


def send_command(command, value):
    try:
        bulb_A.send(command, [value])
        bulb_B.send(command, [value])
        print("Command sent: ", command, value)
    except Exception as e:
        print(e)


pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True

load_dotenv()
IP_A = os.getenv("IP_A")
TOKEN_A = os.getenv("TOKEN_A")
IP_B = os.getenv("IP_B")
TOKEN_B = os.getenv("TOKEN_B")

bulb_A = m.Device(ip=IP_A, token=TOKEN_A)
bulb_B = m.Device(ip=IP_B, token=TOKEN_B)
button_6_pressed = False
on = True if bulb_A.send("get_prop", ["power"])[0] == "on" else False
print("Bulb A is ", "on" if on else "off")

print("Starting infos: ")
brightness = int(bulb_A.send("get_prop", ["bright"])[0])
color = int(bulb_A.send("get_prop", ["rgb"])[0])
print("brightness: ", brightness)
print("color: ", color)

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    joystick = joysticks[-1]
    print("Detected joystick ", joystick.get_name())

while keepPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepPlaying = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Button" + str(event.button) + " pressed")
            if event.button == 6:
                button_6_pressed = True
            elif not on and event.button == 7 and button_6_pressed:
                send_command("set_power", "on")
                on = True
            elif on and event.button == 7 and button_6_pressed:
                send_command("set_power", "off")
                on = False
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 6:
                button_6_pressed = False
        elif event.type == pygame.JOYHATMOTION:
            if event.value == (0, 1) and button_6_pressed and brightness < 100:
                brightness += 10
                send_command("set_bright", brightness)
            elif event.value == (0, -1) and button_6_pressed and brightness > 0:
                brightness -= 10
                send_command("set_bright", brightness)
            elif event.value == (1, 0) and button_6_pressed:
                color += 500
                send_command("set_rgb", color)
            elif event.value == (-1, 0) and button_6_pressed:
                color -= 500
                send_command("set_rgb", color)

    clock.tick(20)
