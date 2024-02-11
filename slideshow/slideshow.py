"""

Slideshow object: show images in a folder + folders

"""

from dataclasses import dataclass
from rich.console import Console
from PIL import Image, ImageTk
import PySimpleGUI as sg
import ctypes

console = Console()


@dataclass
class Slideshow:
    directory: str
    include_sub_folders: bool
    delay: int
    rollover: bool

    def run(self) -> None:
        console.print(
            f"Starting Slideshow in {'current directory' if self.directory == '' else self.directory} "
            f"{'including sub directories' if self.include_sub_folders else ''}",
            style="green",
        )
        console.print(
            f"Rollover is {'active' if self.rollover else ''}, "
            f"delay between images: {(str(self.delay) + 's') if self.delay != 0 else 'Keypress'}",
            style="green",
        )

        image_name = "mandelbrot.jpg"

        im = Image.open(image_name)

        # Create a Pysimplegui window
        sg.theme("DarkGreen3")

        # determine screen size
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        console.print(f"Screen size is {screensize}", style="white")

        layout = [
            [sg.Image(size=screensize, key="-IMAGE-")],
        ]

        window = sg.Window(
            "Slideshow", layout, margins=(0, 0), no_titlebar=True, finalize=True
        )
        window.Maximize()

        # Convert im to ImageTk.PhotoImage after window finalized
        im = im.resize(screensize, resample=Image.BICUBIC)
        image = ImageTk.PhotoImage(image=im)

        # update image in sg.Image
        console.print(f"Showing image '{image_name}' {im}", style="green")
        window["-IMAGE-"].update(data=image)

        # Create an event loop
        while True:
            event, values = window.read()
            # End program if user closes window or
            # presses the OK button
            if event == sg.WIN_CLOSED:
                break

        window.close()
