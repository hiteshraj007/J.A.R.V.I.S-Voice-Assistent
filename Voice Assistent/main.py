# from Frontend.GUI import (
# GraphicalUserInterface,
# SetAssistantStatus,
# ShowTextToScreen,
# TempDirectoryPath,
# SetMicrophoneStatus,
# AnswerModifier,
# QueryModifier,
# GetMicrophoneStatus,
# GetAssistantStatus )
# from Backend.Model import FirstLayerDMM
# from Backend.RealtimeSearchEngine import RealtimeSearchEngine
# from Backend.Automation import Automation
# from Backend.SpeechToText import SpeechRecognition
# from Backend.Chatbot import ChatBot
# from Backend.TextToSpeech import TextToSpeech
# from dotenv import dotenv_values
# from asyncio import run
# from time import sleep
# import subprocess
# import threading
# import json
# import os

# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username")
# Assistantname = env_vars.get("Assistantname")
# DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
# {Assistantname} : Welcome {Username}. I am doing well. How may I assist you today?'''
# subprocesses = []
# Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# def ShowDefaultChatIfNoChats():
#     File = open(r'Data\ChatLog.json',"r", encoding='utf-8')
#     if len(File.read())<5:
#         with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
#             file.write("")

#         with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
#             file.write("DefaultMessage")

# def ReadChatLogJson():
#     with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
#         chatlog_data = json.load(file)
#     return chatlog_data

# def ChatLogIntegration():
#     json_data = ReadChatLogJson()
#     formatted_chatlog = ""
#     for entry in json_data:
#         if entry["role"] == "user":
#             formatted_chatlog += f"User: {entry['content']}\n"
#         elif entry["role"] == "assistant":
#             formatted_chatlog += f"Assistant: {entry['content']}\n" 
#     formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
#     formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")

#     with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
#         file.write(AnswerModifier(formatted_chatlog))

# def ShowChatsOnGUI():
#     File = open(TempDirectoryPath('Database.data'),"r", encoding='utf-8')
#     Data = File.read()
#     if len(str(Data))>0:
#         lines = Data.split('\n')
#         result = '\n'.join(lines)
#         File.close()
#         File = open(TempDirectoryPath('Responses.data'),"w", encoding='utf-8')
#         File.write(result)
#         File.close()

# def InitializeExecution():
#     SetMicrophoneStatus("False")
#     ShowTextToScreen("")
#     ShowDefaultChatIfNoChats()
#     ChatLogIntegration()
#     ShowChatsOnGUI()

# def _is_blank(q):
#     return (q is None) or (str(q).strip() == "") or (str(q).strip().lower() == "none")

# InitializeExecution()

# def MainExecution():

#     TaskExecution = False
#     ImageExecution = False
#     ImageGenerationQuery = ""

#     SetAssistantStatus("Listening...")
#     # Query = SpeechRecognition()
#     Query = SpeechRecognition()

#     # ⛔ if kuch suna hi nahi (None / empty) to wapas available
#     if _is_blank(Query):
#         SetAssistantStatus("Available...")
#         return False

#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")

#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")
#     # Decision = FirstLayerDMM(Query)

#     # print("")
#     # print(f"Decision : {Decision}")
#     # print("")
#     Decision = FirstLayerDMM(Query)

#     print("")
#     print(f"Decision : {Decision}")
#     print("")

#     # ⛔ agar decision bana hi nahi
#     if not Decision:
#         SetAssistantStatus("Available...")
#         ShowTextToScreen(f"{Assistantname} : I could not understand. Please say again.")
#         return False


#     G = any([i for i in Decision if i.startswith("general")])
#     R = any([i for i in Decision if i.startswith("realtime")])

#     Merged_query = " and ".join(
#         [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
#     )

#     for queries in Decision:
#         if "generate " in queries:
#             ImageGenerationQuery = str(queries)
#             ImageExecution = True

#     for queries in Decision:
#         if TaskExecution == False:
#             if any(queries.startswith(func) for func in Functions):
#                 run(Automation(list(Decision)))
#                 TaskExecution = True

