
# PyMera

Hi there! This is a simple program that will make your webcam follow you around. Like those expensive webcam.

DISCLAIMER: The resulted webcam camera resolution will take a hit because this software zoom a bit into your face.

Contact me at discord Evoreign#0813 if you have any questions or suggestions or got some error.
## Install dependencies

To install dependencies

```bash
  pip install mediapipe
  pip install pyvirtualcam
  pip install cv2
```
## Run

To run this project run

```bash
  python main.py
```


## Optimizations

Using MediaPipe facemesh for wider angle detection then face_recognition library

Using CLAHE to improve the detection in uneven or harsh lighting


## Acknowledgements

 - [pyvirtualcam](https://github.com/letmaik/pyvirtualcam)
 - [mediapipe](https://github.com/google/mediapipe)


## Authors

- [@edbertkhovey](https://github.com/evoreign)


## Roadmap

- Finger detection to deactivate and activate the auto tracking feature.

- Virtual background with better edge detection and object detection.

- Denoiseing/Super resolution.

