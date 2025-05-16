# # from rembg import remove
# # from PIL import Image, ImageDraw, ImageFont
# # import io
# # import os
# # import re

# # character_input_folder = "..\Background\characters"
# # character_output_folder = "transparent_characters" 

# # # Clear and recreate transparent character folder
# # if os.path.exists(character_output_folder):
# #     for file in os.listdir(character_output_folder):
# #         file_path = os.path.join(character_output_folder, file)
# #         if os.path.isfile(file_path):
# #             os.remove(file_path)
# # else:
# #     os.makedirs(character_output_folder)

# # # Remove backgrounds from character images
# # for filename in os.listdir(character_input_folder):
# #     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
# #         character_input_path = os.path.join(character_input_folder, filename)
# #         with open(character_input_path, "rb") as f:
# #             input_data = f.read()
# #             output_data = remove(input_data)    
# #         output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
# #         output_filename = os.path.splitext(filename)[0].split()[0].lower() + "_transparent.png"
# #         output_path = os.path.join(character_output_folder, output_filename)
# #         output_image.save(output_path)
# #         print(f"Processed: {filename} → {output_filename}")

# # script_path = "..\Script\comic_script.txt"
# # background_input_folder = "..\Background\images"
# # character_folder = "transparent_characters"
# # output_folder = "Pages"

# # os.makedirs(output_folder, exist_ok=True)

# # import textwrap
# # from PIL import ImageDraw, ImageFont

# # # === Load and parse the script ===
# # with open(script_path, "r") as file:
# #     content = file.read()

# # # === Split the script into scenes using regex ===
# # scenes = re.findall(
# #     r'\d+\.\s*Scene Description: (.*?)\nCharacters Involved: (.*?)\nDialogues: (.*?)(?=\n\d+\.|$)',
# #     content,
# #     re.DOTALL
# # )

# # # === Process each scene ===
# # for i, (scene_desc, character_line, dialogue_line) in enumerate(scenes):
# #     background_path = os.path.join(background_input_folder, f"panel_{i+1}.png")
# #     output_path = os.path.join(output_folder, f"scene_{i+1}.png")

# #     # Load background
# #     try:
# #         background = Image.open(background_path).convert("RGBA")
# #     except FileNotFoundError:
# #         print(f"Background panel_{i+1}.png not found. Skipping...")
# #         continue

# #     # Extract character names
# #     character_names = [name.strip().split()[0].lower() for name in character_line.split(",") if name.strip()]

# #     # Extract dialogues as name: line
# #     dialogues = []
# #     if dialogue_line.strip().lower() != "none":
# #         lines = [l.strip() for l in dialogue_line.split(",")]
# #         for l in lines:
# #             if ':' in l:
# #                 speaker, line = l.split(":", 1)
# #                 dialogues.append((speaker.strip().lower(), line.strip()))

# #     margin = 15
# #     positions = []

# #     for idx, name in enumerate(character_names[:2]):
# #         char_path = os.path.join(character_folder, f"{name}_transparent.png")
# #         if not os.path.exists(char_path):
# #             print(f"Character image not found: {char_path}")
# #             continue

# #         char_img = Image.open(char_path).convert("RGBA")
# #         char_img = char_img.resize((400, 500))

# #         if idx == 0:  # Bottom left
# #             pos = (10, background.height - char_img.height - margin)
# #         else:         # Bottom right
# #             pos = (background.width - char_img.width - margin, background.height - char_img.height - margin)

# #         background.paste(char_img, pos, char_img)
# #         positions.append((name, pos))

# #     # === Add dialogues above characters ===
# #     draw = ImageDraw.Draw(background)
# #     try:
# #         font = ImageFont.truetype("arial.ttf", 27)
# #     except:
# #         font = ImageFont.load_default()
    
# #     for speaker, line in dialogues:
# #         for name, (x, y) in positions:
# #             if name == speaker:
# #                 text = textwrap.fill(line, width=30)
# #                 text_size = draw.textbbox((0, 0), text, font=font)
# #                 text_w = text_size[2] - text_size[0]
# #                 text_h = text_size[3] - text_size[1]
                    
# #                 # Tighter vertical spacing and left alignment
# #                 bubble_x = x + 60   # slight indent from character left
# #                 bubble_y = y - text_h - 10  # closer vertically
                    
# #                 draw.rectangle([bubble_x - 8, bubble_y - 6, bubble_x + text_w + 8, bubble_y + text_h + 6], fill=(255, 255, 255, 220))
# #                 draw.text((bubble_x, bubble_y), text, fill=(0, 0, 0), font=font)
# #                 break


