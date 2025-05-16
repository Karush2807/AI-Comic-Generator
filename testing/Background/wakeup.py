# import os
# from dotenv import load_dotenv
# import replicate

# # Load environment variables from the .env file
# load_dotenv()

# # Get the API key from environment variables
# replicate_token = os.getenv('REPLICATE_API_KEY')

# # Ensure the API key is loaded correctly
# if not replicate_token:
#     print("Error: API key is not loaded correctly.")
# else:
#     print("API key loaded successfully.")

# # Initialize the Replicate client with the loaded API key
# client = replicate.Client(api_token=replicate_token)


import replicate
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # Get API key from the environment variable
# replicate_token = os.getenv('REPLICATE_API_KEY')

# if not replicate_token:
#     print("Error: API key is not loaded correctly.")
# else:
#     print("API key loaded successfully.")

# # Initialize Replicate client with the loaded API key
# client = replicate.Client(api_token=replicate_token)

# # Model version (replace with the actual model version you are using)
# model = client.models.get("stable-diffusion-v1")

# # Define the scene or input you want to pass to the model
# scene = "A beautiful sunset over a mountain range."

# # Run the model with your input scene
# try:
#     output = model.predict(
#         prompt=scene,
#         num_outputs=1  # Number of images you want to generate
#     )

#     # Assuming the model returns a URL to the generated image
#     img_url = output[0]
#     print("Generated image URL:", img_url)

#     # Download the image
#     img_data = requests.get(img_url).content
#     with open("output_image.png", 'wb') as file:
#         file.write(img_data)
#     print("Image saved successfully!")
# except Exception as e:
#     print(f"Error during image generation: {e}")



# import replicate
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Load the API key
# replicate_token = os.getenv('REPLICATE_API_KEY')

# if not replicate_token:
#     print("Error: API key not loaded correctly.")
# else:
#     print("API key loaded successfully.")

# # Initialize Replicate client
# client = replicate.Client(api_token=replicate_token)

# # Example test to make sure it's authenticated
# try:
#     # Try fetching model info to test the connection
#     model = client.models.get("pixray/text2image")
#     print("Successfully connected to Replicate model!")
# except Exception as e:
#     print(f"Error during connection: {e}")


import replicate
import os
import requests  # You missed importing this in your code

# Directly set environment variable for the API token
os.environ["REPLICATE_API_TOKEN"] = "r8_OtsTrsYmvgiZJEBirBYRfFICqziC9OI02dd4c"

print("API key loaded successfully.")

# Specify the model version ID
model_version = "pixray/text2image:5c347a4bfa1d4523a58ae614c2194e15f2ae682b57e3797a5bb468920aa70ebf"

def generate_image(scene_description, output_path):
    try:
        # Use replicate.run() directly — not via the client object
        output = replicate.run(
            model_version,
            input={
                "prompt": scene_description
            }
        )
        
        image_url = output[0]  # pixray usually returns a single image URL

        # Download and save the image
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as file:
            file.write(img_data)
        
        print(f"Image saved at {output_path}")
    
    except Exception as e:
        print(f"Error during image generation: {e}")

# Example usage
scene_description = "A futuristic city with flying cars and neon lights"
output_path = "generated_image.png"
generate_image(scene_description, output_path)
