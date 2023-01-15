import queue
import threading
from tkinter import *

import asyncio
import asyncvnc.asyncvnc as asyncvnc
from PIL import Image, ImageTk
import sys

global app

class ImageViewer(Tk):
	def __init__(self):
		super().__init__()
		self.title("Image Viewer")
		self.geometry("800x600")
		self.canvas = Canvas(self, width=800, height=480)
		self.img = PhotoImage(file='simplevnc.png')
		self.imgArea = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
		self.canvas.pack()

def update_screenshot(screenshot: PhotoImage):
	app.img = screenshot
	app.canvas.itemconfig(app.imgArea, image=app.img)
	try:
		app.update()
		print('updating... pasemite')
	except:
		pass

async def read_updates(client: asyncvnc.Client):
	while True:
		await client.read()

async def run_client():
	async with asyncvnc.connect(sys.argv[1], int(sys.argv[2]), None, sys.argv[3]) as client:
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
			image = Image.fromarray(pixels)#.convert('RGB')
			screenshot=ImageTk.PhotoImage(image)
			print('new screenshot')
			gui_queue.put(lambda: update_screenshot(screenshot))

# root.mainloop()

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
app = ImageViewer()
app.after(10, gui_refresh)
app.mainloop()