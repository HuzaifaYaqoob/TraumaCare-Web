



from django.core.management.base import BaseCommand
import os
import cv2
import numpy as np


def remove_white_background(image_path, output_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    if image is None:
        print(f"Failed to load image: {image_path}")
        return
    
    # Convert to RGBA if not already
    if image.shape[2] != 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Create a mask where white pixels are detected
    lower = np.array([240, 240, 240, 0])  # Lower bound for white in RGBA
    upper = np.array([255, 255, 255, 255])  # Upper bound for white in RGBA
    mask = cv2.inRange(image, lower, upper)
    
    # Invert the mask
    mask = cv2.bitwise_not(mask)
    
    # Add transparency to the white areas
    image[:, :, 3] = mask
    
    name = output_path.split('.')[0]
    # Save the image with the background removed
    new_path = f'{name}.png'
    if new_path != output_path:
        os.remove(output_path)
    cv2.imwrite(new_path, image)
    print(f"Processed and saved: {output_path}")

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        directory_path = "media/Product/images/2025-01/"
        print(len(os.listdir(directory_path)))
        for file in os.listdir(directory_path):
            # Get full path of the file
            file_path = os.path.join(directory_path, file)
            
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Processing: {file_path}")
                
                remove_white_background(file_path, file_path)

        self.stdout.write(self.style.SUCCESS('Done'))