#     # if ImageExecution == True:

#     #     with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
#     #         file.write(f"{ImageGenerationQuery},True")

#     #     try:
#     #         p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#     #                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#     #                                stdin=subprocess.PIPE, shell=False)
#     #         subprocesses.append(p1)

#     #     except Exception as e:
#     #         print(f"Error starting ImageGeneration.py: {e}")
#     if ImageExecution is True:
#         SetAssistantStatus("Generating images (fast)...")

#         # with open(r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data", "w", encoding="utf-8") as file:
#         #     file.write(f"{ImageGenerationQuery},True")
#         IMAGE_FLAG_PATH = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data"
        
#         os.makedirs(os.path.dirname(IMAGE_FLAG_PATH), exist_ok=True)

#         try:
#             with open(IMAGE_FLAG_PATH, "w", encoding="utf-8") as file:
#                 file.write(f"{ImageGenerationQuery},True")
#             print("WROTE FLAG ->", IMAGE_FLAG_PATH)
#             # readback to confirm
#             with open(IMAGE_FLAG_PATH, "r", encoding="utf-8") as f:
#                 print("FLAG CONTENTS ->", repr(f.read()))
#         except Exception as e:
#             print("ERROR writing flag file:", e)


#         try:
#             log_path = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\imagegen.log"
#             with open(log_path, "ab") as logfile:
#                 subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#                                 stdout=logfile, stderr=logfile, stdin=subprocess.DEVNULL, shell=False)
#             print("Started ImageGeneration.py; logs ->", log_path)

#         except Exception as e:
#             ShowTextToScreen(f"{Assistantname} : Image generator failed: {e}")

#         SetAssistantStatus("Available...")
#         return True

#     if G and R or R:

#         SetAssistantStatus("Searching ...")
#         Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
#         ShowTextToScreen(f"{Assistantname} : {Answer}")
#         SetAssistantStatus("Answering ...")
#         TextToSpeech(Answer)
#         return True
    
#     else:
#         for Queries in Decision:

#             if "general" in Queries:
#                 SetAssistantStatus("Thinking ...")
#                 QueryFinal = Queries.replace("general ","")
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 return True
            
#             elif "realtime" in Queries:
#                 SetAssistantStatus("Searching ...")
#                 QueryFinal = Queries.replace("realtime ","")
#                 Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 return True
            
#             elif "exit" in Queries:
#                 QueryFinal = "Okay, Bye!"
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 SetAssistantStatus("Answering ...")
#                 os._exit(1)
#                 # ✅ agar upar wali koi branch match hi nahi hui
#     SetAssistantStatus("Available...")
#     return False


# def FirstThread():

#     while True:

#         CurrentStatus = GetMicrophoneStatus()

#         if CurrentStatus == "True":
#             MainExecution()

#         else:
#             AIStatus = GetAssistantStatus()

#             if "Available..." in AIStatus:
#                 sleep(0.1)

#             else:
#                 SetAssistantStatus("Available...")

# def SecondThread():

#     GraphicalUserInterface()

# if __name__ == "__main__":
#     thread2 = threading.Thread(target=FirstThread, daemon=True)
#     thread2.start()
#     SecondThread()
# main.py (patched) - replace your existing main file with this or integrate the write/spawn block
# from Frontend.GUI import (
#     GraphicalUserInterface,
#     SetAssistantStatus,
#     ShowTextToScreen,
#     TempDirectoryPath,
#     SetMicrophoneStatus,
#     AnswerModifier,
#     QueryModifier,
#     GetMicrophoneStatus,
#     GetAssistantStatus,
# )
# from Backend.Model import FirstLayerDMM
# from Backend.RealtimeSearchEngine import RealtimeSearchEngine
# from Backend.Automation import Automation
# from Backend.SpeechToText import SpeechRecognition
# from Backend.Chatbot import ChatBot
# from Backend.TextToSpeech import TextToSpeech
# from dotenv import dotenv_values
# from asyncio import run
# from time import sleep
# import subprocess
# import threading
# import json
# import os
# import sys

