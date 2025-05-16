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
def generate_image_huggingface(prompt, output_path):
    """Generate image using Hugging Face's free inference API"""
    # You'll need to get a free token from huggingface.co
    hf_token = os.getenv('HUGGINGFACE_API_KEY')
    
    if not hf_token:
        print("Error: Hugging Face API key not found. Please add it to your .env file.")
        return False
    
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    # Improved prompt engineering for better results
    enhanced_prompt = f"high quality, detailed illustration of {prompt}"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
        
        # If the model is loading, wait and retry
        while response.status_code == 503:
            print("Model is loading. Waiting for 10 seconds...")
            time.sleep(10)
            response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
        
        # Check for successful response
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved at {output_path}")
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"Error during Hugging Face image generation: {str(e)}")
        return False

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
def generate_image_craiyon(prompt, output_path):
    """Generate image using Craiyon API (completely free, no key needed)"""
    url = "https://api.craiyon.com/v3"
    
    # Add proper headers to mimic a browser request - this helps bypass Cloudflare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.craiyon.com/",
        "Origin": "https://www.craiyon.com",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "low quality, blurry, distorted, disfigured, bad anatomy",
        "model": "drawing",  # Using "drawing" works better for comic panels
        "version": "35s5hfwn9n78gb06"
    }
    
    # Number of retries
    max_retries = 3
    current_retry = 0
    
    while current_retry < max_retries:
        try:
            print(f"Generating image with Craiyon (attempt {current_retry + 1}/{max_retries})...")
            print(f"Prompt: {prompt}")
            
            # Make the initial request with headers
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Handle common HTTP errors
            if response.status_code == 429:
                print("Rate limit reached. Waiting for 60 seconds before retrying...")
                time.sleep(60)
                current_retry += 1
                continue
                
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                # Try with different model on next attempt
                if current_retry + 1 < max_retries:
                    payload["model"] = "photo" if payload["model"] == "drawing" else "drawing"
                current_retry += 1
                time.sleep(15)  # Wait longer between retries
                continue
            
            # Get submission ID
            data = response.json()
            submission_id = data.get("id")
            if not submission_id:
                print("Error: No submission ID returned")
                current_retry += 1
                time.sleep(15)
                continue
            
            # Poll for results
            get_url = f"https://api.craiyon.com/v3/{submission_id}"
            max_poll_attempts = 40
            poll_attempts = 0
            
            while poll_attempts < max_poll_attempts:
                time.sleep(5)  # Wait between polling attempts
                poll_attempts += 1
                
                try:
                    get_response = requests.get(get_url, headers=headers, timeout=30)
                    
                    if get_response.status_code != 200:
                        print(f"Error polling: {get_response.status_code}")
                        # Wait longer if we hit an error
                        time.sleep(10)
                        continue
                    
                    result = get_response.json()
                    if result.get("finished"):
                        # Get the first image from the results
                        images = result.get("images", [])
                        if not images:
                            print("No images generated")
                            break
                        
                        # Decode and save the first image
                        try:
                            img_data = base64.b64decode(images[0])
                            with open(output_path, "wb") as f:
                                f.write(img_data)
                            print(f"Image saved at {output_path}")
                            return True
                        except Exception as e:
                            print(f"Error saving image: {str(e)}")
                            break
                    
                    print(f"Waiting for generation... (attempt {poll_attempts}/{max_poll_attempts})")
                    
                except Exception as e:
                    print(f"Error during polling: {str(e)}")
                    time.sleep(5)
                    continue
            
            # If we got here, polling either timed out or failed
            print("Failed to get image from Craiyon after multiple attempts")
            current_retry += 1
            
        except Exception as e:
            print(f"Error during Craiyon image generation: {str(e)}")
            current_retry += 1
            time.sleep(15)
    
    print("All Craiyon attempts failed")
    return False