# #     background.save(output_path)
# #     print(f"Scene {i+1} created: {output_path}")





# from rembg import remove
# from PIL import Image, ImageDraw, ImageFont
# import io
# import os
# import re
# import textwrap

# # === Step 1: Remove backgrounds from character images ===
# character_input_folder = "..\Background\characters"
# character_output_folder = "transparent_characters"

# # Clear and recreate transparent character folder
# if os.path.exists(character_output_folder):
#     for file in os.listdir(character_output_folder):
#         file_path = os.path.join(character_output_folder, file)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
# else:
#     os.makedirs(character_output_folder)

# # Remove backgrounds
# for filename in os.listdir(character_input_folder):
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         character_input_path = os.path.join(character_input_folder, filename)
#         with open(character_input_path, "rb") as f:
#             input_data = f.read()
#             output_data = remove(input_data)
#         output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
#         output_filename = os.path.splitext(filename)[0].split()[0].lower() + "_transparent.png"
#         output_path = os.path.join(character_output_folder, output_filename)
#         output_image.save(output_path)
#         print(f"Processed: {filename} → {output_filename}")

# # === Step 2: Parse comic script and generate scenes ===
# script_path = "..\\Script\\comic_script.txt"
# background_input_folder = "..\\Background\\images"
# character_folder = "transparent_characters"
# output_folder = "Pages"
# os.makedirs(output_folder, exist_ok=True)

# # Load and parse script
# with open(script_path, "r") as file:
#     content = file.read()

# # Regex to parse scenes
# scenes = re.findall(
#     r'\d+\.\s*Scene Description: (.*?)\nCharacters Involved: (.*?)\nDialogues: (.*?)(?=\n\d+\.|$)',
#     content,
#     re.DOTALL
# )

# # === Step 3: Process each scene ===
# for i, (scene_desc, character_line, dialogue_line) in enumerate(scenes):
#     background_path = os.path.join(background_input_folder, f"panel_{i+1}.png")
#     output_path = os.path.join(output_folder, f"scene_{i+1}.png")

#     # Load original background
#     try:
#         original_bg = Image.open(background_path).convert("RGBA")
#     except FileNotFoundError:
#         print(f"Background panel_{i+1}.png not found. Skipping...")
#         continue

#     # Prepare scene description text
#     try:
#         desc_font = ImageFont.truetype("arial.ttf", 28)
#     except:
#         desc_font = ImageFont.load_default()

#     scene_text = textwrap.fill(scene_desc.strip(), width=70)
#     dummy_draw = ImageDraw.Draw(original_bg)
#     text_bbox = dummy_draw.textbbox((0, 0), scene_text, font=desc_font)
#     text_height = text_bbox[3] - text_bbox[1]
#     padding = 20

#     # Extend canvas to add description at top
#     new_height = original_bg.height + text_height + padding * 2
#     extended_bg = Image.new("RGBA", (original_bg.width, new_height), (255, 255, 255, 255))
#     draw = ImageDraw.Draw(extended_bg)
#     draw.rectangle([0, 0, extended_bg.width, text_height + padding * 2], fill=(255, 255, 255, 255))
#     draw.text((padding, padding), scene_text, font=desc_font, fill=(0, 0, 0, 255))
#     extended_bg.paste(original_bg, (0, text_height + padding * 2))
#     background = extended_bg

    # # Process characters
    # character_names = [name.strip().split()[0].lower() for name in character_line.split(",") if name.strip()]
    # dialogues = []
    # if dialogue_line.strip().lower() != "none":
    #     lines = [l.strip() for l in dialogue_line.split(",")]
    #     for l in lines:
    #         if ':' in l:
    #             speaker, line = l.split(":", 1)
    #             dialogues.append((speaker.strip().lower(), line.strip()))

    # margin = 15
    # positions = []

    # for idx, name in enumerate(character_names[:2]):
    #     char_path = os.path.join(character_folder, f"{name}_transparent.png")
    #     if not os.path.exists(char_path):
    #         print(f"Character image not found: {char_path}")
    #         continue

    #     char_img = Image.open(char_path).convert("RGBA")
    #     char_img = char_img.resize((400, 500))

    #     if idx == 0:  # Bottom left
    #         pos = (10, background.height - char_img.height - margin)
    #     else:         # Bottom right
    #         pos = (background.width - char_img.width - margin, background.height - char_img.height - margin)

    #     background.paste(char_img, pos, char_img)
    #     positions.append((name, pos))

    # # Add dialogue bubbles
    # try:
    #     font = ImageFont.truetype("arial.ttf", 27)
    # except:
    #     font = ImageFont.load_default()

    # draw = ImageDraw.Draw(background)
    # for speaker, line in dialogues:
    #     for name, (x, y) in positions:
    #         if name == speaker:
    #             text = textwrap.fill(line, width=30)
    #             text_size = draw.textbbox((0, 0), text, font=font)
    #             text_w = text_size[2] - text_size[0]
    #             text_h = text_size[3] - text_size[1]

    #             bubble_x = x + 60
    #             bubble_y = y - text_h - 10

    #             draw.rectangle(
    #                 [bubble_x - 8, bubble_y - 6, bubble_x + text_w + 8, bubble_y + text_h + 6],
    #                 fill=(255, 255, 255, 220)
    #             )
    #             draw.text((bubble_x, bubble_y), text, fill=(0, 0, 0), font=font)
    #             break

