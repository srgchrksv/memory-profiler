import cv2
import mediapipe as mp
from memory_profiler import profile
import datetime
import os
import sys

dirs = ['logs', 'plots', 'images']
for path in dirs:
    os.makedirs(path, exist_ok=True)

def get_timestamp():
    # Get current timestamp in the format YYYYMMDD_HHMMSS
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_image_files(image_dir = "./images"):
    # Get list of image file paths from the ./images directory
    return [os.path.join(image_dir, file) for file in os.listdir(image_dir)]

def log_decorator(log_filename):
    # Decorator to log memory profiling to a specified file
    def decorator(func):
        def wrapper(*args, **kwargs):
            with open(log_filename, 'w+') as fp:
                # Apply memory profiling to the function and log to file
                return profile(stream=fp)(func)(*args, **kwargs)
        return wrapper
    return decorator

@log_decorator(f'logs/constant_{get_timestamp()}.log')
def constant(image_paths, results=[]):
    # Process images with a single FaceMesh instance reused across images
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
    for image_path in image_paths:
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        results.append(mp_face_mesh.process(image).multi_face_landmarks[0])
    return results

@log_decorator(f'logs/linear_{get_timestamp()}.log')
def linear(image_paths, results=[]):
    # Process images with a new FaceMesh instance created for each image
    for image_path in image_paths:
        mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        mp_face_mesh.process(image)
        results.append(mp_face_mesh.process(image).multi_face_landmarks[0])
    return results

@log_decorator(f'logs/logn_{get_timestamp()}.log')
def logn(image_paths, results=[]):
    # Process images with a new FaceMesh instance created and closed for each image
    for image_path in image_paths:
        mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        results.append(mp_face_mesh.process(image).multi_face_landmarks[0])
        mp_face_mesh.close()
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Example usage: python facemesh_profiling.py constant")
        sys.exit(1)

    # pass function name as arg when running script 
    function_to_run = sys.argv[1]
    image_files = get_image_files('./images')
    # run functions
    if function_to_run == "constant":
        constant(image_files)
    elif function_to_run == "linear":
        linear(image_files)
    elif function_to_run == "logn":
        logn(image_files)
    elif function_to_run == "test":
        assert constant(image_files) == linear(image_files) == logn(image_files), "Results are not equal"
        print(f"{'='*20}\nResult are equal\n{'='*20}")
