import queue
import threading
from tkinter import *

import asyncio
import asyncvnc.asyncvnc as asyncvnc
from PIL import Image, ImageTk
import sys

DEBUG=False

def debug(*args):
    if DEBUG==True:
        print(*args)


global app
global scroll_count
scroll_count=0

mutex=threading.Condition()

#	Function that is used to get the coordonates of an event.
#	Used to determine where the user has pressed a mouse button

def get_coordinates(x,y):

	if(app.remote_x==0 or app.remote_y==0): # connection not established
		return -1, -1

	# Getting the min and max coordonates of a window
	min_x = (app.winfo_width() - app.img.width())/2
	max_x = min_x + app.img.width()
	min_y = (app.winfo_height() - app.img.height())/2
	max_y = min_y + app.img.height()


	if(x <= max_x and x >= min_x and y <= max_y and y >= min_y):
		x = (x - min_x) * app.remote_x/(max_x - min_x)
		y=(y - min_y) * app.remote_y/(max_y - min_y)
		return x, y

	return -1, -1

#	We will use a queue to store the event that the user did, and that,
#	will be runned in the application.

#The user has pressed leftclick on their mouse
def leftclick(event):
	print("left")

	x, y = get_coordinates(event.x, event.y)

	if(x == -1 or y == -1):
		return

	print(x, y)
	input_queue.put(lambda: send_left_click(x, y))

#The user has pressed middleclick on their mouse
def middleclick(event):
	print("middle")

	x, y = get_coordinates(event.x, event.y)

	if(x == -1 or y == -1):
		return

	debug(x, y)
	input_queue.put(lambda: send_middle_click(x, y))

#The user has pressed rightclick on their mouse
def rightclick(event):
	print("right")

	x, y = get_coordinates(event.x, event.y)

	if(x == -1 or y == -1):
		return

	debug(x, y)
	input_queue.put(lambda: send_right_click(x, y))

def key_pressed(event):
	if event.char.isprintable() == True and event.char != '':
		input_queue.put(lambda: send_key(event.char))

def enter_pressed(event):
	input_queue.put(lambda: send_key('Return'))

def space_pressed(event):
	input_queue.put(lambda: send_key('space'))

def back_pressed(event):
	input_queue.put(lambda: send_key('BackSpace'))

def delete_pressed(event):
	input_queue.put(lambda: send_key('Delete'))

def escape_pressed(event):
	input_queue.put(lambda: send_key('Escape'))

def win_pressed(event):
	input_queue.put(lambda: send_key('Super_L'))

def ctrl_pressed(event):
	input_queue.put(lambda: send_key('Control_L'))

def scroll_wheel(event):
	global scroll_count
    # Respond to Linux or Windows wheel event

	if event.num == 5 or event.delta == -120:
		mutex.acquire()
		scroll_count -= 1
		mutex.release()

	elif event.num == 4 or event.delta == 120:
		mutex.acquire()
		scroll_count += 1
		mutex.release()

	debug('detected scroll')

class ClientViewer(Tk):
	def __init__(self):
		super().__init__()
		self.title("Connected to: " + sys.argv[1])
		#the base size of the window
		self.geometry('800x600')

		if sys.platform in ['win32', 'win64']:
			self.state('zoomed') 
		else:
			self.attributes('-zoomed', True)

		#Create a canvas and bind all the previously implemented actions to it
		self.canvas = Canvas(self, width=1920, height=1080) # bigger canvas than the window... needed for some reason...?

		#The actions
		self.canvas.bind("<Button-1>", leftclick)
		self.canvas.bind("<Button-2>", middleclick)
		self.canvas.bind("<Button-3>", rightclick)
		self.canvas.bind("<MouseWheel>", scroll_wheel)
		self.bind("<Key>", key_pressed)
		self.bind("<space>", space_pressed)
		self.bind("<Return>", enter_pressed)
		self.bind("<BackSpace>", back_pressed)
		self.bind("<Delete>", delete_pressed)
		self.bind("<Escape>", escape_pressed)
		self.bind("<Super_L>", win_pressed)
		self.bind("<Control_L>", ctrl_pressed)
		self.bind("<Control_R>", ctrl_pressed)
		self.canvas.pack(fill = BOTH)

		self.img=PhotoImage(file = 'simplevnc.png')
		self.imgArea = self.canvas.create_image(0, 0, anchor = CENTER, image = self.img)
		gui_queue.put(lambda: show_logo())

		self.remote_x = 0
		self.remote_y = 0

