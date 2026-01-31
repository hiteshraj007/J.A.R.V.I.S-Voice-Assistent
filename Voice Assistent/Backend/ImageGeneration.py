
import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep


# add near top after imports
DATA_DIR = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\Data"
os.makedirs(DATA_DIR, exist_ok=True)

# Function to open and displly images based on a given prompt
# def open_images(prompt):
#     folder_path = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\Data" # Folder where the images are stored
#     prompt = prompt.replace(" ","_")
# # Replace spaces in prompt with underscores

# # Generate the filenames for the images
#     Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             # Try to open and display the image
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img. show( )
#             sleep(1)


#         except IOError:
#             print(f"Unable to open {image_path}")

def open_images(prompt):
    safe = prompt.replace(" ", "_")
    Files = [os.path.join(DATA_DIR, f"{safe}{i}.jpg") for i in range(1, 5)]
    for image_path in Files:
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")



# API details for the Hugging Face Stable Diffusion model
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}",
    "Accept": "image/png",
    "X-Use-Cache": "true",
    "X-Wait-For-Model": "true"
}


# Async function to send a query to the Hugging Face API
# async def query(payload):
#       response = await asyncio. to_thread(requests.post, API_URL, headers=headers, json=payload)
#       return response.content 
async def query(payload):
    # return full response so caller can check status_code
    resp = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload, timeout=120)
    return resp

async def generate_images(prompt: str):
     tasks = []

     # Create 4 image generation tasks
     for _ in range(2):
         payload = {
               "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
         }
         task = asyncio.create_task(query(payload))
         tasks.append(task)

     # Wait for all tasks to complete
    #  image_bytes_list = await asyncio.gather(*tasks)

    #  # Save the generated images to files
    #  for i, image_bytes in enumerate(image_bytes_list):
    #     safe_prompt = prompt.replace(" ", "_")
    #     with open(fr"Data\{safe_prompt}{i+1}.jpg", "wb") as f:

    #     # with open(fr"Data\{prompt.replace(" ","_")}{i+1}.jpg", "wb") as f:
    #         f.write(image_bytes)
    # Wait for all tasks to complete
     responses = await asyncio.gather(*tasks)

    # Save the generated images to files (only when response is OK)
     safe_prompt = prompt.replace(" ", "_")
     os.makedirs(DATA_DIR, exist_ok=True)

     for i, resp in enumerate(responses, start=1):
        if not hasattr(resp, "status_code"):
            print(f"Bad response object for image {i}: {resp}")
            continue

        if resp.status_code != 200:
            print(f"HuggingFace returned {resp.status_code} for image {i}. Preview: {getattr(resp, 'text', '')[:200]}")
            continue

        out_path = os.path.join(DATA_DIR, f"{safe_prompt}{i}.jpg")
        try:
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print("Saved:", out_path)
        except Exception as e:
            print("Failed saving image:", e)


# Wrapper function to generate and open images
def GenerateImages(prompt: str):
      asyncio.run(generate_images(prompt))
      open_images(prompt) # Open the generated images


# Main loop to monitor for image generation requests


while True:

   try:

       with open(r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

    #    Prompt, Status = Data.split(",")
       data = Data.split(",")
       Status = data[-1].strip()
       Prompt = " ".join(data[:-1]).strip()


       # If the status indicates an image generation request
       if Status == "True":
          print("Generating Images ... ")
          ImageStatus = GenerateImages(prompt=Prompt)

          # Reset the status in the file after generating images
          with open(r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data", "w") as f:
               f.write("False,False")
               break # Exit the loop after processing the request


       else:
           sleep(1)

# Wait for 1 second before checking again

   except :

       pass
