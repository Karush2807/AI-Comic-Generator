import re
import requests
import os
from dotenv import load_dotenv
import base64
import json
import time
from PIL import Image
import io

load_dotenv()

# Create directory for images if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Option 1: Using Hugging Face Inference API (free tier available)
# def generate_image_huggingface(prompt, output_path):
#     """Generate image using Hugging Face's free inference API"""
#     # You'll need to get a free token from huggingface.co
#     hf_token = os.getenv('HUGGINGFACE_API_KEY')
    
#     if not hf_token:
#         print("Error: Hugging Face API key not found. Please add it to your .env file.")
#         return False
    
#     API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
#     headers = {"Authorization": f"Bearer {hf_token}"}
    
#     # Improved prompt engineering for better results
#     enhanced_prompt = f"high quality, detailed illustration of {prompt}"
    
#     try:
#         response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
        
#         # If the model is loading, wait and retry
#         while response.status_code == 503:
#             print("Model is loading. Waiting for 10 seconds...")
#             time.sleep(10)
#             response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
        
#         # Check for successful response
#         if response.status_code == 200:
#             with open(output_path, 'wb') as file:
#                 file.write(response.content)
#             print(f"Image saved at {output_path}")
#             return True
#         else:
#             print(f"Error: {response.status_code}, {response.text}")
#             return False
#     except Exception as e:
#         print(f"Error during Hugging Face image generation: {str(e)}")
#         return False

# Option 2: Using Stable Diffusion through API
def generate_image_stability(prompt, output_path):
    """Generate image using Stability API's free tier"""
    stability_key = os.getenv('STABILITY_API_KEY')
    
    if not stability_key:
        print("Error: Stability API key not found. Please add it to your .env file.")
        return False
    
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {stability_key}"
    }
    
    body = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "steps": 30,
        "width": 1024,
        "height": 1024,
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code == 200:
            data = response.json()
            for i, image in enumerate(data["artifacts"]):
                img_data = base64.b64decode(image["base64"])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Image saved at {output_path}")
                return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"Error during Stability image generation: {str(e)}")
        return False

# Option 3: Using CraiYon (formerly DALL-E Mini) API
# def generate_image_craiyon(prompt, output_path):
#     """Generate image using Craiyon API (completely free, no key needed)"""
#     url = "https://api.craiyon.com/v3"
    
#     payload = {
#         "prompt": prompt,
#         "negative_prompt": "",
#         "model": "photo",  # Can be "photo", "drawing", or "pixel"
#         "version": "35s5hfwn9n78gb06"
#     }
    
#     try:
#         print(f"Generating image for: {prompt}")
        
#         # Make the initial request
#         response = requests.post(url, json=payload)
#         if response.status_code != 200:
#             print(f"Error: {response.status_code}, {response.text}")
#             return False
        
#         # Get submission ID
#         data = response.json()
#         submission_id = data.get("id")
#         if not submission_id:
#             print("Error: No submission ID returned")
#             return False
        
#         # Poll for results
#         get_url = f"https://api.craiyon.com/v3/{submission_id}"
#         max_attempts = 30
#         attempts = 0
        
#         while attempts < max_attempts:
#             time.sleep(2)  # Wait between polling attempts
#             attempts += 1
            
#             get_response = requests.get(get_url)
#             if get_response.status_code != 200:
#                 print(f"Error polling: {get_response.status_code}, {get_response.text}")
#                 continue
            
#             result = get_response.json()
#             if result.get("finished"):
#                 # Get the first image from the results
#                 images = result.get("images", [])
#                 if not images:
#                     print("No images generated")
#                     return False
                
#                 # Decode and save the first image
#                 img_data = base64.b64decode(images[0])
#                 with open(output_path, "wb") as f:
#                     f.write(img_data)
#                 print(f"Image saved at {output_path}")
#                 return True
            
#             print(f"Waiting for generation... (attempt {attempts}/{max_attempts})")
        
#         print("Timed out waiting for image generation")
#         return False
#     except Exception as e:
#         print(f"Error during Craiyon image generation: {str(e)}")
#         return False

def process_comic_script(script_path):
    """Process the comic script and generate images for each panel"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            comic_script = file.read()
    except Exception as e:
        print(f"Error reading script file: {str(e)}")
        return
    
    # Extract scene descriptions with improved regex pattern
    scene_description_pattern = re.compile(r"\*\*Panel (\d+)\*\*\s+- Scene Description: (.*?)(?=\s+-|\s+\*\*|\Z)", re.DOTALL)
    scenes = scene_description_pattern.findall(comic_script)
    
    if not scenes:
        print("No scene descriptions found in the script.")
        return
    
    print(f"Found {len(scenes)} panel descriptions.")
    
    # Choose which API to use - uncomment the one you prefer
    # generate_function = generate_image_craiyon  # Completely free, no key needed
    # generate_function = generate_image_huggingface  # Free tier with API key
    generate_function = generate_image_stability  # Free tier with API key
    
    # Process each scene
    for panel_num, scene in scenes:
        output_path = f"images/panel_{panel_num}.png"
        print(f"\nProcessing Panel {panel_num}:")
        print(f"Scene Description: {scene.strip()}")
        
        # Clean up the prompt
        clean_prompt = scene.strip()
        # Limit prompt length
        if len(clean_prompt) > 500:
            clean_prompt = clean_prompt[:500]
        
        # Generate the image
        success = generate_function(clean_prompt, output_path)
        
        if success:
            print(f"Successfully generated image for Panel {panel_num}")
        else:
            print(f"Failed to generate image for Panel {panel_num}")
        
        # Add a delay to avoid rate limiting
        time.sleep(2)

# Main execution
if __name__ == "__main__":
    script_path = "../Script/comic_script.txt"  # Path to your comic script
    process_comic_script(script_path)