#     background.save(output_path)
#     print(f"Scene {i+1} created: {output_path}")





# # # from rembg import remove
# # # from PIL import Image, ImageDraw, ImageFont
# # # import io
# # # import os
# # # import re
# # # import textwrap

# # # # === Step 1: Remove backgrounds from character images ===
# # # character_input_folder = "..\\Background\\characters"
# # # character_output_folder = "transparent_characters"

# # # # Clear and recreate transparent character folder
# # # if os.path.exists(character_output_folder):
# # #     for file in os.listdir(character_output_folder):
# # #         file_path = os.path.join(character_output_folder, file)
# # #         if os.path.isfile(file_path):
# # #             os.remove(file_path)
# # # else:
# # #     os.makedirs(character_output_folder)

# # # # Remove backgrounds
# # # for filename in os.listdir(character_input_folder):
# # #     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
# # #         character_input_path = os.path.join(character_input_folder, filename)
# # #         with open(character_input_path, "rb") as f:
# # #             input_data = f.read()
# # #             output_data = remove(input_data)
# # #         output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
# # #         output_filename = os.path.splitext(filename)[0].split()[0].lower() + "_transparent.png"
# # #         output_path = os.path.join(character_output_folder, output_filename)
# # #         output_image.save(output_path)
# # #         print(f"Processed: {filename} → {output_filename}")

# # # # === Step 2: Parse comic script and generate scenes ===
# # # script_path = "..\\Script\\comic_script.txt"
# # # background_input_folder = "..\\Background\\images"
# # # character_folder = "transparent_characters"
# # # output_folder = "Pages"
# # # os.makedirs(output_folder, exist_ok=True)

# # # # Load and parse script
# # # with open(script_path, "r") as file:
# # #     content = file.read()

# # # # Regex to parse scenes
# # # scenes = re.findall(
# # #     r'\d+\.\s*Scene Description: (.*?)\nScene Explanation: (.*?)\nCharacters Involved: (.*?)\nDialogues: (.*?)(?=\n\d+\.|$)',
# # #     content,
# # #     re.DOTALL
# # # )

# # # # === Step 3: Process each scene ===
# # # for i, (scene_desc, scene_expl, character_line, dialogue_line) in enumerate(scenes):
# # #     background_path = os.path.join(background_input_folder, f"panel_{i+1}.png")
# # #     output_path = os.path.join(output_folder, f"scene_{i+1}.png")

# # #     # Load original background
# # #     try:
# # #         original_bg = Image.open(background_path).convert("RGBA")
# # #     except FileNotFoundError:
# # #         print(f"Background panel_{i+1}.png not found. Skipping...")
# # #         continue

# # #     # Prepare scene description and explanation text
# # #     try:
# # #         desc_font = ImageFont.truetype("arial.ttf", 28)
# # #         expl_font = ImageFont.truetype("arial.ttf", 24)
# # #     except:
# # #         desc_font = ImageFont.load_default()
# # #         expl_font = ImageFont.load_default()

# # #     scene_text = textwrap.fill(scene_desc.strip(), width=70)
# # #     explanation_text = textwrap.fill(scene_expl.strip(), width=70)

# # #     # Dummy draw to calculate text height
# # #     dummy_draw = ImageDraw.Draw(original_bg)
# # #     desc_bbox = dummy_draw.textbbox((0, 0), scene_text, font=desc_font)
# # #     expl_bbox = dummy_draw.textbbox((0, 0), explanation_text, font=expl_font)
# # #     desc_height = desc_bbox[3] - desc_bbox[1]
# # #     expl_height = expl_bbox[3] - expl_bbox[1]
# # #     padding = 20