# # ------------------ CONFIG (adjust paths if your structure differs) ------------------
# BASE = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent"
# IMAGE_FLAG_PATH = os.path.join(BASE, "Frontend", "Fronted", "Files", "ImageGeneration.data")
# IMAGEGEN_LOG = os.path.join(BASE, "Backend", "imagegen.log")
# # ensure parent folder exists
# os.makedirs(os.path.dirname(IMAGE_FLAG_PATH), exist_ok=True)
# os.makedirs(os.path.dirname(IMAGEGEN_LOG), exist_ok=True)

# # ------------------ env & defaults ------------------
# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username") or "User"
# Assistantname = env_vars.get("Assistantname") or "Assistant"

# DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
# {Assistantname} : Welcome {Username}. I am doing well. How may I assist you today?'''
# subprocesses = []
# Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# # ------------------ helper GUI/data functions ------------------
# def ShowDefaultChatIfNoChats():
#     try:
#         with open(r'Data\ChatLog.json', "r", encoding='utf-8') as File:
#             txt = File.read()
#     except FileNotFoundError:
#         txt = ""
#     if len(txt) < 5:
#         with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
#             file.write("")
#         with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
#             file.write("DefaultMessage")

# def ReadChatLogJson():
#     with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
#         chatlog_data = json.load(file)
#     return chatlog_data

# def ChatLogIntegration():
#     json_data = ReadChatLogJson()
#     formatted_chatlog = ""
#     for entry in json_data:
#         if entry["role"] == "user":
#             formatted_chatlog += f"User: {entry['content']}\n"
#         elif entry["role"] == "assistant":
#             formatted_chatlog += f"Assistant: {entry['content']}\n"
#     formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
#     formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

#     with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
#         file.write(AnswerModifier(formatted_chatlog))

# def ShowChatsOnGUI():
#     try:
#         with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as File:
#             Data = File.read()
#     except FileNotFoundError:
#         Data = ""
#     if len(str(Data)) > 0:
#         lines = Data.split('\n')
#         result = '\n'.join(lines)
#         with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as File:
#             File.write(result)

# def InitializeExecution():
#     SetMicrophoneStatus("False")
#     ShowTextToScreen("")
#     ShowDefaultChatIfNoChats()
#     try:
#         ChatLogIntegration()
#     except Exception as e:
#         print("ChatLogIntegration issue:", e)
#     ShowChatsOnGUI()

# def _is_blank(q):
#     return (q is None) or (str(q).strip() == "") or (str(q).strip().lower() == "none")

# InitializeExecution()

# # ------------------ IMAGE generation helpers inside main ------------------
# def clean_prompt(raw_query: str) -> str:
#     """Turn 'generate image Akshay Kumar.' into a clean prompt for the model."""
#     if not raw_query:
#         return ""
#     s = str(raw_query)
#     s = s.lower()
#     # remove common command tokens
#     s = s.replace("generate image", "").replace("generate", "").replace("image of", "")
#     s = s.strip()
#     # remove punctuation at end
#     s = s.rstrip(".!?")
#     # capitalise first letter for aesthetics (optional)
#     if len(s) > 0:
#         s = s[0].upper() + s[1:]
#     # add style hints
#     final = f"{s}, photorealistic, portrait, high detail"
#     return final

# def start_image_watcher_if_needed():
#     """
#     Start Backend/ImageGeneration.py in background if not already running.
#     Simple check: if IMAGEGEN_LOG exists and was modified recently we assume running.
#     This is a lightweight approach; for production use a PID file or process check.
#     """
#     try:
#         # if log exists and was modified in last 60 seconds, assume running
#         if os.path.exists(IMAGEGEN_LOG):
#             mtime = os.path.getmtime(IMAGEGEN_LOG)
#             if (time_now := (os.path.getmtime(IMAGEGEN_LOG))) and (time_now + 60 > os.path.getmtime(IMAGEGEN_LOG)):
#                 # this check is intentionally conservative; we'll still start if uncertain
#                 pass
#         # Start process and log stdout/stderr to IMAGEGEN_LOG
#         # with open(IMAGEGEN_LOG, "ab") as logfile:
#         #     subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#         #                      stdout=logfile, stderr=logfile, stdin=subprocess.DEVNULL, shell=False)
#         IMAGE_GEN_SCRIPT = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\ImageGeneration.py"
#         PYTHON_EXE = sys.executable  # always venv python

