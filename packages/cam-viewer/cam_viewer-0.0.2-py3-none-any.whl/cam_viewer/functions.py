import subprocess
import random
import time
import urllib.request
import logging

cam_proc = None

def current_time():
    return time.strftime("%H:%M:%S", time.localtime())

def cam_data(cams_json = None, cam_name = "", cam_number = 1):
    cam_url = ""
    enabled = True
    response = f"Cam {cam_name} {cam_number} is turned on"
    if cam_name == "": 
        cam_name =  random.choice(list(cams_json.keys()))
        cam_number = random.randrange(1, len(cams_json[cam_name]) + 1)
        response = f"Cam {cam_name} {cam_number} is turned on"
        cam_url = cams_json[cam_name][cam_number - 1]
        logging.info(f"{current_time()} | Rand {response} url: {cam_url}")
    else:
        if cam_name in cams_json and cams_json[cam_name]:
            if 1 <= cam_number <= len(cams_json[cam_name]):
                cam_url = cams_json[cam_name][cam_number - 1]
                logging.info(f"{current_time()} | {response} url: {cam_url}")
                if(not url_available(cam_url)):
                    enabled = False
                    response = f"Cam {str(cam_name)} {str(cam_number)} is disabled"
                    logging.error(f"{current_time()} | {response} url: {cam_url}")
            else:
                enabled = False
                response = f"Cam {len(cams_json[cam_name])} does not exist - invalid number"
                logging.error(f"{current_time()} | {response}")
        else:
            enabled = False
            response = f"Cam {str(cam_name)} {str(cam_number)} does not exist - invalid name"
            logging.error(f"{current_time()} | {response}")
    return [cam_url, enabled, response]

def url_available(cam_url = ""):
    try: 
        urllib.request.urlopen(cam_url)
        return True
    except: return False

def playback(command = "ffplay", parameters = "", cams_json = None, cam_name = "", cam_number = 1, use_text = False, font_file = ""):
    logging.info(f"{current_time()} | Play {command} {parameters} {cam_name} {cam_number} {use_text} {font_file}")
    cam_url = ""
    text = ""
    global cam_proc
    
    cam = cam_data(cams_json, cam_name, cam_number)
    cam_url = cam[0]
    enabled = cam[1]
    response = cam[2]

    if enabled: 
        if use_text and font_file != "": text = f"-vf \"drawtext=fontfile={str(font_file)}:fontsize=18:fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=5:y=5:text='Camera\: {str(cam_name)} {str(cam_number)}'\""
        if cam_proc:
            try:
                logging.info(f"{current_time()} | FFMPEG killing...")
                cam_proc.stdin.write('q'.encode('utf-8'))
                cam_proc.stdin.flush()
                logging.info(f"{current_time()} | FFMPEG killed successfully!")
            except: logging.error(f"{current_time()} | FFMPEG killing ERROR")
        try:
            logging.info(f"{current_time()} | FFMPEG launch: {command} {cam_url} {text} {parameters}")
            cam_proc = subprocess.Popen(f"{command} {cam_url} {text} {parameters}", shell=True, stdin=subprocess.PIPE)
        except: logging.error(f"{current_time()} | FFMPEG launch ERROR")
    return [cam_proc, response]