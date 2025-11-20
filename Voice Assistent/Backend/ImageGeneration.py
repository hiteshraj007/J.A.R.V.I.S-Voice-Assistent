# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# import os
# from time import sleep
# from requests.adapters import HTTPAdapter


# os.makedirs("Data", exist_ok=True)

# # Function to open and displly images based on a given prompt
# def open_images(prompt):
#     folder_path = r"Data" # Folder where the images are stored
#     prompt = prompt.replace(" ","_")
# # Replace spaces in prompt with underscores

# # Generate the filenames for the images
#     Files = [f"{prompt}{i}.png" for i in range(1, 5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             # Try to open and display the image
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)


#         except IOError:
#             print(f"Unable to open {image_path}")




# # API details for the Hugging Face Stable Diffusion model
# # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
# # API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
# # API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/sdxl-turbo"
# # API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
# API_URL = "https://api.deepai.org/api/text2img"
# DEEPAI_KEY = get_key('.env', 'DEEPAI_API_KEY')  # make sure your .env has this key

# headers = {
#     "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}",
#     "Accept": "image/png" ,  # add this 
#     "X-Use-Cache": "true",        # optional but helpful
#     "X-Wait-For-Model": "true" 
# }

# # Reuse TCP connection -> faster
# # session = requests.Session()
# # adapter = HTTPAdapter(pool_connections=4, pool_maxsize=4)
# # session.mount("https://", adapter)

# # Async function to send a query to the Hugging Face API
# # async def query(payload):
# #       response = await asyncio. to_thread(requests.post, API_URL, headers=headers, json=payload)
# #       return response.content 
# # Async function to send a query to the Hugging Face API
# async def query(payload):
#     # retry/backoff for 503/429
#     delay = 1.5
#     for attempt in range(1, 6):
#         resp = await asyncio.to_thread(
#             requests.post, API_URL, headers=headers, json=payload, timeout=120
#         )
#         ctype = resp.headers.get("content-type", "")
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype  # success: image bytes
#         # log error body (json/text) for debug
#         try:
#             body = resp.text[:300]
#         except Exception:
#             body = f"<{len(resp.content)} bytes>"
#         print(f"[HF] attempt {attempt}/5 failed: status={resp.status_code}, ctype={ctype}, body={body}")
#         if resp.status_code in (503, 429):
#             await asyncio.sleep(delay)
#             delay = min(delay * 1.8, 12)
#             continue
#         await asyncio.sleep(1.0)
#     # last try (may still be error)
#     resp = await asyncio.to_thread(
#         requests.post, API_URL, headers=headers, json=payload, timeout=120
#     )
#     ctype = resp.headers.get("content-type", "")
#     if resp.status_code == 200 and "image" in ctype:
#         return resp.content, ctype
#     raise RuntimeError(f"HF failed after retries. status={resp.status_code}, ctype={ctype}, body={resp.text[:300]}")

# async def query(payload):
#     delay = 1.0
#     for attempt in range(1, 5):
#         resp = await asyncio.to_thread(
#             session.post, API_URL, headers=headers, json=payload, timeout=60
#         )
#         ctype = resp.headers.get("content-type", "")
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype

#         if resp.status_code == 403:
#             raise RuntimeError("HF 403: token me Serverless Inference permission/billing missing.")
#         if resp.status_code == 410:
#             raise RuntimeError("HF 410: use router.huggingface.co endpoint (already set).")

#         # Transient: 429/503 retry
#         if resp.status_code in (429, 503):
#             await asyncio.sleep(delay)
#             delay = min(delay * 1.7, 8)
#             continue

#         # log other
#         try:
#             print(f"[HF] status={resp.status_code}, body={resp.text[:200]}")
#         except:
#             pass
#         await asyncio.sleep(0.5)
#     raise RuntimeError("HF failed after retries.")
# async def query(payload):
#     delay = 0.8
#     for attempt in range(1, 5):
#         resp = await asyncio.to_thread(
#             requests.post, API_URL, headers=headers, json=payload, timeout=60
#         )
#         ctype = resp.headers.get("content-type", "")
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype
#         if resp.status_code == 403:
#             raise RuntimeError("HF 403: token lacks Serverless Inference/billing.")
#         if resp.status_code in (429, 503):
#             await asyncio.sleep(delay); delay = min(delay*1.7, 8); continue
#         await asyncio.sleep(0.5)
#     raise RuntimeError("HF failed after retries.")

