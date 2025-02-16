import random
import time
import threading
import pygame
import sys
from typing import Tuple, List

pygame.init()
simulation = pygame.sprite.Group()

# Default values of signal timers
default_red = 150
default_yellow = 3
default_green = 10


class TrafficSignal:
	"""Class to represent a traffic signal at the intersection of the road.

	Attributes:
		signal_coordinates (Tuple[int, int]): Coordinates of the signal image
		timer_coordinates (Tuple[int, int]): Coordinates of the timer text
		red (int): Time for red signal
		yellow (int): Time for yellow signal
		green (int): Time for green signal
		timer_text (str): Text to display the timer of the signal
	"""

	def __init__(
		self,
		signal_coordinates: Tuple[int, int],
		timer_coordinates: Tuple[int, int],
		red: int = default_red,
		yellow: int = default_yellow,
		green: int = default_green,
	):
		self.signal_coordinates = signal_coordinates
		self.timer_coordinates = timer_coordinates
		self.red = red
		self.yellow = yellow
		self.green = green
		self.timer_text = ""


def create_signals():
	"""
	Create signals at the intersection of the road and set their default timer values for red, yellow, and green signals.

	Returns:
	List[TrafficSignal]: List of TrafficSignal objects
	"""
	# Coordinates of signal image, timer, and vehicle count
	signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
	signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]

	ts1 = TrafficSignal(
		signal_coordinates=signalCoods[0], timer_coordinates=signalTimerCoods[0], red=0
	)
	ts2 = TrafficSignal(
		signal_coordinates=signalCoods[1],
		timer_coordinates=signalTimerCoods[1],
		red=ts1.yellow + ts1.green,
	)
	ts3 = TrafficSignal(
		signal_coordinates=signalCoods[2], timer_coordinates=signalTimerCoods[2]
	)
	ts4 = TrafficSignal(
		signal_coordinates=signalCoods[3], timer_coordinates=signalTimerCoods[3]
	)

	signals = [ts1, ts2, ts3, ts4]
	return signals


# Simulation global variables
signals = create_signals()
no_of_signals = 4

current_green = 0  # Indicates which signal is green currently
next_green = (
	current_green + 1
) % no_of_signals  # Indicates which signal will turn green next
current_yellow = 0  # Indicates whether yellow signal is on or off


def run_simulation():
	"""Run the simulation of the traffic signals at the intersection of the road.

	If the green signal is on, countdown the green timer by one second. After countdown, check if the green timer is zero.
	If the green timer is zero, set the yellow signal on and countdown the yellow timer by one second.
	After countdown, set the yellow signal off and reset the timer of the current signal to default values.
	Set the next signal as green signal and set the red timer of the next to next signal as (yellow time + green time) of the next signal.
	Run the simulation again.
	"""
	global signals, no_of_signals, current_green, next_green, current_yellow
	while signals[current_green].green > 0:
		countdown_one_second()
	current_yellow = 1  # set yellow signal on

	while signals[current_green].yellow > 0:
		countdown_one_second()
	current_yellow = 0  # set yellow signal off

	# reset all signal times of current signal to default times
	(
		signals[current_green].green,
		signals[current_green].yellow,
		signals[current_green].red,
	) = (default_green, default_yellow, default_red)

	current_green = next_green  # set next signal as green signal
	next_green = (current_green + 1) % no_of_signals  # set next green signal
	signals[next_green].red = (
		signals[current_green].yellow + signals[current_green].green
	)  # set the red time of next to next signal as (yellow time + green time) of next signal
	run_simulation()


def countdown_one_second():
	"""Countdown the timer of the signals by one second.

	If the green signal is on, decrement the green timer by one.
	If the yellow signal is on, decrement the yellow timer by one.
	Otherwise, decrement the red timer by one.
	Sleep for one second after decrementing the timer.
	"""
	for i in range(0, no_of_signals):
		if i == current_green:
			if current_yellow == 0:
				signals[i].green -= 1
			else:
				signals[i].yellow -= 1
		else:
			signals[i].red -= 1
	time.sleep(1)


def main():
	"""Main function to run the simulation of the traffic signals at the intersection of the road."""
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
	background = pygame.image.load("images/intersection.png")

	screen = pygame.display.set_mode(screenSize)
	pygame.display.set_caption("SIMULATION")

	# Loading signal images and font
	redSignal = pygame.image.load("images/signals/red.png")
	yellowSignal = pygame.image.load("images/signals/yellow.png")
	greenSignal = pygame.image.load("images/signals/green.png")

	thread1 = threading.Thread(
		name="run_simulation",
		target=run_simulation,
		args=(),
	)  # initialization
	thread1.daemon = True
	thread1.start()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.blit(background, (0, 0))  # display background in simulation

		# display signal and set timer according to current status: green, yellow, or red
		for i in range(0, no_of_signals):
			if i == current_green:
				if current_yellow == 1:
					signals[i].timer_text = signals[i].yellow
					screen.blit(yellowSignal, signals[i].signal_coordinates)
				else:
					signals[i].timer_text = signals[i].green
					screen.blit(greenSignal, signals[i].signal_coordinates)
			else:
				if signals[i].red <= 10:
					signals[i].timer_text = signals[i].red
				else:
					signals[i].timer_text = "---"
				screen.blit(redSignal, signals[i].signal_coordinates)

			# display signal timer
			timer_text = font.render(str(signals[i].timer_text), True, white, black)
			screen.blit(timer_text, signals[i].timer_coordinates)

		pygame.display.update()


if __name__ == "__main__":
	main()
