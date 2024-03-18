#!/usr/bin/env python3

import hashlib
import PIL
import pyautogui
from pyscreeze import screenshot
import pytesseract
import threading
import time
import tkinter

class GameOCR:
    app: tkinter.Tk

    ocr_interval: float = 0.1 # 100ms

    drawing: bool = False
    start_x: int | None = None
    start_y: int | None = None
    rectangle_coordinates: tuple[int, int, int, int] | None = None

    runngin_ocr: bool = True

    def __init__(self) -> None:
        self.app = tkinter.Tk()

        # alpha metric
        self.app.attributes("-alpha", 0.3)

    def display(self) -> None:
        screen_width: int = self.app.winfo_screenwidth()
        screen_height: int = self.app.winfo_screenheight()

        self.app.title("Game OCR")
        self.app.geometry(f"{screen_width}x{screen_height}")

        self.tk_canvas = tkinter.Canvas(master=self.app, width=screen_width, height=screen_height)
        self.tk_canvas.grid(row=1, column=0)

        self.tk_canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.tk_canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.tk_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.app.mainloop()
        self.runngin_ocr = False

    def start_drawing(self, event=None) -> None:
        if self.drawing == False and event is not None:
            self.drawing = True
            self.start_x = event.x
            self.start_y = event.y

    def draw_rectangle(self, event=None) -> None:
        if self.drawing == False or event is None:
            return

        current_x: int = event.x
        current_y: int = event.y

        self.tk_canvas.delete("display_rectangle")
        self.tk_canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, outline="blue", width=2, tags=["display_rectangle"])

    def stop_drawing(self, event=None) -> None:
        if self.drawing == False or event is None:
            return

        current_x: int = event.x
        current_y: int = event.y

        self.tk_canvas.delete("display_rectangle")

        start_x: int = self.tk_canvas.winfo_rootx() + self.start_x
        start_y: int = self.tk_canvas.winfo_rooty() + self.start_y
        end_x: int = self.tk_canvas.winfo_rootx() + current_x
        end_y: int = self.tk_canvas.winfo_rooty() + current_y

        # Reverse
        if start_x >= end_x:
            start_x = end_x
            end_x = self.tk_canvas.winfo_rootx() + self.start_x
        if start_y >= end_y:
            start_y = end_y
            end_y = self.tk_canvas.winfo_rooty() + self.start_y

        self.rectangle_coordinates = (start_x, start_y, end_x, end_y)
        #print(self.rectangle_coordinates)

        # minimize
        self.app.iconify()

        self.drawing = False

    def run_ocr(self) -> None:
        hash_before: str = ""

        while self.runngin_ocr == True:
            time.sleep(self.ocr_interval)

            if self.rectangle_coordinates is None:
                continue

            screenshot = self.caputure_screen(
                self.rectangle_coordinates[0],
                self.rectangle_coordinates[1],
                self.rectangle_coordinates[2],
                self.rectangle_coordinates[3]
            )

            if screenshot is None:
                continue

            data: bytes = screenshot.tobytes()
            hash_now: str = hashlib.sha3_256(data).hexdigest()

            if hash_now == hash_before:
                continue

            hash_before = hash_now
            #print("[DEBUG]", "HASH3-256:", hash_now)

            # Zoom
            magnification: int = 2
            size: tuple[int, int] = (round(screenshot.width * magnification), round(screenshot.height * magnification))
            screenshot = screenshot.resize(size, resample=PIL.Image.BICUBIC)

            screenshot.save("./screenshot.png")

            text: str = pytesseract.image_to_string(screenshot,
                                                    lang="jpn",
                                                    config="--psm 6")
            print(text)

    def caputure_screen(self, start_x: int, start_y: int, end_x: int, end_y: int, is_grayscale: bool = False):
        screenshot = None
        try:
            screenshot = pyautogui.screenshot(region=(
                    start_x,
                    start_y,
                    end_x - start_x,
                    end_y - start_y
                ))
        except pyautogui.ImageNotFoundException:
            pass
        return screenshot

if __name__ == "__main__":
    gameocr = GameOCR()

    thread_orc = threading.Thread(target=gameocr.run_ocr)
    thread_orc.start()

    gameocr.display()
    thread_orc.join()
