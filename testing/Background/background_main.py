def process_comic_script(script_path):
    """Process the comic script and generate images for each panel and character"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            comic_script = file.read()
    except FileNotFoundError:
        print(f"Script file not found: {script_path}")
        script_path = input("Please enter the correct path to your comic script: ")
        try:
            with open(script_path, "r", encoding="utf-8") as file:
                comic_script = file.read()
        except Exception as e:
            print(f"Error reading script file: {str(e)}")
            return
    except Exception as e:
        print(f"Error reading script file: {str(e)}")
        return
    
    # Print the first 100 characters of the script to debug
    print(f"Script content preview: {comic_script[:100].strip()}...")
    
    # Try multiple patterns to extract scene descriptions, from most specific to most general
    
    # Pattern 1: Your specific format
    panel_pattern1
import re
import requests
import os
from dotenv import load_dotenv
import base64
import json
import time
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Create directories for images if they don't exist
os.makedirs("images", exist_ok=True)
os.makedirs("characters", exist_ok=True)

def generate_image_stability(prompt, output_path, retries=2):
    """Generate image using Stability API with retry mechanism"""
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
    
    for attempt in range(retries + 1):
        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for i, image in enumerate(data["artifacts"]):
                    img_data = base64.b64decode(image["base64"])
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    print(f"Image saved at {output_path}")
                    return True
            elif response.status_code == 429:  # Rate limit exceeded
                if attempt < retries:
                    wait_time = min(2 ** attempt * 5, 60)  # Exponential backoff
                    print(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Maximum retries reached. Rate limit still in effect.")
                    return False
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return False
        except Exception as e:
            print(f"Error during Stability image generation: {str(e)}")
            if attempt < retries:
                print(f"Retrying... (Attempt {attempt + 1}/{retries})")
                time.sleep(5)
            else:
                return False
    return False


def extract_unique_characters(script):
    """Extract unique character names from the comic script format with 'Characters Involved:' sections"""
    # Extract characters from the "Characters Involved:" sections
    characters_involved_pattern = re.compile(r"- Characters Involved:\s*(.*?)(?=\s+- Dialogues:|\s+\*\*|\Z)", re.DOTALL)
    characters_sections = characters_involved_pattern.findall(script)
    
    unique_characters = {}
    for section in characters_sections:
        # Split by commas or other common separators
        character_names = re.split(r',|\band\b', section)
        for name in character_names:
            name = name.strip()
            if name and name not in unique_characters:
                # Default description based on name (will be updated if found in scene descriptions)
                unique_characters[name] = f"character in comic, distinctive appearance"
    
    # Look for character descriptions in scene descriptions to enhance our information
    scene_desc_pattern = re.compile(r"- Scene Description:\s*(.*?)(?=\s+- Characters Involved:|\s+\*\*|\Z)", re.DOTALL)
    scene_descriptions = scene_desc_pattern.findall(script)
    
    # Extract character descriptions from scene descriptions
    for scene in scene_descriptions:
        for name in unique_characters.keys():
            # Look for descriptions near the character name
            desc_pattern = re.compile(f"{name},\\s*(?:a|an)\\s+(.*?)(?=\\.|\\,|\\s+\\w+\\s+is|\s+with\\s+|\\s+has\\s+|$)", re.IGNORECASE)
            desc_matches = desc_pattern.search(scene)
            if desc_matches:
                # Update character description with more specific information
                unique_characters[name] = desc_matches.group(1).strip()
            
            # Also look for physical descriptions
            phys_pattern = re.compile(f"{name}.*?(?:with|has)\\s+(.*?)(?=\\.|\\,|$)", re.IGNORECASE)
            phys_matches = phys_pattern.search(scene)
            if phys_matches:
                current_desc = unique_characters[name]
                physical_desc = phys_matches.group(1).strip()
                # Combine descriptions
                if "character in comic" in current_desc:
                    unique_characters[name] = physical_desc
                else:
                    unique_characters[name] = f"{current_desc}, {physical_desc}"
    
    return unique_characters


def generate_character_images(character_list):
    """Generate images for each unique character using Stability AI"""
    for name, description in character_list.items():
        print(f"\nGenerating image for {name}: {description}")
        
        # Create a more tailored prompt for character generation
        base_prompt = f"Full-body illustration of {name}, {description}, comic book art style"
        
        # Add style directives for better character images
        art_directives = ", dynamic pose, strong line art, detailed facial features, white background, centered composition, high contrast"
        prompt = base_prompt + art_directives
        
        output_path = f"characters/{name}.png"
        
        # Check if image already exists (to avoid unnecessary API calls)
        if os.path.exists(output_path):
            print(f"Image for {name} already exists. Skipping.")
            continue
        
        # Generate character image
        success = generate_image_stability(prompt, output_path)
        
        if success:
            print(f"Successfully generated image for {name}")
        else:
            print(f"Failed to generate image for {name}")
        
        # Add a delay to avoid rate limiting
        time.sleep(3)


def process_comic_script(script_path):
    """Process the comic script and generate images for each panel and character"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            comic_script = file.read()
    except FileNotFoundError:
        print(f"Script file not found: {script_path}")
        script_path = input("Please enter the correct path to your comic script: ")
        try:
            with open(script_path, "r", encoding="utf-8") as file:
                comic_script = file.read()
        except Exception as e:
            print(f"Error reading script file: {str(e)}")
            return
    except Exception as e:
        print(f"Error reading script file: {str(e)}")
        return
    
    # Print the first 100 characters of the script to debug
    print(f"Script content preview: {comic_script[:100].strip()}...")
    
    # Pattern for your specific format: "1. Scene Description: [description]Characters Involved: [characters]Dialogues: [dialogues]"
    panel_pattern = re.compile(r"(\d+)\.\s*Scene Description:\s*(.*?)Characters Involved:", re.DOTALL)
    scenes = panel_pattern.findall(comic_script)
    
    if not scenes:
        print("No scene descriptions found with the primary pattern. Trying alternative patterns...")
        
        # Try with more flexible spacing
        panel_pattern = re.compile(r"(\d+)\.?\s*Scene Description:?\s*(.*?)(?=Characters Involved:|Dialogues:|Character|Dialog|\d+\.|\Z)", re.DOTALL | re.IGNORECASE)
        scenes = panel_pattern.findall(comic_script)
    
    if not scenes:
        print("Still no scene descriptions found. Please provide a sample of your comic script format.")
        return
    
    print(f"Found {len(scenes)} panel descriptions.")
    
    # Extract character information with a pattern matching your format
    characters_pattern = re.compile(r"Characters Involved:\s*(.*?)(?=Dialogues:|Dialog|\d+\.|\Z)", re.DOTALL)
    characters_sections = characters_pattern.findall(comic_script)
    
    unique_characters = {}
    for section in characters_sections:
        # Look for character name with description in parentheses: "Lakshay (mountain climber)"
        char_desc_pattern = re.compile(r"(\w+)\s*\((.*?)\)", re.DOTALL)
        char_matches = char_desc_pattern.findall(section)
        
        for name, desc in char_matches:
            if name and name not in unique_characters:
                unique_characters[name] = desc.strip()
    
    # Do the same for character images - always regenerate them
    if unique_characters:
        print(f"Found {len(unique_characters)} unique characters:")
        for name, desc in unique_characters.items():
            print(f"- {name}: {desc}")
        
        # Generate character images (will now replace existing ones)
        for name, description in unique_characters.items():
            print(f"\nGenerating image for {name}: {description}")
            
            # Create a more tailored prompt for character generation
            base_prompt = f"Full-body illustration of {name}, {description}, comic book art style"
            
            # Add style directives for better character images
            art_directives = ", dynamic pose, strong line art, detailed facial features, white background, centered composition, high contrast"
            prompt = base_prompt + art_directives
            
            output_path = f"characters/{name}.png"
            
            # Generate character image (removed the existing file check)
            success = generate_image_stability(prompt, output_path)
            
            if success:
                print(f"Successfully generated image for {name}")
            else:
                print(f"Failed to generate image for {name}")
            
            # Add a delay to avoid rate limiting
            time.sleep(3)
    else:
        print("No character descriptions found in the script.")
    
    # Process each scene (background generation)
    for panel_num, scene in scenes:
        output_path = f"images/panel_{panel_num}.png"
        
        # Note: We've removed the check for existing files, so images will always be regenerated
        print(f"\nProcessing Panel {panel_num}:")
        print(f"Scene Description: {scene.strip()}")
        
        # Clean up the prompt
        clean_prompt = scene.strip()
        
        # Limit prompt length
        if len(clean_prompt) > 500:
            clean_prompt = clean_prompt[:500]
            print("Scene description truncated to 500 characters for API compatibility.")
        
        # Add comic style directive
        clean_prompt += ", comic book style illustration, detailed background, dramatic lighting, high quality"
        
        # Generate the image for the panel (background)
        success = generate_image_stability(clean_prompt, output_path)
        
        if success:
            print(f"Successfully generated image for Panel {panel_num}")
        else:
            print(f"Failed to generate image for Panel {panel_num}")
        
        # Add a delay to avoid rate limiting
        time.sleep(3)


# Main execution
if __name__ == "__main__":
    # Use the original path from your code as the default
    script_path = "../Script/comic_script.txt"
    
    # Check if the default path exists, otherwise prompt for input
    if not os.path.exists(script_path):
        script_path = input(f"Script file not found at {script_path}. Enter the correct path to your comic script: ")
    else:
        print(f"Comic script found at {script_path}")
    
    process_comic_script(script_path)
    print("\nImage generation complete! Check the 'images' and 'characters' folders.")
    print("Note: You may need to combine the background images with character images in an image editor to complete your comic panels.")