# async def generate_images(prompt: str):
#      tasks = []

#      # Create 4 image generation tasks
#      for _ in range(4):
#          payload = {
#                "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
#          }
#          task = asyncio.create_task(query(payload))
#          tasks.append(task)

#      # Wait for all tasks to complete
#      image_bytes_list = await asyncio.gather(*tasks)

#     #  # Save the generated images to files
#     #  for i, image_bytes in enumerate(image_bytes_list):
#     #         safe = prompt.strip().replace(" ", "_")
#     #         with open(fr"Data\{safe}{i+1}.png", "wb") as f:

#     #     # with open(fr"Data\{prompt.replace('','_')}{i+1}.jpg", "wb") as f:
#     #              f.write(image_bytes)
#      safe = prompt.strip().replace(" ", "_")

#      for i, res in enumerate(image_bytes_list, start=1):
#         out_path = fr"Data\{safe}{i}.png"  # PNG me save karna (Accept:image/png)

#         # res may be exception if API failed
#         if isinstance(res, Exception):
#             print(f"[Save] Query exception for {out_path}: {res}")
#             continue

#         image_bytes, ctype = res
#         if "image" not in ctype:
#             print(f"[Save] Not an image for {out_path}. Response was text/JSON.")
#             continue

#         with open(out_path, "wb") as f:
#             f.write(image_bytes)

#         print(f"Saved: {out_path}")
# async def generate_images(prompt: str):
#     # Concurrency limit (2 better with router)
#     sem = asyncio.Semaphore(2)

#     async def one_job(seed: int):
#         payload = {
#             "inputs": f"{prompt}",
#             # Turbo ko low steps chahiye; 512x512 fastest
#             "parameters": {
#                 "num_inference_steps": 6,     # 4–8 fast
#                 "guidance_scale": 1.5,        # turbo ke liye low
#                 "width": 512,
#                 "height": 512,
#                 "seed": seed
#             }
#         }
#         async with sem:
#             return await query(payload)

#     # 2–4 images; 2 very fast, 4 thoda zyada time
#     jobs = [asyncio.create_task(one_job(randint(0, 1_000_000))) for _ in range(2)]
#     results = await asyncio.gather(*jobs, return_exceptions=True)

#     safe = prompt.strip().replace(" ", "_")
#     os.makedirs("Data", exist_ok=True)

#     for i, res in enumerate(results, start=1):
#         out_path = fr"Data\{safe}{i}.png"
#         if isinstance(res, Exception):
#             print(f"[Save] skip {out_path} -> {res}")
#             continue
#         image_bytes, ctype = res
#         if "image" not in ctype:
#             try:
#                 print(f"[Save] not image -> {image_bytes[:150].decode('utf-8','ignore')}")
#             except:
#                 print(f"[Save] not image ({len(image_bytes)} bytes)")
#             continue
#         with open(out_path, "wb") as f:
#             f.write(image_bytes)
#         print(f"Saved: {out_path}")

# async def generate_images(prompt: str):
#     # fastest: 2 images, 512x512
#     async def one_job(seed: int):
#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "width": 512, "height": 512,
#                 "num_inference_steps": 6,   # 4–8 fast
#                 "guidance_scale": 1.5,
#                 "seed": seed
#             }
#         }
#         return await query(payload)

#     tasks = [asyncio.create_task(one_job(randint(0, 1_000_000))) for _ in range(2)]
#     results = await asyncio.gather(*tasks, return_exceptions=True)

#     safe = prompt.strip().replace(" ", "_")
#     for i, res in enumerate(results, start=1):
#         out = fr"Data\{safe}{i}.png"
#         if isinstance(res, Exception): print(f"[Save] skip {out} -> {res}"); continue
#         img_bytes, ctype = res
#         if "image" not in ctype: print(f"[Save] not image: {ctype}"); continue
#         with open(out, "wb") as f: f.write(img_bytes)
#         print(f"Saved: {out}")

# # Wrapper function to generate and open images
# def GenerateImages(prompt: str):
#       asyncio.run(generate_images(prompt))
#       open_images(prompt) # Open the generated images


# # Main loop to monitor for image generation requests


# while True:

#    try:

#        with open(r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Fronted/Files/ImageGeneration.data", "r",encoding="utf-8") as f:
#             Data: str = f.read()

#     #    Prompt, Status = Data.split(",")
#        Prompt, Status = [x.strip() for x in Data.split(",", 1)]


