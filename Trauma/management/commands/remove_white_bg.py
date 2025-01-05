



from django.core.management.base import BaseCommand
import os
import cv2
import numpy as np

def remove_white_background_and_crop(image_path, output_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    if image is None:
        print(f"Failed to load image: {image_path}")
        return
    
    # Convert to RGBA if not already
    if len(image.shape) == 3 and image.shape[2] == 3:  # If the image is RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Create a mask where white pixels are detected
    lower = np.array([240, 240, 240])  # Lower bound for white
    upper = np.array([255, 255, 255])  # Upper bound for white
    white_mask = cv2.inRange(image[:, :, :3], lower, upper)
    
    # Invert the mask to keep non-white areas
    alpha_mask = cv2.bitwise_not(white_mask)

    # Apply the new alpha channel
    image[:, :, 3] = alpha_mask

    # Find the bounding box of non-transparent pixels
    coords = cv2.findNonZero(alpha_mask)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped_image = image[y:y+h, x:x+w]
    else:
        print(f"No content found in image: {image_path}")
        return
    
    # Save the cropped image with the background removed
    name = output_path.split('.')[0]
    new_path = f'{name}.png'
    if new_path != output_path:
        os.remove(output_path)
    cv2.imwrite(new_path, cropped_image)
    print(f"Processed and saved: {new_path}")

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
                
                remove_white_background_and_crop(file_path, file_path)

        self.stdout.write(self.style.SUCCESS('Done'))

