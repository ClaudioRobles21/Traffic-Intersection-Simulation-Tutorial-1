import random
import time
import threading
import pygame
import sys
from typing import Tuple

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, signal_coordinates: Tuple[int, int], timer_coordinates: Tuple[int, int], red: int=default_red, yellow:int=default_yellow, green:int=default_green):
        self.signal_coordinats = signal_coordinates
        self.timer_coordinates = timer_coordinates
        self.red = red
        self.yellow = yellow
        self.green = green
        self.timer_text = ""

# Default values of signal timers
default_red = 150
default_yellow = 5
default_green = 15

signals = []
noOfSignals = 4

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

# Initialization of signals with default values
def create_signals():
    ts1 = TrafficSignal(signal_coordinates=signalCoods[0], timer_coordinates=signalTimerCoods[0], red=0)
    ts2 = TrafficSignal(signal_coordinates=signalCoods[1], timer_coordinates=signalTimerCoods[1], red=ts1.yellow+ts1.green)
    ts3 = TrafficSignal(signal_coordinates=signalCoods[2], timer_coordinates=signalTimerCoods[2])
    ts4 = TrafficSignal(signal_coordinates=signalCoods[3], timer_coordinates=signalTimerCoods[3])
    signals.extend([ts1, ts2, ts3, ts4])


def run_simulation(current_green=0, next_green=1, current_yellow=0):
    # global current_green, current_yellow, next_green
    while(signals[current_green].green>0):   # while the timer of current green signal is not zero
        countdown_one_second()
    current_yellow = 1   # set yellow signal on
   
    while(signals[current_green].yellow>0):  # while the timer of current yellow signal is not zero
        countdown_one_second()
    current_yellow = 0   # set yellow signal off
    
     # reset all signal times of current signal to default times
    signals[current_green].green, signals[current_green].yellow, signals[current_green].red = default_green, default_yellow, default_red
       
    current_green = next_green # set next signal as green signal
    next_green = (current_green+1)%noOfSignals    # set next green signal
    signals[next_green].red = signals[current_green].yellow+signals[current_green].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    run_simulation(current_green=current_green, next_green=next_green, current_yellow=current_yellow)  

# Update values of the signal timers after every second
def countdown_one_second():
    for i in range(0, noOfSignals):
        if(i==current_green):
            if(current_yellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1
    time.sleep(1)


def main():
    current_green = 0   # Indicates which signal is green currently
    next_green = (current_green+1)%noOfSignals    # Indicates which signal will turn green next
    current_yellow = 0   # Indicates whether yellow signal is on or off 
    create_signals()
    
    thread1 = threading.Thread(name="run_simulation",target=run_simulation, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Font
    font = pygame.font.Font(None, 30)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation

        for i in range(0, noOfSignals):  # display signal and set timer according to current status: green, yellow, or red
            if(i==current_green):
                if(current_yellow==1):
                    signals[i].timer_text = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].timer_text = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red<=10):
                    signals[i].timer_text = signals[i].red
                else:
                    signals[i].timer_text = "---"
                screen.blit(redSignal, signalCoods[i])
            
            # display signal timer
            timer_text = font.render(str(signals[i].timer_text), True, white, black)
            screen.blit(timer_text, signalTimerCoods[i])

        pygame.display.update()

if __name__ == '__main__':
    main()