#        # If the status indicates an image generation request
#        if Status == "True":
#           print("Generating Images ... ")
#           ImageStatus = GenerateImages(prompt=Prompt)

#           # Reset the status in the file after generating images
#           with open(r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Fronted/Files/ImageGeneration.data", "w",encoding="utf-8") as f:
#                f.write("False,False")
#                break # Exit the loop after processing the request


#        else:
#            sleep(1)

# # Wait for 1 second before checking again

#    except Exception as e:
#        print(f"Loop error: {e}")
#        sleep(1)


# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# import os
# from time import sleep

# # Function to open and displly images based on a given prompt
# def open_images(prompt):
#     folder_path = r"Data" # Folder where the images are stored
#     prompt = prompt.replace(" ","_")
# # Replace spaces in prompt with underscores

# # Generate the filenames for the images
#     # Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
#     Files = [f"{prompt}{i}.png" for i in range(1, 5)]


#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             # Try to open and display the image
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show( )
#             sleep(1)


#         except IOError:
#             print(f"Unable to open {image_path}")




# # API details for the Hugging Face Stable Diffusion model
# # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
# API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
# # API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"


# headers = {
#     "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}",
#     "Accept": "image/png",
#     "X-Use-Cache": "true",
#     "X-Wait-For-Model": "true"
# }



# # Async function to send a query to the Hugging Face API
# # async def query(payload):
# #       response = await asyncio. to_thread(requests.post, API_URL, headers=headers, json=payload)
# #       return response.content 
# async def query(payload):
#     delay = 0.9
#     for attempt in range(1, 5):
#         resp = await asyncio.to_thread(
#             requests.post, API_URL, headers=headers, json=payload, timeout=60
#         )
#         ctype = resp.headers.get("content-type", "")
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype

#         if resp.status_code == 403:
#             raise RuntimeError("HF 403: token me Serverless Inference permission/billing missing.")
#         if resp.status_code == 410:
#             raise RuntimeError("HF 410: old endpoint; router already set.")

#         if resp.status_code in (429, 503):
#             await asyncio.sleep(delay); delay = min(delay*1.7, 8); continue

#         try:
#             print(f"[HF] status={resp.status_code}, ctype={ctype}, body={resp.text[:200]}")
#         except Exception:
#             pass
#         await asyncio.sleep(0.5)
#     raise RuntimeError("HF failed after retries.")


# async def generate_images(prompt: str):
#      tasks = []

#      # Create 4 image generation tasks
#      for _ in range(4):
#          payload = {
#                "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
#          }
#          task = asyncio.create_task(query(payload))
#          tasks.append(task)

#      # Wait for all tasks to complete
#      image_bytes_list = await asyncio.gather(*tasks)

#      # Save the generated images to files
#     #  for i, image_bytes in enumerate(image_bytes_list):
#     #     # with open(fr"Data\{prompt.replace('','_')}{i+1}.jpg", "wb") as f:
#     #     safe = prompt.strip().replace(" ", "_")
#     #     with open(fr"Data\{safe}{i+1}.png", "wb") as f:
#     #         f.write(image_bytes)
#      safe = prompt.strip().replace(" ", "_")
#      for i, res in enumerate(image_bytes_list, start=1):
#         out_path = fr"Data\{safe}{i}.png"
#         if isinstance(res, Exception):
#             print(f"[Save] Query exception for {out_path}: {res}")
#             continue
#         image_bytes, ctype = res
#         if "image" not in ctype:
#             print(f"[Save] Not an image for {out_path}.")
#             continue
#         with open(out_path, "wb") as f:
#             f.write(image_bytes)
#         print(f"Saved: {out_path}")


# # Wrapper function to generate and open images
# def GenerateImages(prompt: str):
#       asyncio.run(generate_images(prompt))
#       open_images(prompt) # Open the generated images


# # Main loop to monitor for image generation requests


# while True:

#    try:

#        with open(r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Files/ImageGeneration.data", "r") as f:
#             Data: str = f.read()

#        Prompt, Status = Data.split(",")

#        # If the status indicates an image generation request
#        if Status == "True":
#           print("Generating Images ... ")
#           ImageStatus = GenerateImages(prompt=Prompt)

#           # Reset the status in the file after generating images
#           with open(r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Files/ImageGeneration.data", "w") as f:
#                f.write("False,False")
#                break # Exit the loop after processing the request


#        else:
#            sleep(1)

# # Wait for 1 second before checking again