def process_comic_script(script_path, start_panel=1):
    """Process the comic script and generate images for each panel"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            comic_script = file.read()
    except Exception as e:
        print(f"Error reading script file: {str(e)}")
        return
    
    # Try different regex patterns to extract scene descriptions
    patterns = [
        # Pattern 1: Standard format with Panel and Scene Description
        r"\*\*Panel (\d+)\*\*\s+- Scene Description: (.*?)(?=\s+-|\s+\*\*|\Z)",
        # Pattern 2: Alternative format that might be in the script
        r"Panel (\d+)[\s:]+(?:Scene Description:?)?\s*(.*?)(?=\s*Panel \d+|\Z)",
        # Pattern 3: Even more flexible pattern
        r"(?:Panel|PANEL) (\d+)[:\s]+(.*?)(?=(?:Panel|PANEL) \d+|\Z)"
    ]
    
    scenes = []
    for pattern in patterns:
        scenes = re.findall(pattern, comic_script, re.DOTALL)
        if scenes:
            print(f"Found {len(scenes)} panel descriptions using pattern.")
            break
    
    if not scenes:
        print("No scene descriptions found in the script. Trying a different approach...")
        # Fall back to manual parsing by lines
        lines = comic_script.split('\n')
        current_panel = None
        current_description = []
        
        for line in lines:
            panel_match = re.search(r"(?:Panel|PANEL)\s*(\d+)", line)
            if panel_match:
                # Save previous panel if exists
                if current_panel and current_description:
                    scenes.append((current_panel, ' '.join(current_description).strip()))
                    current_description = []
                
                current_panel = panel_match.group(1)
            elif current_panel and line.strip():
                current_description.append(line.strip())
        
        # Add the last panel
        if current_panel and current_description:
            scenes.append((current_panel, ' '.join(current_description).strip()))
    
    if not scenes:
        print("Still no scene descriptions found. Please check your script format.")
        return
    
    print(f"Found {len(scenes)} panel descriptions total.")
    
    # Function to try APIs in preferred order: Craiyon first, Hugging Face second
    def try_preferred_apis(prompt, output_path):
        # First try Craiyon (no API key needed)
        print("Attempting to generate with Craiyon...")
        if generate_image_craiyon(prompt, output_path):
            return True
        
        # Only try Hugging Face if Craiyon fails and API key is available
        hf_token = os.getenv('HUGGINGFACE_API_KEY')
        if hf_token:
            print("Craiyon failed. Attempting to generate with Hugging Face...")
            if generate_image_huggingface(prompt, output_path):
                return True
        
        # Skip Stability AI entirely as per user preference
        print("Both APIs failed to generate the image.")
        return False
    
    # Use the function with preferred API order
    generate_function = try_preferred_apis
    
    # Process each scene, starting from the specified panel
    for panel_num_str, scene in scenes:
        try:
            panel_num = int(panel_num_str)
            
            # Skip panels before the start_panel
            if panel_num < start_panel:
                print(f"Skipping Panel {panel_num} (starting from panel {start_panel})")
                continue
                
            output_path = f"images/panel_{panel_num}.png"
            
            # Check if the file already exists
            if os.path.exists(output_path):
                print(f"\nPanel {panel_num} image already exists at {output_path}")
                choice = input("Enter 'r' to regenerate, any other key to skip: ").lower()
                if choice != 'r':
                    print(f"Skipping Panel {panel_num}")
                    continue
            
            print(f"\nProcessing Panel {panel_num}:")
            print(f"Scene Description: {scene.strip()}")
            
            # Clean up the prompt
            clean_prompt = scene.strip()
            
            # Enhance the prompt for better image generation
            clean_prompt = f"comic panel illustration: {clean_prompt}"
            
            # Limit prompt length
            if len(clean_prompt) > 500:
                clean_prompt = clean_prompt[:500]
            
            # Generate the image
            success = generate_function(clean_prompt, output_path)
            
            if success:
                print(f"Successfully generated image for Panel {panel_num}")
                
                # Display the image if running in a Jupyter notebook or similar
                try:
                    from IPython.display import Image, display
                    display(Image(output_path))
                except ImportError:
                    pass  # Not running in an environment that supports display
            else:
                print(f"Failed to generate image for Panel {panel_num}")
                
                # Ask user if they want to retry
                choice = input("Enter 'r' to retry, any other key to continue: ").lower()
                if choice == 'r':
                    print("Retrying with different parameters...")
                    # Try with different parameters
                    alt_prompt = f"simple illustration of {clean_prompt}"
                    success = generate_function(alt_prompt, output_path)
                    if success:
                        print(f"Successfully generated image on retry for Panel {panel_num}")
            
            # Add a longer delay to avoid rate limiting
            print("Waiting before processing next panel to avoid rate limits...")
            time.sleep(10)
            
        except ValueError:
            print(f"Invalid panel number: {panel_num_str}, skipping")
            continue

# Main execution
if __name__ == "__main__":
    # Try to read the script path from the command line or use default
    import sys
    
    # Show welcome message
    print("=" * 80)
    print("Comic Panel Image Generator".center(80))
    print("=" * 80)
    print("This script will generate images for your comic panels using free text-to-image APIs.")
    print("You can choose which API to use or try them all in sequence.")
    print()
    
    # Get script path
    if len(sys.argv) > 1:
        script_path = sys.argv[1]
    else:
        default_path = "../Script/comic_script.txt"
        script_path = input(f"Enter path to comic script file [default: {default_path}]: ").strip()
        if not script_path:
            script_path = default_path
    
    print(f"Using script file: {script_path}")
    
    # Check if file exists
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at {script_path}")
        alternative = input("Enter alternative path or press Enter to exit: ").strip()
        if not alternative:
            sys.exit(1)
        script_path = alternative
        if not os.path.exists(script_path):
            print(f"Error: Script file not found at {script_path}")
            sys.exit(1)
    
    # Add an option to start from a specific panel
    start_panel = 1
    if len(sys.argv) > 2:
        try:
            start_panel = int(sys.argv[2])
        except ValueError:
            print("Invalid start panel number. Starting from panel 1.")
    else:
        try:
            panel_input = input("Start from panel number [default: 1]: ").strip()
            if panel_input:
                start_panel = int(panel_input)
        except ValueError:
            print("Invalid panel number. Starting from panel 1.")
    
    print(f"Starting from panel {start_panel}")
    
    # Check API keys
    hf_token = os.getenv('HUGGINGFACE_API_KEY')
    stability_key = os.getenv('STABILITY_API_KEY')
    
    print("\nAPI Status (in order of preference):")
    print(f"1. Craiyon API: Always available (no key required)")
    print(f"2. Hugging Face API: {'Available' if hf_token else 'Not configured'}")
    print(f"3. Stability API: {'Available but not used (as per your preference)' if stability_key else 'Not configured'}")
    
    if not hf_token:
        print("\nNote: Hugging Face API key not configured. Only Craiyon will be used.")
        print("If Craiyon fails, you won't have a fallback option.")
        print("For better results, add the Hugging Face API key to your .env file:")
        print("HUGGINGFACE_API_KEY=your_key_here")
        
        add_key = input("\nWould you like to add a Hugging Face API key now? (y/n): ").lower().strip()
        if add_key == 'y':
            hf_key = input("Enter Hugging Face API key: ").strip()
            if hf_key:
                os.environ['HUGGINGFACE_API_KEY'] = hf_key
                print("Hugging Face API key added for this session.")
    
    # Process the comic script
    print("\nStarting image generation...")
    process_comic_script(script_path, start_panel)