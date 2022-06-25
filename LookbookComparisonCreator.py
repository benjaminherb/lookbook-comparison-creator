import os
import time
import subprocess
import math
import re
import platform
import multiprocessing
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


def main():
    app = LookbookComparisonCreatorApp()
    app.mainloop()

    #source_dir = "540"
    #for key in DEFAULT_KEYS:
    #    output_file = f"{OUTPUT_DIR}/{('_'.join(key)).replace(' ', '_').replace('|', '+')}.mov"
    #    create_comparison_clips(key, source_dir, output_file)

# CLI
OUTPUT_RESOLUTION = "1920:1080"
INPUT_RESOLUTION = "1920:1080"
OUTPUT_DIR = "out_update"

DEFAULT_KEYS = [
    ['Key', 'Close', 'Orbiter|Robe', '°', '-Frost'],
    [''],
    ['Kicker'],
    ['Key', 'Close'],
    ['Key', 'Wide'],
    ['Key', 'Close', 'Orbiter'],
    ['Key', 'Wide', 'Orbiter'],
    ['Kicker', 'Orbiter'],
    ['Key', 'Close', 'Maxi Mix'],
    ['Key', 'Wide', 'Maxi Mix'],
    ['Kicker', 'Maxi Mix'],
    ['Key', 'Close', 'Mini Mix'],
    ['Key', 'Wide', 'Mini Mix'],
    ['Kicker', 'Mini Mix'],
    ['Key', 'Close', 'Astera'],
    ['Key', 'Wide', 'Astera'],
    ['Kicker', 'Astera'],
    ['Key', 'Close', 'LIGHTBRIDGE'],
    ['Key', 'Wide', 'LIGHTBRIDGE'],
    ['Kicker', 'LIGHTBRIDGE'],
    ['Key', 'Close', 'Robe'],
    ['Key', 'Wide', 'Robe'],
    ['Kicker', 'Robe'],
    ['Key', 'Close', 'SL1'],
    ['Key', 'Wide', 'SL1'],
    ['Kicker', 'SL1'],
    ['Key', 'Close', 'Dash Light'],
    ['Key', 'Wide', 'Dash Light'],
    ['Kicker', 'Dash Light'],
]


def create_comparison_clips(ffmpeg_cmd, key, source_dir, output_file):

    files = os.listdir(source_dir)

    input_files = []
    max_files = []
    # Check for matching input files
    for file in files:
        add = True
        for subkey in key:
            if subkey.startswith('-'):
                if re.search(subkey[1:], file):
                    add = False
            else:
                if not re.search(subkey, file):
                    add = False

        if add:
            if file.find("100%") != -1:
                max_files.append(file)
            elif file.find("255 (8-bit)") != -1:
                # all robe shots had enough output
                pass
            else:
                input_files.append(file)

    for file in max_files:
        pos_brightness = file.find("100%")
        if file[:pos_brightness] not in '\t'.join(input_files):
            input_files.append(file)

    input_files.sort()

    print(f"FOR {key} THERE WERE {len(input_files)} FILES")
    print('\n'.join(input_files))
    print()

    ffmpeg_cmd = [
            ffmpeg_cmd,
            ]

    for input in input_files:
        ffmpeg_cmd.append("-i")
        ffmpeg_cmd.append(f"{source_dir}/{input}")

    # calculate the best grid for the video count
    squared = round(math.sqrt(len(input_files)))
    if squared*squared < len(input_files):
        grid_h, grid_v = [squared + 1, squared]
    else:
        grid_h, grid_v = [squared, squared]
    print(f"H/V {grid_h} - {grid_v}")

    # pad inputs with black videos if there is no good grid possible
    for i in range(0, (grid_h) * (grid_v) - len(input_files)):
        ffmpeg_cmd.extend([
            "-f", "lavfi", "-i",
            f"color=c=black:s={INPUT_RESOLUTION.replace(':','x')}:r=24:d=1",
            ])

    filter_string = ""
    down_scale_string = ""
    v = 0
    for i in range(0, grid_v):
        for j in range(0, grid_h):
            filter_string += f"[{v}:v]"
            v += 1
        filter_string += f"hstack=inputs={grid_h}[stack_{i}];"

    for i in range(0, grid_v):
        filter_string += f"[stack_{i}]"

    filter_string += f"vstack=inputs={grid_v}[v];"
    filter_string += f"[v]scale={OUTPUT_RESOLUTION}:force_original_aspect_ratio=decrease,pad={OUTPUT_RESOLUTION}:(ow-iw)/2:(oh-ih)/2[v]"

    ffmpeg_cmd.extend([
        "-filter_complex", down_scale_string + filter_string,
        "-map", "[v]",
        "-y",
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-loglevel", "warning",
        "-stats",
        output_file
        ])

    print(f"FFMPEG CMD: \n{ffmpeg_cmd}")

    run_output = subprocess.run(ffmpeg_cmd, capture_output=True)
    print(run_output)