#    except :
#        pass


# # ---------- FREE LOCAL IMAGE GENERATION (no API/credits) ----------
# import os, asyncio
# from time import sleep
# from random import randint
# from glob import glob
# from typing import Tuple

# from PIL import Image
# import torch
# from diffusers import AutoPipelineForText2Image

# # Paths (same Jarvis flow)
# DATA_DIR = "Data"
# FLAG_FILE = r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Files/ImageGeneration.data"
# os.makedirs(DATA_DIR, exist_ok=True)

# # --------- Pick model (fastest first) ----------
# # 1) SDXL-TURBO = fastest draft quality
# # MODEL_ID = "stabilityai/sdxl-turbo"
# MODEL_ID = "runwayml/stable-diffusion-v1-5"

# # If VRAM low or OOM, try: MODEL_ID = "runwayml/stable-diffusion-v1-5"

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# DTYPE  = torch.float16 if DEVICE == "cuda" else torch.float32

# # Load pipeline once
# print(f"[Local] Loading model: {MODEL_ID} on {DEVICE} ({DTYPE}) ...")
# pipe = AutoPipelineForText2Image.from_pretrained(
#     MODEL_ID,
#     torch_dtype=DTYPE,
#     safety_checker=None
# )
# pipe.to(DEVICE)
# pipe.disable_attention_slicing()  # good default; xformers auto-used if installed
# print("[Local] Model ready.")

# # ---------- helpers ----------
# def sanitize_prompt(p: str) -> str:
#     p = p.strip().replace(" ", "_")
#     return "".join(c for c in p if c.isalnum() or c in ("_", "-", "."))[:80] or "image"

# def save_png(img: Image.Image, base: str, idx: int) -> str:
#     out = os.path.join(DATA_DIR, f"{base}{idx}.png")
#     img.save(out)
#     print(f"Saved: {out}")
#     return out

# def open_images_for_prompt(prompt: str):
#     base = sanitize_prompt(prompt)
#     files = sorted(glob(os.path.join(DATA_DIR, f"{base}*.png")))
#     if not files:
#         print("[Open] No images found.")
#         return
#     for p in files:
#         try:
#             im = Image.open(p)
#             print(f"Opening image: {p}")
#             im.show()
#             sleep(0.8)
#         except Exception as e:  
#             print(f"Unable to open {p}: {e}")

# # ---------- core local generation ----------
# def generate_local(prompt: str, n_images: int = 2, w: int = 512, h: int = 512) -> int:
#     """
#     Returns number of images saved. Uses SDXL-Turbo defaults (very fast).
#     """
#     base = sanitize_prompt(prompt)
#     saved = 0
#     for i in range(1, n_images + 1):
#         seed = randint(0, 1_000_000)
#         gen = torch.Generator(device=DEVICE).manual_seed(seed)

#         # SDXL-Turbo likes very low steps & guidance ~0–1.5
#         result = pipe(
#             prompt,
#             num_inference_steps=6,     # 4–8 fast
#             guidance_scale=1.0,        # low guidance for turbo
#             width=w, height=h,
#             generator=gen
#         )
#         img = result.images[0]
#         save_png(img, base, i)
#         saved += 1
#     return saved

# # ---------- async wrapper to match your old flow ----------
# async def generate_images(prompt: str):
#     return generate_local(prompt, n_images=2, w=512, h=512)

# def GenerateImages(prompt: str):
#     try:
#         saved = asyncio.run(generate_images(prompt))
#         if saved:
#             open_images_for_prompt(prompt)
#         else:
#             print("[Local] Nothing saved.")
#     except Exception as e:
#         print(f"[Local] Generation error: {e}")

# # ---------- watcher loop (same contract) ----------
# while True:
#     try:
#         with open(FLAG_FILE, "r", encoding="utf-8") as f:
#             data = f.read().strip()
#         try:
#             Prompt, Status = [x.strip() for x in data.split(",", 1)]
#         except ValueError:
#             sleep(1); continue

#         if Status == "True":
#             print("Generating Images (LOCAL) ...")
#             GenerateImages(Prompt)
#             with open(FLAG_FILE, "w", encoding="utf-8") as f:
#                 f.write("False,False")
#             break
#         else:
#             sleep(1)

#     except FileNotFoundError:
#         # init file if missing
#         os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
#         with open(FLAG_FILE, "w", encoding="utf-8") as f:
#             f.write("False,False")
#         sleep(1)
#     except Exception as e:
#         print(f"[Watcher] {e}")
#         sleep(1)
# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import get_key
# import os
# from time import sleep