#         with open(IMAGEGEN_LOG, "ab") as logfile:
#             subprocess.Popen(
#                 [PYTHON_EXE, IMAGE_GEN_SCRIPT],
#                 cwd=os.path.dirname(IMAGE_GEN_SCRIPT),
#                 stdout=logfile,
#                 stderr=logfile,
#                 stdin=subprocess.DEVNULL,
#                 shell=False
#             )

#         print("Started ImageGeneration.py; logs ->", IMAGEGEN_LOG)
#     except Exception as e:
#         print("Could not start image watcher:", e)

# # ------------------ MAIN EXECUTION ------------------
# def MainExecution():

#     TaskExecution = False
#     ImageExecution = False
#     ImageGenerationQuery = ""

#     SetAssistantStatus("Listening...")
#     Query = SpeechRecognition()

#     if _is_blank(Query):
#         SetAssistantStatus("Available...")
#         return False

#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")

#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")

#     Decision = FirstLayerDMM(Query)

#     print("")
#     print(f"Decision : {Decision}")
#     print("")

#     if not Decision:
#         SetAssistantStatus("Available...")
#         ShowTextToScreen(f"{Assistantname} : I could not understand. Please say again.")
#         return False

#     G = any([i for i in Decision if i.startswith("general")])
#     R = any([i for i in Decision if i.startswith("realtime")])

#     Merged_query = " and ".join(
#         [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
#     )

#     for queries in Decision:
#         if "generate " in queries:
#             ImageGenerationQuery = str(queries)
#             ImageExecution = True

#     for queries in Decision:
#         if TaskExecution == False:
#             if any(queries.startswith(func) for func in Functions):
#                 run(Automation(list(Decision)))
#                 TaskExecution = True

#     if ImageExecution is True:
#         SetAssistantStatus("Generating images (fast)...")

#         # clean the prompt and write to IMAGE_FLAG_PATH
#         final_prompt = clean_prompt(ImageGenerationQuery)
#         if not final_prompt:
#             ShowTextToScreen(f"{Assistantname} : I couldn't parse the image request.")
#             SetAssistantStatus("Available...")
#             return False

#         # Write atomically and flush to disk to avoid OneDrive caching issues
#         try:
#             with open(IMAGE_FLAG_PATH, "w", encoding="utf-8") as file:
#                 file.write(f"{final_prompt},True")
#                 file.flush()
#                 os.fsync(file.fileno())
#             print("WROTE FLAG ->", IMAGE_FLAG_PATH)
#             # readback to confirm
#             with open(IMAGE_FLAG_PATH, "r", encoding="utf-8") as f:
#                 print("FLAG CONTENTS ->", repr(f.read()))
#         except Exception as e:
#             print("ERROR writing flag file:", e)
#             ShowTextToScreen(f"{Assistantname} : Could not create image request file. {e}")
#             SetAssistantStatus("Available...")
#             return False

#         # Start watcher (if not running) and inform user
#         try:
#             # For simplicity we always attempt to start watcher (it will just create another process if you already started)
#             with open(IMAGEGEN_LOG, "ab") as logfile:
#                 subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#                                  stdout=logfile, stderr=logfile, stdin=subprocess.DEVNULL, shell=False)
#             print("Started ImageGeneration.py; logs ->", IMAGEGEN_LOG)
#         except Exception as e:
#             print("Could not start ImageGeneration.py:", e)
#             ShowTextToScreen(f"{Assistantname} : Image generator failed to start: {e}")
#             SetAssistantStatus("Available...")
#             return False

