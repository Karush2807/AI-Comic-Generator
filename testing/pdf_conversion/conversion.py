from PIL import Image
import os

# Folder where your comic pages are stored
image_folder = "..\Panel\Pages"
output_pdf_path = "Comic_Book.pdf"

# Delete existing PDF if it exists
if os.path.exists(output_pdf_path):
    os.remove(output_pdf_path)
    print(f"Old comic PDF '{output_pdf_path}' deleted.")

# Get all image file names (assuming they are .png, .jpg, or .jpeg)
image_files = sorted(
    [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
)

# Convert images to RGB and add them to a list
image_list = []
for file_name in image_files:
    image_path = os.path.join(image_folder, file_name)
    img = Image.open(image_path).convert("RGB")
    image_list.append(img)

# Save as PDF
if image_list:
    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
    print(f"PDF saved successfully as '{output_pdf_path}'")
else:
    print("No images found to convert.")
