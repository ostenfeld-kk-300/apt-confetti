#!usr/bin/env python

import random
import time
import shutil
import sys
import signal

def confetti():

	def handler(signum, frame):
		pass

	signal.signal(signal.SIGINT, handler)

	cols, rows = shutil.get_terminal_size()

	colors = [
		'\033[91m',
		'\033[92m',
		'\033[93m',
		'\033[94m',
		'\033[95m',
		'\033[96m',
	]
	reset = '\033[0m'
	shapes = ['*', '+', 'o', '.', '^', ',', 'v']

	duration = 2
	end_time = time.time() + duration

	particles = []

	sys.stdout.write("\n")

	print("\033[?1049h\033[?25l", end = "", flush = True)

	try:
		while time.time() < end_time:

			for _ in range(3):
				r_col = random.randint(1, cols)
				r_row = random.randint(1, rows)
				color = random.choice(colors)
				shape = random.choice(shapes)

				particles.append({
					'x': r_col,
					'y': r_row,
					'char': shape,
					'color': color
				})

			buffer = ""
			alive_particles = []

			for p in particles:
				buffer += f"\033[{p['y']};{p['x']}H "

				p['y'] += 1

				sway= random.choice([-1, 0, 1])
				p['x'] += sway

				p['x'] = max(1, min(p['x'], cols))

				if p['y'] < rows:
					buffer += f"\033[{p['y']};{p['x']}H{p['color']}{p['char']}"
					alive_particles.append(p)

			particles = alive_particles

			print(buffer, end = "", flush = True)

			time.sleep(0.06)

	except:
		pass

	print("\033[?1049l\033[?25h", end = "")

if __name__ == "__main__":
	confetti()