#         ShowTextToScreen(f"{Assistantname} : Generating images... please check the Data folder shortly.")
#         SetAssistantStatus("Available...")
#         return True

#     if G and R or R:
#         SetAssistantStatus("Searching ...")
#         Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
#         ShowTextToScreen(f"{Assistantname} : {Answer}")
#         SetAssistantStatus("Answering ...")
#         TextToSpeech(Answer)
#         return True

#     else:
#         for Queries in Decision:
#             if "general" in Queries:
#                 SetAssistantStatus("Thinking ...")
#                 QueryFinal = Queries.replace("general ", "")
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 return True

#             elif "realtime" in Queries:
#                 SetAssistantStatus("Searching ...")
#                 QueryFinal = Queries.replace("realtime ", "")
#                 Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 return True

#             elif "exit" in Queries:
#                 QueryFinal = "Okay, Bye!"
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering ...")
#                 TextToSpeech(Answer)
#                 SetAssistantStatus("Answering ...")
#                 os._exit(1)
#     SetAssistantStatus("Available...")
#     return False

# def FirstThread():

#     while True:
#         CurrentStatus = GetMicrophoneStatus()
#         if CurrentStatus == "True":
#             MainExecution()
#         else:
#             AIStatus = GetAssistantStatus()
#             if "Available..." in AIStatus:
#                 sleep(0.1)
#             else:
#                 SetAssistantStatus("Available...")

# def SecondThread():
#     GraphicalUserInterface()

# if __name__ == "__main__":
#     thread2 = threading.Thread(target=FirstThread, daemon=True)
#     thread2.start()
#     SecondThread()


from Frontend.GUI import (
GraphicalUserInterface,
SetAssistantStatus,
ShowTextToScreen,
TempDirectoryPath,
SetMicrophoneStatus,
AnswerModifier,
QueryModifier,
GetMicrophoneStatus,
GetAssistantStatus )
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

import re
# global flag: set True once wakeword heard; stays True until app closed or you manually clear it
WakeUnlocked = False


WAKEWORD = "jarvis"
WAKE_REG = re.compile(rf"\b{re.escape(WAKEWORD)}\b", flags=re.IGNORECASE)
WAKE_LISTENING_PAUSE = 0.25