# # #     # Extend canvas to add description and explanation at top
# # #     new_height = original_bg.height + desc_height + expl_height + padding * 3
# # #     extended_bg = Image.new("RGBA", (original_bg.width, new_height), (255, 255, 255, 255))

# # #     # Draw the scene description and explanation
# # #     draw = ImageDraw.Draw(extended_bg)
# # #     draw.rectangle([0, 0, extended_bg.width, desc_height + padding * 2], fill=(255, 255, 255, 255))
# # #     draw.text((padding, padding), scene_text, font=desc_font, fill=(0, 0, 0, 255))

# # #     # Draw the scene explanation
# # #     draw.rectangle([0, desc_height + padding * 2, extended_bg.width, desc_height + expl_height + padding * 3], fill=(240, 240, 240, 255))
# # #     draw.text((padding, desc_height + padding * 2), explanation_text, font=expl_font, fill=(0, 0, 0, 255))

# # #     # Paste the original background after the extended portion
# # #     extended_bg.paste(original_bg, (0, desc_height + expl_height + padding * 3))
# # #     background = extended_bg

# # #     # Process characters
# # #     character_names = [name.strip().split()[0].lower() for name in character_line.split(",") if name.strip()]
# # #     dialogues = []
# # #     if dialogue_line.strip().lower() != "none":
# # #         lines = [l.strip() for l in dialogue_line.split(",")]
# # #         for l in lines:
# # #             if ':' in l:
# # #                 speaker, line = l.split(":", 1)
# # #                 dialogues.append((speaker.strip().lower(), line.strip()))

# # #     margin = 15
# # #     positions = []

# # #     for idx, name in enumerate(character_names[:2]):
# # #         char_path = os.path.join(character_folder, f"{name}_transparent.png")
# # #         if not os.path.exists(char_path):
# # #             print(f"Character image not found: {char_path}")
# # #             continue

# # #         char_img = Image.open(char_path).convert("RGBA")
# # #         char_img = char_img.resize((400, 500))

# # #         if idx == 0:  # Bottom left
# # #             pos = (10, background.height - char_img.height - margin)
# # #         else:         # Bottom right
# # #             pos = (background.width - char_img.width - margin, background.height - char_img.height - margin)

# # #         background.paste(char_img, pos, char_img)
# # #         positions.append((name, pos))

# # #     # Add dialogue bubbles
# # #     try:
# # #         font = ImageFont.truetype("arial.ttf", 27)
# # #     except:
# # #         font = ImageFont.load_default()

# # #     draw = ImageDraw.Draw(background)
# # #     for speaker, line in dialogues:
# # #         for name, (x, y) in positions:
# # #             if name == speaker:
# # #                 text = textwrap.fill(line, width=30)
# # #                 text_size = draw.textbbox((0, 0), text, font=font)
# # #                 text_w = text_size[2] - text_size[0]
# # #                 text_h = text_size[3] - text_size[1]

# # #                 bubble_x = x + 60
# # #                 bubble_y = y - text_h - 10

# # #                 draw.rectangle(
# # #                     [bubble_x - 8, bubble_y - 6, bubble_x + text_w + 8, bubble_y + text_h + 6],
# # #                     fill=(255, 255, 255, 220)
# # #                 )
# # #                 draw.text((bubble_x, bubble_y), text, fill=(0, 0, 0), font=font)
# # #                 break

# # #     background.save(output_path)
# # #     print(f"Scene {i+1} created: {output_path}")



# # from rembg import remove
# # from PIL import Image, ImageDraw, ImageFont
# # import io
# # import os
# # import re
# # import textwrap

# # # === Step 1: Remove backgrounds from character images ===
# # character_input_folder = "..\\Background\\characters"
# # character_output_folder = "transparent_characters" 

# # # Clear and recreate transparent character folder
# # if os.path.exists(character_output_folder):
# #     for file in os.listdir(character_output_folder):
# #         file_path = os.path.join(character_output_folder, file)
# #         if os.path.isfile(file_path):
# #             os.remove(file_path)
# # else:
# #     os.makedirs(character_output_folder)

