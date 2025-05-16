import re
import requests
import os
from dotenv import load_dotenv
import replicate

load_dotenv()
# deepai_api_key = os.getenv('DEEPAI_API_KEY')
# hf_token = os.getenv('HUGGINGFACE_API_KEY')

replicate_token = os.getenv('REPLICATE_API_KEY')

# Initialize Replicate client
client = replicate.Client(api_token=replicate_token)

# Define the model you want to use (Stable Diffusion or another model)
model = client.models.get("stability-ai/stable-diffusion")

def generate_images(scene, output_path):
    # Define the input data for the Replicate model
    input_data = {
        "prompt": scene,
        "num_inference_steps": 50,  # Number of steps for better quality (you can adjust this)
        "seed": 42,  # Optional: Set seed for reproducibility
    }

    # Use replicate.run() to generate the image
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion",  # Model name
            input_data  # The input data for the model
        )
        
        # The model returns a list of image URLs, get the first one
        image_url = output[0]

        # Download the image from the generated URL
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as file:
            file.write(img_data)
        print(f"Image saved at {output_path}")
    except Exception as e:
        print(f"Error during image generation: {str(e)}")

if not os.path.exists("images"):
    os.makedirs("images")

with open("..\Script\comic_script.txt", "r") as file:
    comic_script = file.read()
    
scene_description_pattern = re.compile(r"\*\*Panel \d+\*\*\s+- Scene Description: (.*?)\s+-", re.DOTALL)

scene_descriptions = scene_description_pattern.findall(comic_script)

for i, scene in enumerate(scene_descriptions, 1):
    output_path = f"images/{i}.png"
    generate_images(scene.strip(), output_path)


# print(scene_descriptions)
# for scene in scene_descriptions:
#     print(f"Scene : {scene.strip()}")