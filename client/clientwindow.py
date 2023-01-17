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

def get_coordinates(x,y):
	if(app.remote_x==0 or app.remote_y==0): # connection not established
		return -1, -1
	min_x=(app.winfo_width()-app.img.width())/2
	max_x=min_x+app.img.width()
	min_y=(app.winfo_height()-app.img.height())/2
	max_y=min_y+app.img.height()
	#print('(',min_x,max_x,')','(',min_y,max_y,sep=',')
	if(x<=max_x and x>=min_x and y<=max_y and y>=min_y):
		x=(x-min_x)*app.remote_x/(max_x-min_x)
		y=(y-min_y)*app.remote_y/(max_y-min_y)
		return x, y
	return -1, -1

def leftclick(event):
	print("left")
	x, y=get_coordinates(event.x, event.y)
	if(x==-1 or y==-1):
		return
	print(x, y)
	input_queue.put(lambda: send_click(x, y))


def middleclick(event):
	print("middle")
	x, y=get_coordinates(event.x, event.y)
	if(x==-1 or y==-1):
		return
	debug(x, y)
	input_queue.put(lambda: send_middle_click(x, y))

def rightclick(event):
	print("right")
	x, y=get_coordinates(event.x, event.y)
	if(x==-1 or y==-1):
		return
	debug(x, y)
	input_queue.put(lambda: send_right_click(x, y))

class ImageViewer(Tk):
	def __init__(self):
		super().__init__()
		self.title("Image Viewer")
		self.geometry('800x600')

		if sys.platform in ['win32', 'win64']:
			self.state('zoomed') 
		else:
			self.attributes('-zoomed', True)

		self.canvas = Canvas(self, width=1920, height=1080) # bigger canvas than the window... needed for some reason...?
		self.canvas.bind("<Button-1>", leftclick)
		self.canvas.bind("<Button-2>", middleclick)
		self.canvas.bind("<Button-3>", rightclick)
		self.canvas.pack(fill=BOTH)


		self.img=PhotoImage(file='simplevnc.png')
		self.imgArea = self.canvas.create_image(0, 0, anchor=CENTER, image=self.img)
		gui_queue.put(lambda: show_logo())

		self.remote_x=0
		self.remote_y=0

def show_logo():
	new_x=(app.winfo_width()-app.img.width())/2
	new_y=(app.winfo_height()-app.img.height())/2
	app.canvas.moveto(app.imgArea, x=new_x, y=new_y)

def update_screenshot(screenshot: Image):
	app.remote_x=screenshot.width
	app.remote_y=screenshot.height

	aspect_ratio = screenshot.width/screenshot.height
	canvas_aspect_ratio = app.winfo_width()/app.winfo_height()	

	if aspect_ratio > canvas_aspect_ratio:
		new_size=(app.winfo_width(), int(app.winfo_width()/aspect_ratio))
	else:
		new_size=(int(app.winfo_height()*aspect_ratio), app.winfo_height())

	image = screenshot.resize(new_size, Image.Resampling.LANCZOS)
	
	app.img = ImageTk.PhotoImage(image)
	app.canvas.itemconfig(app.imgArea, image=app.img)

	new_x=int((app.winfo_width()-image.width)/2)
	new_y=int((app.winfo_height()-image.height)/2)
	app.canvas.moveto(app.imgArea, x=new_x, y=new_y)

	try:
		app.update()
		debug('updating... pasemite')###
	except:
		pass

async def read_updates(client: asyncvnc.Client):
	while True:
		await client.read()

async def run_client():
	async with asyncvnc.connect(sys.argv[1], int(sys.argv[2]), None, sys.argv[3]) as client:
		global global_client
		global_client=client
		while True:
			client.video.refresh()

			# Handle packets for a few seconds
			try:
				await asyncio.wait_for(read_updates(client), 0.5)
			except asyncio.TimeoutError:
				pass

			# Retrieve pixels as a 3D numpy array
			pixels = client.video.as_rgba()

			# Save as ImageTk using PIL/pillow
			screenshot = Image.fromarray(pixels)
			debug('new screenshot')###
			gui_queue.put(lambda: update_screenshot(screenshot))
			try:
				fn = input_queue.get_nowait()
			except queue.Empty:
				continue
			await fn()

async def send_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.click()
	print('sending click')

async def send_right_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.middle_click()

async def send_middle_click(x, y):
	global_client.mouse.move(int(x), int(y))
	global_client.mouse.right_click()


def gui_refresh():
	while True:
		try:
			fn = gui_queue.get_nowait()
		except queue.Empty:
			break
		fn()
	app.after(10, gui_refresh)

def start_loop():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.create_task(run_client())
	loop.run_forever()

thread=threading.Thread(target=start_loop, daemon=True)
thread.start()

gui_queue = queue.Queue()
input_queue = queue.Queue()
app = ImageViewer()
app.after(10, gui_refresh)
app.mainloop()