# os.makedirs("Data", exist_ok=True)

# # --------- helper: open and display images ----------
# def open_images(prompt):
#     folder_path = r"Data"
#     safe = prompt.replace(" ", "_")
#     Files = [f"{safe}{i}.png" for i in range(1, 5)]
#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)
#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)
#         except IOError:
#             print(f"Unable to open {image_path}")

# # --------- DeepAI endpoint & headers ----------
# API_URL = "https://api.deepai.org/api/text2img"
# DEEPAI_KEY = get_key('.env', 'DEEPAI_API_KEY')  # make sure your .env has this key

# if not DEEPAI_KEY:
#     raise RuntimeError("DEEPAI_API_KEY not found in .env")

# HEADERS = {
#     "api-key": DEEPAI_KEY
# }

# # --------- async query to DeepAI (post text, then download returned image url) ----------
# async def query_deepai(prompt_text: str):
#     """
#     Send prompt to DeepAI and download image bytes.
#     Returns: (bytes, content_type) on success or raises Exception.
#     """
#     # DeepAI sometimes needs a small backoff for rate-limits; implement retries.
#     delay = 1.0
#     for attempt in range(1, 6):
#         try:
#             # POST to DeepAI with form data 'text'
#             resp = await asyncio.to_thread(
#                 requests.post,
#                 API_URL,
#                 headers=HEADERS,
#                 data={"text": prompt_text},
#                 timeout=60
#             )
#         except Exception as e:
#             print(f"[DeepAI] network error attempt {attempt}: {e}")
#             await asyncio.sleep(delay)
#             delay = min(delay * 1.8, 10)
#             continue

#         # DeepAI usually returns JSON with field 'output_url'
#         if resp.status_code == 200:
#             try:
#                 j = resp.json()
#             except Exception:
#                 j = None
#             # Try common keys
#             img_url = None
#             if isinstance(j, dict):
#                 img_url = j.get("output_url") or j.get("output", None)
#                 # Sometimes output could be list/dict; handle loosely
#                 if isinstance(img_url, list) and img_url:
#                     img_url = img_url[0]
#             if not img_url:
#                 # If JSON didn't include URL, print and retry (or return error)
#                 body = resp.text[:300]
#                 print(f"[DeepAI] 200 but no image url in response: {body}")
#                 # try small wait and retry
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 10)
#                 continue

#             # Download the image bytes from the returned URL
#             try:
#                 img_resp = await asyncio.to_thread(requests.get, img_url, timeout=60)
#                 img_resp.raise_for_status()
#                 ctype = img_resp.headers.get("content-type", "image")
#                 return img_resp.content, ctype
#             except Exception as e:
#                 print(f"[DeepAI] failed to download image: {e}")
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 10)
#                 continue

#         else:
#             # handle rate limits / server errors
#             print(f"[DeepAI] status={resp.status_code}, body={resp.text[:300]}")
#             if resp.status_code in (429, 503, 502):
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 10)
#                 continue
#             # other statuses: break/raise
#             raise RuntimeError(f"DeepAI error: status={resp.status_code}, body={resp.text[:400]}")

#     raise RuntimeError("DeepAI failed after retries.")

# # --------- generate multiple images concurrently ----------
# async def generate_images(prompt: str, count: int = 4):
#     tasks = []
#     # Slightly vary prompt by adding small seed/instruction so outputs differ
#     for i in range(count):
#         seed = randint(0, 999999)
#         # keep prompt concise for DeepAI; appended seed to diversify
#         final_prompt = f"{prompt} -- ultra-detailed, high resolution -- seed:{seed}"
#         tasks.append(asyncio.create_task(query_deepai(final_prompt)))

#     results = await asyncio.gather(*tasks, return_exceptions=True)

#     # save results
#     safe = prompt.strip().replace(" ", "_")
#     for idx, res in enumerate(results, start=1):
#         out_path = os.path.join("Data", f"{safe}{idx}.png")
#         if isinstance(res, Exception):
#             print(f"[Save] Query exception for {out_path}: {res}")
#             continue
#         image_bytes, ctype = res
#         if "image" not in ctype:
#             print(f"[Save] Not an image for {out_path}, content-type={ctype}")
#             continue
#         with open(out_path, "wb") as f:
#             f.write(image_bytes)
#         print(f"Saved: {out_path}")

