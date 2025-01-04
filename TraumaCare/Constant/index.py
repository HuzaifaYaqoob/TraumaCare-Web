

from django.conf import settings
from Constants.Data.Profile import DUMMY_PROFILE_IMAGE

import time
from PIL import Image
from datetime import datetime
import os

def addWatermark(input_image, output_path):
    last_dir = "/".join(output_path.split('/')[:-1])
    if not os.path.exists(last_dir):
        print('Creating directory')
        os.makedirs(last_dir)

    print(input_image.url)
    foreground_path = f'{settings.BASE_DIR}/Files/tc_icon.png'
    foreground = Image.open(foreground_path).convert("RGBA")
    img_name = input_image.name
    ext = img_name.split('.')[-1]
    try:
        background = Image.open(input_image)
    except:
        background = Image.open(input_image.url)
    bg_w, bg_h = background.size

    # Calculate the size of the foreground image based on the background
    cfg_w, cfg_h = bg_w // 2, bg_h // 2

    foreground_path = f'{settings.BASE_DIR}/Files/tc_icon.png'
    foreground = Image.open(foreground_path).convert("RGBA")

    # Calculate aspect ratio
    aspect_ratio = foreground.width / foreground.height

    # Calculate new width and height while maintaining aspect ratio
    new_width = cfg_w
    new_height = int(new_width / aspect_ratio)

    # Resize the foreground image
    foreground = foreground.resize((new_width, new_height), Image.ANTIALIAS)
    fg_w, fg_h = foreground.size

    # Calculate position to paste the foreground image at the center of the background
    x, y = ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2)

    # Adjust alpha channel if it exists
    bands = list(foreground.split())
    if len(bands) == 4:
        # Assuming alpha is the last band
        opacity = 0.2
        bands[3] = bands[3].point(lambda x: x * opacity)
        foreground = Image.merge(foreground.mode, bands)

    # Paste the foreground image onto the background
    background.paste(foreground, (x, y), foreground)

    # Save the resulting image
    time.sleep(1)
    today_time = datetime.now()
    time_now = today_time.strftime("%d-%H%M%S")
    
    saving_url = output_path

    background.save(saving_url, quality=100)
    return f'{saving_url}'.split('media/')[-1]