# # # Remove backgrounds from character images
# # for filename in os.listdir(character_input_folder):
# #     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
# #         character_input_path = os.path.join(character_input_folder, filename)
# #         with open(character_input_path, "rb") as f:
# #             input_data = f.read()
# #             output_data = remove(input_data)    
# #         output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
# #         output_filename = os.path.splitext(filename)[0].split()[0].lower() + "_transparent.png"
# #         output_path = os.path.join(character_output_folder, output_filename)
# #         output_image.save(output_path)
# #         print(f"Processed: {filename} → {output_filename}")

# # # === Step 2: Parse comic script and generate scenes ===
# # script_path = "..\\Script\\comic_script.txt"
# # background_input_folder = "..\\Background\\images"
# # character_folder = "transparent_characters"
# # output_folder = "Pages"

# # # os.makedirs(output_folder, exist_ok=True)

# # # Load and parse the script
# # with open(script_path, "r") as file:
# #     content = file.read()

# # # Split the script into scenes using regex
# # scenes = re.findall(
# #     r'\d+\.\s*Scene Description: (.*?)\nCharacters Involved: (.*?)\nDialogues: (.*?)(?=\n\d+\.|$)',
# #     content,
# #     re.DOTALL
# # )

# # # Process each scene
# # for i, (scene_desc, character_line, dialogue_line) in enumerate(scenes):
# #     background_path = os.path.join(background_input_folder, f"panel_{i+1}.png")
# #     output_path = os.path.join(output_folder, f"scene_{i+1}.png")

# #     # Load background
# #     try:
# #         background = Image.open(background_path).convert("RGBA")
# #     except FileNotFoundError:
# #         print(f"Background panel_{i+1}.png not found. Skipping...")
# #         continue

# #     # Extract character names
# #     character_names = [name.strip().split()[0].lower() for name in character_line.split(",") if name.strip()]

# #     # Extract dialogues as name: line
# #     dialogues = []
# #     if dialogue_line.strip().lower() != "none":
# #         lines = [l.strip() for l in dialogue_line.split(",")]
# #         for l in lines:
# #             if ':' in l:
# #                 speaker, line = l.split(":", 1)
# #                 dialogues.append((speaker.strip().lower(), line.strip()))

# #     margin = 15
# #     positions = []

# #     for idx, name in enumerate(character_names[:2]):
# #         char_path = os.path.join(character_folder, f"{name}_transparent.png")
# #         if not os.path.exists(char_path):
# #             print(f"Character image not found: {char_path}")
# #             continue

# #         char_img = Image.open(char_path).convert("RGBA")
# #         char_img = char_img.resize((400, 500))

# #         if idx == 0:  # Bottom left
# #             pos = (10, background.height - char_img.height - margin)
# #         else:         # Bottom right
# #             pos = (background.width - char_img.width - margin, background.height - char_img.height - margin)

# #         # Paste the character with transparency (alpha channel)
# #         background.paste(char_img, pos, char_img)
# #         positions.append((name, pos))

# #     # Add dialogues above characters only if they exist
# #     if dialogues:
# #         draw = ImageDraw.Draw(background)
# #         try:
# #             font = ImageFont.truetype("arial.ttf", 27)
# #         except:
# #             font = ImageFont.load_default()

# #         for speaker, line in dialogues:
# #             for name, (x, y) in positions:
# #                 if name == speaker:
# #                     text = textwrap.fill(line, width=30)
# #                     text_size = draw.textbbox((0, 0), text, font=font)
# #                     text_w = text_size[2] - text_size[0]
# #                     text_h = text_size[3] - text_size[1]
                    
# #                     # Adjust positioning of the bubble
# #                     bubble_x = x + 60  # slight indent from character left
# #                     bubble_y = y - text_h - 15  # closer vertically
                    
# #                     # Draw the text bubble
# #                     draw.rectangle([bubble_x - 8, bubble_y - 6, bubble_x + text_w + 8, bubble_y + text_h + 6], fill=(255, 255, 255, 220))
# #                     draw.text((bubble_x, bubble_y), text, fill=(0, 0, 0), font=font)
# #                     break

# #     # Save the final image for the scene
# #     background.save(output_path)
# #     print(f"Scene {i+1} created: {output_path}")




from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import io
import os
import re
import textwrap

# === Step 1: Remove backgrounds from character images ===
character_input_folder = "..\Background\characters"
character_output_folder = "transparent_characters"