# GUI

class LookbookComparisonCreatorApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Lookbook Comparison Creator")
        # Place Window Centered
        width = 450
        height = 190
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x_win = (width_screen/2) - (width/2)
        y_win = (height_screen/2) - (height/2)
        self.geometry("%dx%d+%d+%d" % (width, height, x_win, y_win))

        self.minsize(width=width, height=height)
        self.maxsize(width=width + 200, height=height)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame = ttk.Frame(padding='10')
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.grid(sticky="NEWS")

        # FFMPEG
        self.ffmpeg_cmd = tk.StringVar(self, 'ffmpeg')
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
        self.source_dir = tk.StringVar(self, '~')
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
        self.key_string = tk.StringVar(self, 'Key,Close,Orbiter|Robe,°,-Frost')
        self.key_label = ttk.Label(self.frame, text="Keys:")
        self.key_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.key_entry = ttk.Entry(
                self.frame, justify="left", textvariable=self.key_string)
        self.key_entry.grid(
                row=2, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        # RUN
        self.run_button = ttk.Button(
            self.frame, text="Create Video", command=self.run)
        self.run_button.grid(row=3, column=1, sticky="EWS", padx=5, pady=5)

    def select_source(self):
        initialdir = os.path.dirname(self.source_dir.get())
        new_source = fd.askdirectory(
            title='Choose source file', initialdir=initialdir)
        if new_source:
            self.source_dir.set(new_source)

    def select_ffmpeg(self):
        initialdir = self.ffmpeg_cmd.get()
        new_ffmpeg_cmd = fd.askopenfilename(
            title='Choose ffmpeg binary', initialdir=initialdir)
        if new_ffmpeg_cmd:
            self.ffmpeg_cmd.set(new_ffmpeg_cmd)

    def run(self):
        key = self.key_string.get().split(',')
        initial_filename = f"{('_'.join(key)).replace(' ', '_').replace('|', '+')}"
        self.toggle_ui(state='disable')
        output_file = fd.asksaveasfilename(
                initialdir='~', initialfile=initial_filename,
                filetypes=[('Video Files', '*.mp4'), ('All Files', '*')])

        # if it was canceled
        if output_file == "":
            return

        self.render_process = multiprocessing.Process(
                target=create_comparison_clips,
                args=(
                    self.ffmpeg_entry.get(), key,
                    self.source_dir.get(), output_file))
        self.render_process.start()

        while self.render_process.is_alive():
            self.update()
            time.sleep(1)
            print("RUNNING")

        self.render_process.join()
        self.toggle_ui('enable')

        # Try to open finished video
        try:
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', output_file))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(output_file)
            else:                                   # linux variants
                subprocess.call(('xdg-open', output_file))
        except Exception as e:
            print(f"FAILED TO OPEN {e}")

    def cancel(self):
        if self.render_process.is_alive():
            self.render_process.terminate()

    def toggle_ui(self, state='disable'):
        self.ffmpeg_entry.configure(state=state)
        self.choose_ffmpeg_button.configure(state=state)
        self.source_entry.configure(state=state)
        self.choose_source_button.configure(state=state)
        self.key_entry.configure(state=state)

        if state == 'disable':
            self.run_button.configure(
                    text='Cancel', command=self.cancel)
        else:
            self.run_button.configure(
                    text='Create Video', command=self.run)


if __name__ == "__main__":
    main()
