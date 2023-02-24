# import only system from os
from configparser import Interpolation
from os import system, name
import time 
from numpy import stack, where
from cv2 import bitwise_and, bitwise_not,GaussianBlur,fillPoly,imread, INTER_LANCZOS4,INTER_AREA,INTER_NEAREST,resize,fastNlMeansDenoisingColored,VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FPS, cvtColor, COLOR_BGR2GRAY, createCLAHE, COLOR_BGR2RGB, COLOR_RGB2BGR
from mediapipe import solutions
from pyvirtualcam import PixelFormat, Camera
# define our clear function
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


mp_selfie_segmentation = solutions.selfie_segmentation

def blur_background(image):
    image = resize(image, (0, 0), fx=0.5, fy=0.5, interpolation=INTER_LANCZOS4)
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=1) as selfie_segmentation:
        image = cvtColor(image, COLOR_BGR2RGB)
        image.flags.writeable = False
        results = selfie_segmentation.process(image)
        image = cvtColor(image, COLOR_RGB2BGR)

        # Draw selfie segmentation on the background image.
        condition = stack(
            (results.segmentation_mask,) * 3, axis=-1) > 0.1

        # Blur the background using Gaussian blur
        blurred = GaussianBlur(image, (55, 55), 0)

        output_image = where(condition, image, blurred)
        output_image = resize(output_image, (0, 0), fx=2, fy=2, interpolation=INTER_LANCZOS4)
        return output_image
clear()

banner = '''
───────────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─████████──████████─██████──────────██████─██████████████─████████████████───██████████████─
─██░░░░░░░░░░██─██░░░░██──██░░░░██─██░░██████████████░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─
─██░░██████░░██─████░░██──██░░████─██░░░░░░░░░░░░░░░░░░██─██░░██████████─██░░████████░░██───██░░██████░░██─
─██░░██──██░░██───██░░░░██░░░░██───██░░██████░░██████░░██─██░░██─────────██░░██────██░░██───██░░██──██░░██─
─██░░██████░░██───████░░░░░░████───██░░██──██░░██──██░░██─██░░██████████─██░░████████░░██───██░░██████░░██─
─██░░░░░░░░░░██─────████░░████─────██░░██──██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─
─██░░██████████───────██░░██───────██░░██──██████──██░░██─██░░██████████─██░░██████░░████───██░░██████░░██─
─██░░██───────────────██░░██───────██░░██──────────██░░██─██░░██─────────██░░██──██░░██─────██░░██──██░░██─
─██░░██───────────────██░░██───────██░░██──────────██░░██─██░░██████████─██░░██──██░░██████─██░░██──██░░██─
─██░░██───────────────██░░██───────██░░██──────────██░░██─██░░░░░░░░░░██─██░░██──██░░░░░░██─██░░██──██░░██─
─██████───────────────██████───────██████──────────██████─██████████████─██████──██████████─██████──██████─
───────────────────────────────────────────────────────────────────────────────────────────────────────────'''
print(banner)
print("\n")
print("Hi there! This is a simple program that will make your webcam follow you around. Like those expensive webcam.\n")
print("DISCLAIMER: The resulted webcam camera resolution will take a hit because this software zoom a bit into your face.\n")
print("Contact me at discord Evoreign#0813 if you have any questions or suggestions or got some error.\n")
print("Press enter to continue...")
input()
print("If you want to exit, press ctrl+c or just close the window.\n")
print("Running... Please wait a bit ~5sec...")


start = time.time()
mp_drawing = solutions.drawing_utils
mp_selfie_segmentation = solutions.selfie_segmentation
BG_COLOR = (192, 192, 192) # gray
vc = VideoCapture(0)
if not vc.isOpened():
    raise RuntimeError('Could not open video source')
    
media_mobile = 20
baricentro_x = []
baricentro_y = []    
pref_width = 2560
pref_height = 1440
pref_fps = 60
vc.set(CAP_PROP_FRAME_WIDTH, pref_width)
vc.set(CAP_PROP_FRAME_HEIGHT, pref_height)
vc.set(CAP_PROP_FPS, pref_fps)
frame_width, frame_height, frame_fps = [int(vc.get(i)) for i in [CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS]]
clahe = createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