# def GenerateImages(prompt: str):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# # --------- main loop reading the ImageGeneration.data file ----------
# WATCH_FILE = r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Fronted/Files/ImageGeneration.data"

# while True:
#     try:
#         with open(WATCH_FILE, "r", encoding="utf-8") as f:
#             Data: str = f.read()
#         # Expecting "Prompt,True" or "Prompt,False"
#         Prompt, Status = [x.strip() for x in Data.split(",", 1)]
#         if Status == "True":
#             print("Generating Images ... ")
#             GenerateImages(prompt=Prompt)
#             # Reset status
#             with open(WATCH_FILE, "w", encoding="utf-8") as f:
#                 f.write("False,False")
#             break  # exit after processing one request
#         else:
#             sleep(1)
#     except Exception as e:
#         print(f"Loop error: {e}")
#         sleep(1)
# image_gen_hf.py
# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import load_dotenv
# import os
# from time import sleep
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # load .env (make sure python-dotenv is installed)
# load_dotenv(".env")

# os.makedirs("Data", exist_ok=True)

# # -------- config ----------
# # Use the router endpoint (recommended)
# API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
# HF_KEY = os.environ.get("HuggingFaceAPIKey") or os.environ.get("HUGGINGFACE_API_KEY")

# HEADERS = {
#     "Authorization": f"Bearer {HF_KEY}",
#     "Accept": "image/png",
#     "X-Use-Cache": "true",
#     "X-Wait-For-Model": "true",
# }

# # requests session with retries for robustness
# session = requests.Session()
# retries = Retry(total=3, backoff_factor=0.8, status_forcelist=(429, 502, 503, 504))
# adapter = HTTPAdapter(max_retries=retries, pool_connections=4, pool_maxsize=8)
# session.mount("https://", adapter)
# session.mount("http://", adapter)

# # -------- helper: open and display images ----------
# def open_images(prompt):
#     folder_path = "Data"
#     safe = prompt.replace(" ", "_")
#     Files = [f"{safe}{i}.png" for i in range(1, 5)]
#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)
#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)
#         except IOError:
#             print(f"Unable to open {image_path}")

# # -------- async query to Hugging Face (single request) ----------
# async def query_hf(payload):
#     """
#     Send payload to HF router and return (bytes, content-type).
#     Raises RuntimeError on unrecoverable errors.
#     """
#     delay = 1.0
#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             resp = await asyncio.to_thread(session.post, API_URL, headers=HEADERS, json=payload, timeout=120)
#         except Exception as e:
#             print(f"[HF] network error attempt {attempt}: {e}")
#             if attempt < max_attempts:
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 12)
#                 continue
#             raise RuntimeError(f"Network failure: {e}")

#         ctype = resp.headers.get("content-type", "")
#         # success: image
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype

#         # specific helpful errors
#         if resp.status_code == 403:
#             raise RuntimeError("HF 403: token lacks inference permission or billing required.")
#         if resp.status_code == 410:
#             raise RuntimeError("HF 410: old endpoint; use router.huggingface.co")

#         # transient errors -> retry
#         body_preview = resp.text[:300]
#         print(f"[HF] attempt {attempt} failed: status={resp.status_code}, ctype={ctype}, body={body_preview}")
#         if resp.status_code in (429, 502, 503, 504):
#             if attempt < max_attempts:
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 12)
#                 continue
#             else:
#                 raise RuntimeError(f"Transient HF error after retries: status={resp.status_code}")

#         # other non-retriable statuses -> raise
#         raise RuntimeError(f"HF error: status={resp.status_code}, body={body_preview}")

#     raise RuntimeError("HF failed after retries.")

# # -------- generate multiple images with concurrency limit ----------
# # async def generate_images_async(prompt: str, count: int = 4, concurrency: int = 2):
# async def generate_images_async(prompt: str, count: int = 3, concurrency: int = 2):

#     sem = asyncio.Semaphore(concurrency)

#     async def one_job(seed: int, idx: int):
#         final_prompt = f"{prompt} -- ultra-detailed, high resolution -- seed:{seed}"
#         payload = {
#             "inputs": final_prompt,
#             "parameters": {
#                 "width": 1024,            # HF SDXL supports larger sizes; change if needed
#                 "height": 1024,
#                 # you can add model-specific parameters if supported by the endpoint
#             }
#         }
#         async with sem:
#             try:
#                 return await query_hf(payload)
#             except Exception as e:
#                 return e