# Clear and recreate transparent character folder
if os.path.exists(character_output_folder):
    for file in os.listdir(character_output_folder):
        file_path = os.path.join(character_output_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
else:
    os.makedirs(character_output_folder)

# Remove backgrounds
for filename in os.listdir(character_input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        character_input_path = os.path.join(character_input_folder, filename)
        with open(character_input_path, "rb") as f:
            input_data = f.read()
            output_data = remove(input_data)
        output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
        output_filename = os.path.splitext(filename)[0].split()[0].lower() + "_transparent.png"
        output_path = os.path.join(character_output_folder, output_filename)
        output_image.save(output_path)
        print(f"Processed: {filename} → {output_filename}")

# === Step 2: Parse comic script and generate scenes ===
script_path = "..\\Script\\comic_script.txt"
background_input_folder = "..\\Background\\images"
character_folder = "transparent_characters"
output_folder = "Pages"
os.makedirs(output_folder, exist_ok=True)

# Load and parse script
with open(script_path, "r") as file:
    content = file.read()

# Regex to parse scenes with both Scene Description and Scene Explanation
scenes = re.findall(
    r'\d+\.\s*Scene Description: (.*?)\nScene Explanation: (.*?)\nCharacters Involved: (.*?)\nDialogues: (.*?)(?=\n\d+\.|$)',
    content,
    re.DOTALL
)

# === Step 3: Process each scene ===
for i, (scene_description, scene_explanation, character_line, dialogue_line) in enumerate(scenes):
    background_path = os.path.join(background_input_folder, f"panel_{i+1}.png")
    output_path = os.path.join(output_folder, f"scene_{i+1}.png")

    # Load original background
    try:
        original_bg = Image.open(background_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Background panel_{i+1}.png not found. Skipping...")
        continue

    # Prepare scene explanation text (instead of scene description)
    try:
        desc_font = ImageFont.truetype("arial.ttf", 28)
    except:
        desc_font = ImageFont.load_default()

    scene_text = textwrap.fill(scene_explanation.strip(), width=70)
    dummy_draw = ImageDraw.Draw(original_bg)
    text_bbox = dummy_draw.textbbox((0, 0), scene_text, font=desc_font)
    text_height = text_bbox[3] - text_bbox[1]
    padding = 20

    # Extend canvas to add scene explanation at top
    new_height = original_bg.height + text_height + padding * 2
    extended_bg = Image.new("RGBA", (original_bg.width, new_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(extended_bg)
    draw.rectangle([0, 0, extended_bg.width, text_height + padding * 2], fill=(255, 255, 255, 255))
    draw.text((padding, padding), scene_text, font=desc_font, fill=(0, 0, 0, 255))
    extended_bg.paste(original_bg, (0, text_height + padding * 2))
    background = extended_bg

        # Process characters
    character_names = [name.strip().split()[0].lower() for name in character_line.split(",") if name.strip()]
    dialogues = []
    if dialogue_line.strip().lower() != "none":
        lines = [l.strip() for l in dialogue_line.split(",")]
        for l in lines:
            if ':' in l:
                speaker, line = l.split(":", 1)
                dialogues.append((speaker.strip().lower(), line.strip()))

    margin = 15
    positions = []

    for idx, name in enumerate(character_names[:2]):
        char_path = os.path.join(character_folder, f"{name}_transparent.png")
        if not os.path.exists(char_path):
            print(f"Character image not found: {char_path}")
            continue

        char_img = Image.open(char_path).convert("RGBA")
        char_img = char_img.resize((400, 500))

        if idx == 0:  # Bottom left
            pos = (10, background.height - char_img.height - margin)
        else:         # Bottom right
            pos = (background.width - char_img.width - margin, background.height - char_img.height - margin)

        background.paste(char_img, pos, char_img)
        positions.append((name, pos))

    # Add dialogue bubbles
    try:
        font = ImageFont.truetype("arial.ttf", 27)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(background)
    for speaker, line in dialogues:
        for name, (x, y) in positions:
            if name == speaker:
                text = textwrap.fill(line, width=30)
                text_size = draw.textbbox((0, 0), text, font=font)
                text_w = text_size[2] - text_size[0]
                text_h = text_size[3] - text_size[1]

                bubble_x = x + 60
                bubble_y = y - text_h - 10

                draw.rectangle(
                    [bubble_x - 8, bubble_y - 6, bubble_x + text_w + 8, bubble_y + text_h + 6],
                    fill=(255, 255, 255, 220)
                )
                draw.text((bubble_x, bubble_y), text, fill=(0, 0, 0), font=font)
                break

    background.save(output_path)
    print(f"Scene {i+1} created: {output_path}")

