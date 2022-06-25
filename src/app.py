import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


class LookbookComparisonCreatorApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Lookbook Comparison Creator")

        # Place Window Centered
        width = 450
        height = 160
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x_win = (width_screen/2) - (width/2)
        y_win = (height_screen/2) - (height/2)
        self.geometry("%dx%d+%d+%d" % (width, height, x_win, y_win))

        self.minsize(width=width, height=height)
        self.maxsize(width=width + 200, height=height)

        self.columnconfigure(0, weight=1)
        self.frame = ttk.Frame(padding='10')
        self.frame.columnconfigure(1, weight=1)
        self.frame.grid(sticky="NEWS")

        # FFMPEG
        self.ffmpeg_cmd = tk.StringVar(self)
        self.ffmpeg_label = ttk.Label(self.frame, text="FFmpeg:")
        self.ffmpeg_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.ffmpeg_entry = ttk.Entry(
                self.frame, justify="left", textvariable=self.ffmpeg_cmd)
        self.ffmpeg_entry.grid(
                row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)

        self.choose_ffmpeg_button = ttk.Button(
                self.frame, text='Choose',
                command=self.select_ffmpeg)
        self.choose_ffmpeg_button.grid(
                row=0, column=3, padx=5, pady=5, sticky="E"
                )

        # SOURCE DIRECTORY
        self.source_dir = tk.StringVar(self)
        self.source_label = ttk.Label(self.frame, text="Source:")
        self.source_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.source_entry = ttk.Entry(
                self.frame, justify="left", textvariable=self.source_dir)
        self.source_entry.grid(
                row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)
        self.choose_source_button = ttk.Button(
                self.frame, text='Choose',
                command=self.select_source)
        self.choose_source_button.grid(
                row=1, column=3, padx=5, pady=5, sticky="E"
                )

        # COMPARISON STRING
        self.key_string = tk.StringVar(self)
        self.key_label = ttk.Label(self.frame, text="Keys:", width=6)
        self.key_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.key_entry = ttk.Entry(
                self.frame, justify="left", textvariable=self.key_string)
        self.key_entry.grid(
                row=2, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        # RUN
        self.run_button = ttk.Button(
        self, text="Create Quicktime", command=self.run)
        self.run_button.grid(row=0, column=3, sticky="ES", padx=5, pady=5)

    def select_source(self):
        initialdir = os.path.dirname(self.ffmpeg_cmd.get())
        new_source = fd.askdirectory(
            title='Choose source file', initialdir=initialdir)
        if new_source:
            self.source_dir.set(new_source)

    def select_ffmpeg(self):
        initialdir = os.path.dirname(self.ffmpeg_cmd.get())
        new_ffmpeg_cmd = fd.askopenfilename(
            title='Choose source file', initialdir=initialdir)
        if new_ffmpeg_cmd:
            self.ffmpeg_cmd.set(new_ffmpeg_cmd)


    def run(self):

    
def main():
    app = LookbookComparisonCreatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