#     jobs = [asyncio.create_task(one_job(randint(0, 999_999), i)) for i in range(count)]
#     results = await asyncio.gather(*jobs, return_exceptions=False)
#     safe = prompt.strip().replace(" ", "_")
#     saved = []
#     for i, res in enumerate(results, start=1):
#         out_path = os.path.join("Data", f"{safe}{i}.png")
#         if isinstance(res, Exception):
#             print(f"[Save] Query exception for {out_path}: {res}")
#             continue
#         image_bytes, ctype = res
#         if "image" not in ctype:
#             print(f"[Save] Not an image for {out_path}, content-type={ctype}")
#             continue
#         with open(out_path, "wb") as f:
#             f.write(image_bytes)
#         print(f"Saved: {out_path}")
#         saved.append(out_path)
#     return saved

# def GenerateImages(prompt: str):
#     if not HF_KEY:
#         print("HuggingFace API key not found in environment. Set HuggingFaceAPIKey in your .env")
#         return
#     asyncio.run(generate_images_async(prompt))
#     open_images(prompt)

# # -------- main loop: monitor file for prompt requests ----------
# WATCH_FILE = r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Fronted/Files/ImageGeneration.data"

# while True:
#     try:
#         with open(WATCH_FILE, "r", encoding="utf-8") as f:
#             Data = f.read()
#         # Expecting "Prompt,True" or "Prompt,False"
#         Prompt, Status = [x.strip() for x in Data.split(",", 1)]
#         if Status == "True":
#             print("Generating Images ... ")
#             GenerateImages(prompt=Prompt)
#             # Reset status
#             with open(WATCH_FILE, "w", encoding="utf-8") as f:
#                 f.write("False,False")
#             break  # exit after processing one request
#         else:
#             sleep(1)
#     except Exception as e:
#         print(f"Loop error: {e}")
#         sleep(1)
# Backend/ImageGeneration.py
# import asyncio
# from random import randint
# from PIL import Image
# import requests
# from dotenv import load_dotenv
# import os
# from time import sleep
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import sys

# # load .env from project root (adjust if needed)
# load_dotenv(".env")

# # Ensure Data folder exists
# os.makedirs("Data", exist_ok=True)

# # -------- config ----------
# API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
# HF_KEY = os.environ.get("HuggingFaceAPIKey") or os.environ.get("HUGGINGFACE_API_KEY")

# HEADERS = {"Accept": "image/png"}
# if HF_KEY:
#     HEADERS["Authorization"] = f"Bearer {HF_KEY}"

# # requests session with retries for robustness
# session = requests.Session()
# retries = Retry(total=3, backoff_factor=0.8, status_forcelist=(429, 502, 503, 504))
# adapter = HTTPAdapter(max_retries=retries, pool_connections=4, pool_maxsize=8)
# session.mount("https://", adapter)
# session.mount("http://", adapter)

# # -------- helper: open and display images ----------
# def open_images(prompt, count=3):
#     folder_path = "Data"
#     safe = prompt.strip().replace(" ", "_")
#     Files = [f"{safe}{i}.png" for i in range(1, count + 1)]
#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)
#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)
#         except IOError:
#             print(f"Unable to open {image_path}")

# # -------- async query to Hugging Face (single request) ----------
# async def query_hf(payload):
#     """
#     Send payload to HF router and return (bytes, content-type).
#     Raises RuntimeError on unrecoverable errors.
#     """
#     if not HF_KEY:
#         raise RuntimeError("HuggingFace API key not set. Put HuggingFaceAPIKey=hf_xxx in .env")

#     delay = 1.0
#     max_attempts = 5
#     for attempt in range(1, max_attempts + 1):
#         try:
#             # use session.post inside a thread to avoid blocking
#             resp = await asyncio.to_thread(session.post, API_URL, headers=HEADERS, json=payload, timeout=120)
#         except Exception as e:
#             print(f"[HF] network error attempt {attempt}: {e}")
#             if attempt < max_attempts:
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 12)
#                 continue
#             raise RuntimeError(f"Network failure: {e}")

#         ctype = resp.headers.get("content-type", "")
#         if resp.status_code == 200 and "image" in ctype:
#             return resp.content, ctype

#         # helpful debugging output
#         body_preview = resp.text[:800]
#         print(f"[HF] attempt {attempt} failed: status={resp.status_code}, ctype={ctype}, body_preview={body_preview}")