width = frame_width
height = frame_height
fps = 30
zoom_scale = 1.5
width_out = int(width/zoom_scale)
height_out = int(height/zoom_scale)
start_x = 0
start_y = 0
stop_x = width_out
stop_y = height_out
clear()
print(banner)
print('| Camera Settings -----------------------------------')
print(f'Height: {frame_height}PX')
print(f'Width: {frame_width}PX')
print(f'FPS: {frame_fps}\n')
print('-----------------------------------------------------')
print('| Original Output Settings -----------------------------------')
print(f'Height: {height}PX')
print(f'Width: {width}PX')
print(f'FPS: {int(fps)}\n')
print('--------------------------------------------------------------')
print('| Output Settings -----------------------------------')
print(f'Height: {height_out}PX')
print(f'Width: {width_out}PX')
print(f'Active Area: {round(1/zoom_scale,2)}%\n')
print('-----------------------------------------------------')
import numpy as np
end = time.time()
print("Camera starting time:",end - start)
scale_percent = 50 # percent of original size
with solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=False,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as face_mesh:
    with Camera(width_out, height_out, fps, fmt=PixelFormat.BGR) as cam:
        print()
        print('Virtual camera device: ' + cam.device)
        alert = '''
█▀▀ ▄▀█ █▀▄▀█ █▀▀ █▀█ ▄▀█   █ █▀   █▀█ █░█ █▄░█ █▄░█ █ █▄░█ █▀▀
█▄▄ █▀█ █░▀░█ ██▄ █▀▄ █▀█   █ ▄█   █▀▄ █▄█ █░▀█ █░▀█ █ █░▀█ █▄█'''
        print(alert)
        print("If you want to exit, press ctrl+c or just close the window.\n")
        print("Contact me at discord Evoreign#0813 if you have any questions or suggestions or got some error.\n")
        while True:
            ret, image = vc.read()

            gray = cvtColor(image, COLOR_BGR2GRAY)
            width_downscale = int(gray.shape[1] * scale_percent / 100)
            height_downscale = int(gray.shape[0] * scale_percent / 100)
            dim = (width_downscale, height_downscale)

            #downscale gray for faster processing
            gray_downscale = resize(gray, dim, interpolation = INTER_LANCZOS4)
            equalize_frame = clahe.apply(gray)
            equalize_frame = cvtColor(equalize_frame, COLOR_BGR2RGB)
            results = face_mesh.process(equalize_frame)
            image.flags.writeable = False

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    x_face_min = face_landmarks.landmark[234].x
                    y_face_min = face_landmarks.landmark[234].y

                    x_face_max = face_landmarks.landmark[447].x
                    y_face_max = face_landmarks.landmark[447].y

                    x_face = int((x_face_max + x_face_min)/2*width)
                    y_face = int((y_face_max + y_face_min)/2*height)

                baricentro_x.append(x_face)
                baricentro_y.append(y_face)

                smooth = len(baricentro_x)
                smooth_y = len(baricentro_y)
                if smooth > media_mobile:
                    del baricentro_x[0]
                    del baricentro_y[0]
                    x_face = int(sum(baricentro_x)/media_mobile)
                    y_face = int(sum(baricentro_y)/media_mobile)
                else:
                    x_face = int(sum(baricentro_x)/smooth)
                    y_face = int(sum(baricentro_y)/smooth_y)

                if y_face - height_out/2 < 0:
                    start_y = 0
                    stop_y = height_out
                elif y_face + height_out/2 > height:
                    start_y =  height - height_out
                    stop_y = height
                else:
                    start_y = y_face-height_out/2
                    stop_y = y_face+height_out/2

                if x_face - width_out/2 < 0:
                    start_x = 0
                    stop_x = width_out
                elif x_face + width_out/2 > width:
                    start_x = width - width_out
                    stop_x = width
                else:
                    start_x = x_face - width_out/2
                    stop_x = x_face + width_out/2

                image_crop = image[int(start_y):int(stop_y), int(start_x):int(stop_x), :]
                #selfie segmentation
                image_crop = blur_background(image_crop)
            else:
                image_crop = resize(image, (width_out, height_out), interpolation=INTER_LANCZOS4)
                image_crop = blur_background(image_crop)
            cam.send(image_crop)
            cam.sleep_until_next_frame()