env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I assist you today?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r'Data\ChatLog.json',"r", encoding='utf-8')
    if len(File.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")

        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write("DefaultMessage")

def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n" 
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'),"r", encoding='utf-8')
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'),"w", encoding='utf-8')
        File.write(result)
        File.close()
def WakeWordListener():
    """
    Minimal wake-word loop.
    - Only listens when microphone is not active (GetMicrophoneStatus() == "False")
    - Uses existing SpeechRecognition() function to capture short audio and checks for WAKEWORD.
    - If WAKEWORD found -> SetMicrophoneStatus("True") and show short text on GUI.
    """

    while True:
        try:
            # only listen for wakeword when mic is off / assistant available
            if GetMicrophoneStatus() == "False":
                # quick listen (SpeechRecognition may block until it gets something)
                # It must be safe: if SpeechRecognition returns None/"" it simply continues
                text = SpeechRecognition()
                if text:
                    txt = str(text).lower()
                    # check if wakeword is present as a whole word
                    # if WAKEWORD in txt.split():
                    #     print("Wakeword detected:", txt)
                    #     ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                    #     SetAssistantStatus("Listening...")
                    #     SetMicrophoneStatus("True")
                    #     # give FirstThread/MainExecution time to take over
                    #     # do not keep listening until helper resets mic
                    #     # small sleep to avoid immediate re-trigger
                    #     sleep(0.5)
                    # if WAKEWORD in txt.split():
                    #     print("Wakeword detected:", txt)
                    #     ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                    #     SetAssistantStatus("Listening...")
                    #     SetMicrophoneStatus("True")

                    #     # ==== ADD THESE LINES ====
                    #     global WakeUnlocked
                    #     WakeUnlocked = True
                    #     # ==========================

                    #     # small debounce so main captures actual command next
                    #     sleep(0.6)
                    if WAKEWORD in txt.split():
                        print("Wakeword detected:", txt)
                        ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                        SetAssistantStatus("Listening...")
                        SetMicrophoneStatus("True")

                        # ==== KEEP ASSISTANT UNLOCKED FOR CONTINUOUS LISTENING ====
                        global WakeUnlocked
                        WakeUnlocked = True
                        # =========================================================

                        # ===== START MAINEXECUTION IMMEDIATELY IN BACKGROUND =====
                        threading.Thread(target=MainExecution, daemon=True).start()
                        # =========================================================

                        # small debounce so main captures actual command next
                        sleep(0.6)


                    else:
                        # optional: very short sleep to avoid busy-looping
                        sleep(WAKE_LISTENING_PAUSE)
                else:
                    # nothing heard — wait a tiny bit
                    sleep(WAKE_LISTENING_PAUSE)
            else:
                # mic already True -> do not compete with MainExecution
                sleep(0.2)
        except Exception as e:
            # don't kill thread on transient errors; print for debugging
            print("WakeWordListener error:", e)
            sleep(0.5)


def InitializeExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitializeExecution()


# def MainExecution(initial_query=None):
#     """
#     If initial_query provided (string), use it directly instead of calling SpeechRecognition().
#     This allows WakeWordListener to pass the immediate command captured right after wakeword.
#     """


#     # SetAssistantStatus("Listening...")
#     # Query = SpeechRecognition()
#     # ShowTextToScreen(f"{Username} : {Query}")
#     # SetAssistantStatus("Thinking...")
#     # Decision = FirstLayerDMM(Query)


#     # SetAssistantStatus("Listening...")
#     # Query = SpeechRecognition()
#     # # show whatever came (None will be shown as 'None' but we'll handle below)
#     # ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Listening...")
#     if initial_query is not None:
#         Query = initial_query
#     else:
#         Query = SpeechRecognition()

#     ShowTextToScreen(f"{Username} : {Query}")



#     # If speech recog failed or returned nothing, reset status & return early
#     # if not Query:
#     #     print("SpeechRecognition returned empty/None. Resetting status.")
#     #     SetAssistantStatus("Available...")
#     #     SetMicrophoneStatus("False")
#     #     return False

def MainExecution(initial_query=None):
    """
    If initial_query is provided, use it instead of calling SpeechRecognition().
    """

    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    if initial_query is not None:
        Query = initial_query
    else:
        Query = SpeechRecognition()

    # show whatever came (None will be shown as 'None' but we'll handle below)
    ShowTextToScreen(f"{Username} : {Query}")

    # If speech recog failed or returned nothing, reset status & return early
    if not Query:
        print("SpeechRecognition returned empty/None.")
        # if unlocked, keep listening (do not turn mic off) — just return
        if WakeUnlocked:
            SetAssistantStatus("Listening...")
            return False
        # else behave as before
        SetAssistantStatus("Available...")
        SetMicrophoneStatus("False")
        return False


#     if not Query:
#         print("SpeechRecognition returned empty/None.")
#         # if unlocked, keep listening (do not turn mic off) — just return
#         if WakeUnlocked:
#             SetAssistantStatus("Listening...")
#             return False
#         # else behave as before
#         SetAssistantStatus("Available...")
#         SetMicrophoneStatus("False")
#         return False


    SetAssistantStatus("Thinking...")
    # Protect the DMM call with try/except so a crash doesn't hang the GUI
    try:
        Decision = FirstLayerDMM(Query)
    except Exception as e:
        print("FirstLayerDMM raised exception:", e)
        SetAssistantStatus("Available...")
        SetMicrophoneStatus("False")
        # Optionally show a friendly message on UI
        ShowTextToScreen(f"{Assistantname} : Sorry, I couldn't process that. Try again.")
        return False


    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    # if ImageExecution == True:

    #     with open(r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data", "w") as file:
    #         file.write(f"{ImageGenerationQuery},True")

    #     try:
    #         p1 = subprocess.Popen(['python', r'C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\ImageGeneration.py'],
    #                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                                stdin=subprocess.PIPE, shell=False)
    #         subprocesses.append(p1)

    #     except Exception as e:
    #         print(f"Error starting ImageGeneration.py: {e}")
    if ImageExecution == True:
    # Clean ImageGenerationQuery to a prompt-only string
        raw = ImageGenerationQuery.strip()
        # remove leading keyword like "generate image" or "create image"
        lowered = raw.lower()
        if lowered.startswith("generate image"):
            prompt_to_write = raw[len("generate image"):].strip()
        elif lowered.startswith("create image"):
            prompt_to_write = raw[len("create image"):].strip()
        else:
            prompt_to_write = raw

        # remove trailing punctuation (dot) and extra commas
        prompt_to_write = prompt_to_write.rstrip(" .,")

        # if user only said a name like "Akshay Kumar", you may want to map to a lookalike descriptive prompt
        if "akshay" in prompt_to_write.lower():
            prompt_to_write = ("portrait of a South-Asian male film actor in his 40s, "
                            "short black hair, confident smile, cinematic studio lighting, photorealistic, high detail")

        # write the cleaned prompt (only) to file
        data_path = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data"
        try:
            with open(data_path, "w", encoding="utf-8") as file:
                file.write(f"{prompt_to_write},True")
            print("Wrote ImageGeneration.data:", prompt_to_write)
        except Exception as e:
            print("Failed writing ImageGeneration.data:", e)

        # start image generator subprocess and show its stderr for debug
        try:
            p1 = subprocess.Popen(
                ['python', r'C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\ImageGeneration.py'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False
            )
            # debug: read a short stderr if it fails quickly (non-blocking attempt)
            try:
                out, err = p1.communicate(timeout=8)  # waits up to 8s
                if out:
                    print("ImageGen stdout:", out.decode(errors='ignore'))
                if err:
                    print("ImageGen stderr:", err.decode(errors='ignore'))
            except Exception:
                # if child takes longer, do not block; append to list so main can continue
                subprocesses.append(p1)
                print("ImageGeneration.py started (background).")
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:

        SetAssistantStatus("Searching ...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True
    
    else:
        for Queries in Decision:

            if "general" in Queries:
                SetAssistantStatus("Thinking ...")
                QueryFinal = Queries.replace("general ","")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "realtime" in Queries:
                SetAssistantStatus("Searching ...")
                QueryFinal = Queries.replace("realtime ","")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering ...")
                os._exit(1)

# def FirstThread():

#     while True:

#         CurrentStatus = GetMicrophoneStatus()

#         if CurrentStatus == "True":
#             MainExecution()

#         else:
#             AIStatus = GetAssistantStatus()

#             if "Available..." in AIStatus:
#                 sleep(0.1)

#             else:
#                 SetAssistantStatus("Available...")
def FirstThread():
    global WakeUnlocked
    while True:
        if WakeUnlocked:
            # keep microphone active for continuous conversation
            # ensure GUI shows Listening and let MainExecution handle each utterance
            try:
                SetAssistantStatus("Listening...")
                SetMicrophoneStatus("True")
                MainExecution()
            except Exception as e:
                print("Error in MainExecution (FirstThread):", e)
                # small sleep to avoid busy-looping on errors
                sleep(0.2)
        else:
            # existing behavior when locked
            CurrentStatus = GetMicrophoneStatus()
            if CurrentStatus == "True":
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available..." in AIStatus:
                    sleep(0.1)
                else:
                    SetAssistantStatus("Available...")

def SecondThread():

    GraphicalUserInterface()

# if __name__ == "__main__":
#     thread2 = threading.Thread(target=FirstThread, daemon=True)
#     thread2.start()
#     SecondThread()

if __name__ == "__main__":
    # Start wakeword listener thread (daemon)
    wake_thread = threading.Thread(target=WakeWordListener, daemon=True)
    wake_thread.start()

    # Start background FirstThread that runs MainExecution when mic is True
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()

    # Launch GUI (blocks)
    SecondThread()