#         # common actionable errors
#         if resp.status_code == 401:
#             raise RuntimeError("HF 401: Unauthorized — check your HuggingFaceAPIKey.")
#         if resp.status_code == 403:
#             raise RuntimeError("HF 403: Forbidden — token lacks 'Make calls to Inference Providers' permission or billing required.")
#         if resp.status_code == 410:
#             raise RuntimeError("HF 410: old endpoint; use router.huggingface.co")
#         if resp.status_code in (429, 502, 503, 504):
#             if attempt < max_attempts:
#                 await asyncio.sleep(delay)
#                 delay = min(delay * 1.8, 12)
#                 continue
#             raise RuntimeError(f"Transient HF error after retries: status={resp.status_code}")

#         # other non-retriable statuses -> raise
#         raise RuntimeError(f"HF error: status={resp.status_code}, body={body_preview}")

#     raise RuntimeError("HF failed after retries.")

# # -------- generate multiple images with concurrency limit ----------
# async def generate_images_async(prompt: str, count: int = 3, concurrency: int = 2, width: int = 512, height: int = 512):
#     sem = asyncio.Semaphore(concurrency)

#     async def one_job(seed: int, idx: int):
#         final_prompt = f"{prompt} -- ultra-detailed, high resolution -- seed:{seed}"
#         payload = {
#             "inputs": final_prompt,
#             "parameters": {
#                 "width": width,
#                 "height": height,
#                 # model might ignore some parameters; HF will return helpful errors if unsupported
#             }
#         }
#         async with sem:
#             try:
#                 return await query_hf(payload)
#             except Exception as e:
#                 return e

#     jobs = [asyncio.create_task(one_job(randint(0, 999_999), i)) for i in range(count)]
#     results = await asyncio.gather(*jobs, return_exceptions=False)

#     safe = prompt.strip().replace(" ", "_")
#     saved = []
#     for i, res in enumerate(results, start=1):
#         out_path = os.path.join("Data", f"{safe}{i}.png")
#         if isinstance(res, Exception):
#             print(f"[Save] Query exception for {out_path}: {res}")
#             continue
#         image_bytes, ctype = res
#         if "image" not in ctype:
#             print(f"[Save] Not an image for {out_path}, content-type={ctype}")
#             continue
#         with open(out_path, "wb") as f:
#             f.write(image_bytes)
#         print(f"Saved: {out_path}")
#         saved.append(out_path)
#     return saved

# def GenerateImages(prompt: str, count=3):
#     try:
#         asyncio.run(generate_images_async(prompt, count=count))
#     except Exception as e:
#         print("GenerateImages error:", e)
#     # try opening saved images (best-effort)
#     open_images(prompt, count=count)

# # -------- main loop: monitor file for prompt requests ----------
# WATCH_FILE = r"C:/Users/hites/OneDrive/Desktop/Voice Assistent/Frontend/Fronted/Files/ImageGeneration.data"
# print("ImageGeneration watcher watching:", WATCH_FILE)
# os.makedirs(os.path.dirname(WATCH_FILE), exist_ok=True)

# while True:
#     try:
#         # small sleep to avoid busy-loop
#         sleep(0.5)
#         # read file content
#         with open(WATCH_FILE, "r", encoding="utf-8") as f:
#             Data = f.read()
#         if not Data:
#             continue
#         # Expecting "Prompt,True" or "Prompt,False"
#         try:
#             Prompt, Status = [x.strip() for x in Data.split(",", 1)]
#         except Exception:
#             print("Watcher: invalid file format, content:", repr(Data))
#             # reset to avoid repeated errors
#             with open(WATCH_FILE, "w", encoding="utf-8") as f:
#                 f.write("False,False")
#             continue

#         if Status == "True":
#             print("Generating Images for prompt:", Prompt)
#             GenerateImages(prompt=Prompt, count=3)
#             # Reset status so frontend can request again
#             with open(WATCH_FILE, "w", encoding="utf-8") as f:
#                 f.write("False,False")
#             # continue watching (do not break) so subsequent requests work
#             print("Generation complete. Watching for next request...")
#         else:
#             # nothing to do; loop again
#             continue

#     except FileNotFoundError:
#         # file may not exist yet; wait and continue
#         # print("Watcher: flag file not found, waiting...")
#         sleep(1)
#         continue
#     except Exception as e:
#         print(f"Loop error: {e}")
#         sleep(1)
#         continue


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