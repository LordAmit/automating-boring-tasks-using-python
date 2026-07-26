from PIL import Image, ImageOps, ExifTags
import os


# Function to correct orientation using EXIF metadata
def correct_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()  # Get EXIF data
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:  # Rotated 180 degrees
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:  # Rotated 270 degrees clockwise
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:  # Rotated 90 degrees clockwise
                img = img.rotate(90, expand=True)
    except Exception as e:
        print(f"Error correcting orientation: {e}")
    return img

# Function to resize the image to a maximum size of 2000 pixels
def resize_image(img, max_size=2000):
    width, height = img.size
    if max(width, height) > max_size:
        scaling_factor = max_size / max(width, height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    return img

def squarify(input_folder):
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print("Processing: "+filename)
            # Open the image
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            # Correct the orientation using EXIF metadata
            img = correct_orientation(img)
            img = resize_image(img, max_size=2000)

            # Get the dimensions of the image
            width, height = img.size

            # Calculate the new dimensions to make the image square
            max_dim = max(width, height)
            horizontal_padding = (max_dim - width) // 2
            vertical_padding = (max_dim - height) // 2

            # Add a white border to make the image square
            img_with_border = ImageOps.expand(
                img,
                border=(horizontal_padding, vertical_padding, horizontal_padding, vertical_padding),
                fill='white'
            )

            # Save the processed image to the output folder
            output_path = os.path.join(output_folder, filename)
            img_with_border.save(output_path)

            print(f"Processed and saved: {output_path}")

    print("Batch processing completed!")

# Define input and output folder paths
input_folder = os.getcwd()  # Folder containing original images
output_folder = os.getcwd()+"/output_images"  # Folder to save processed images

print(input_folder)
print(output_folder)
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

squarify(input_folder)
