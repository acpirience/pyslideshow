"""

Slideshow object: show images in a folder + folders

"""

from dataclasses import dataclass
from rich.console import Console
from PIL import Image, ImageTk
import PySimpleGUI as sg
import ctypes
import os
import glob
import time

VALID_IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".tiff"]

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
            f"Rollover is {'active' if self.rollover else 'inactive'}, "
            f"delay between images: {(str(self.delay) + 's') if self.delay != 0 else 'Keypress'}",
            style="green",
        )

        self.img_file = self.get_filenames()
        if not self.img_file:
            console.print("*** Error: No files to show ***", style="red")
            exit(1)

        self.idx = 0

        # determine screen size
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        console.print(f"Screen size is {self.screensize}", style="white")

        self.init_window()
        self.exit_requested = False

        # Show first image
        self.idx = self.show_next_image()

        # delay, used if delay != 0
        self.start_time = time.time()
        console.log(self.start_time)

        # Create an event loop
        while not self.exit_requested:
            event, values = self.window.read(timeout=10)
            # End program if user pres ESCAPE
            if event in (sg.WINDOW_CLOSED, "-ESCAPE-"):
                break
            # Next image with ENTER
            if event in (sg.WINDOW_CLOSED, "-ENTER-"):
                self.idx = self.show_next_image()
                self.start_time = time.time()

            # Next image if delay is passed
            if self.delay != 0:
                if time.time() - self.start_time > self.delay:
                    self.idx = self.show_next_image()
                    self.start_time = time.time()

        self.window.close()

    def get_filenames(self) -> list[str]:
        file_list: list[str] = []
        file_pattern = "*.*"
        if self.include_sub_folders:
            file_pattern = "**/*.*"

        files = glob.glob(
            os.path.join(self.directory, file_pattern),
            recursive=self.include_sub_folders,
        )
        for file in files:
            if os.path.isfile(file):
                if os.path.splitext(file)[1].lower() in VALID_IMG_EXTENSIONS:
                    file_list.append(file)

        return file_list

    def init_window(self) -> None:
        # Create a Pysimplegui window
        layout = [
            [sg.Image(size=self.screensize, key="-IMAGE-")],
        ]

        self.window = sg.Window(
            "Slideshow", layout, margins=(0, 0), no_titlebar=True, finalize=True
        )
        self.window.Maximize()
        self.window.bind("<Escape>", "-ESCAPE-")
        self.window.bind("<Return>", "-ENTER-")

    def show_next_image(self) -> int:
        image_name = self.img_file[self.idx]
        im = Image.open(image_name)
        img_size = im.size
        img_resized = Slideshow.get_resize_dim(img_size, self.screensize)
        im = im.resize(img_resized, resample=Image.BICUBIC)

        image = Image.new("RGB", (self.screensize[0], self.screensize[1]))
        coords = (
            int((self.screensize[0] - img_resized[0]) / 2),
            int((self.screensize[1] - img_resized[1]) / 2),
        )
        image.paste(im, coords)

        tk_image = ImageTk.PhotoImage(image=image)

        console.print(
            f"Showing image '{image_name}' {img_size}->{img_resized}", style="green"
        )
        self.window["-IMAGE-"].update(data=tk_image)

        self.idx += 1
        if self.idx == len(self.img_file):
            if self.rollover:
                self.idx = 0
            else:
                console.print("Last image", style="red")
                self.exit_requested = True

        return self.idx

    @staticmethod
    def get_resize_dim(
        image_size: tuple[int, int], screen_size: tuple[int, int]
    ) -> tuple[int, int]:
        screen_ratio = screen_size[0] / screen_size[1]
        image_ratio = image_size[0] / image_size[1]

        if screen_ratio > image_ratio:
            h = float(screen_size[1])
            w = image_ratio * h
        else:
            w = float(screen_size[0])
            h = w / image_ratio

        return (int(w), int(h))