#Show the SimpleVNC logo at the until the connection is established
#and until the screenshot is updated
def show_logo():
	new_x = (app.winfo_width() - app.img.width())/2
	new_y = (app.winfo_height() - app.img.height())/2
	app.canvas.moveto(app.imgArea, x = new_x, y = new_y)

def update_screenshot(screenshot: Image):
	app.remote_x = screenshot.width
	app.remote_y = screenshot.height

	aspect_ratio = screenshot.width/screenshot.height
	canvas_aspect_ratio = app.winfo_width()/app.winfo_height()	

	if aspect_ratio > canvas_aspect_ratio:
		new_size = (app.winfo_width(), int(app.winfo_width()/aspect_ratio))
	else:
		new_size = (int(app.winfo_height()*aspect_ratio), app.winfo_height())

	# We use the already defined Lanczos algorithm, in order to resize the screenshot
	# if the user wants to
	image = screenshot.resize(new_size, Image.Resampling.LANCZOS)
	
	app.img = ImageTk.PhotoImage(image)
	app.canvas.itemconfig(app.imgArea, image = app.img)

	new_x = int((app.winfo_width() - image.width)/2)
	new_y = int((app.winfo_height() - image.height)/2)
	app.canvas.moveto(app.imgArea, x = new_x, y = new_y)

	try:
		app.update()
		debug('updating... pasemite')
	except:
		pass

async def read_updates(client: asyncvnc.Client):
	while True:
		await client.read()

#Fucntion that runs the client util it is stopped
async def run_client():

	async with asyncvnc.connect(sys.argv[1], int(sys.argv[2]), None, sys.argv[3]) as client:
		global global_client
		global scroll_count

		global_client=client
		scroll_count=0

		while True:
			client.video.refresh()

			# Handle packets for a few seconds
			try:
				await asyncio.wait_for(read_updates(client), 3)
			except asyncio.TimeoutError:
				pass

			# Retrieve pixels as a 3D numpy array
			pixels = client.video.as_rgba()

			# Save as ImageTk using PIL/pillow
			screenshot = Image.fromarray(pixels)
			debug('new screenshot')
			gui_queue.put(lambda: update_screenshot(screenshot))

			mutex.acquire()

			if scroll_count!=0:
				if scroll_count<0: client.mouse.scroll_down(-scroll_count)
				else: client.mouse.scroll_up(scroll_count)
				scroll_count=0
				debug('scrolled')

			mutex.release()

			# Get input from tkinter to send to the server
			try:
				fn = input_queue.get_nowait()
			except queue.Empty:
				continue
			await fn()

#function that sends the left click
async def send_left_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.click()
	debug('sending click')

#function that sends the right click
async def send_right_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.middle_click()

#function that sends the middle click
async def send_middle_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.right_click()

#function that send scrolling updates
async def update_scroll(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.right_click()

#function that send a key
async def send_key(ch):
	global_client.keyboard.press(ch)


def gui_refresh():
	while True:

		try:
			fn = gui_queue.get_nowait()
		except queue.Empty:
			break

		fn()

	app.after(2, gui_refresh)

def start_loop():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.create_task(run_client())
	loop.run_forever()

thread=threading.Thread(target = start_loop, daemon = True)

thread.start()

gui_queue = queue.Queue()

input_queue = queue.Queue()

app = ClientViewer()

app.after(10, gui_refresh)

app.mainloop()