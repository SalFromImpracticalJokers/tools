import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def remove_similar_frames(input_video, output_video, similarity_threshold=0.95):
    cap = cv2.VideoCapture(input_video)
    
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return
    
    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))
    
    ret, prev_frame = cap.read()
    out.write(prev_frame)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frames to grayscale
        prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM between current frame and previous frame
        ssim_value = ssim(prev_frame_gray, frame_gray)
        
        if ssim_value < similarity_threshold:
            out.write(frame)
        else:
            print(f"Frame :{frame} removed")
        
        prev_frame = frame
    
    cap.release()
    out.release()

if __name__ == "__main__":
    input_video = input("input name: ")
    output_video = input("what name should it have: ")
    similarity_threshold = 0.985 # Adjust this threshold as needed
    remove_similar_frames(input_video, output_video, similarity_threshold)
