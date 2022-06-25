import os
import math
import re
import subprocess

OUTPUT_RESOLUTION = "1920:1080"
INPUT_RESOLUTION = "960:540"
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


if __name__ == '__main__':

    source_dir = "540"
    for key in DEFAULT_KEYS:
        output_file = f"{OUTPUT_DIR}/{('_'.join(key)).replace(' ', '_').replace('|', '+')}.mov"
        create_comparison_clips(key, source_dir, output_file)
