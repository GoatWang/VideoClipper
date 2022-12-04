import os
import cv2
import time
import numpy as np
from pathlib import Path
 

def get_frame_time(frame_id, fps):
    frame_seconds =  frame_id/fps
    hours = "%02i"%(int(frame_seconds)//3600)
    minutes = "%02i"%((int(frame_seconds)%3600)//60)
    seconds = "%02i"%(int(frame_seconds)%60)
    millisecond = "%.3f"%(frame_seconds - int(frame_seconds))
    millisecond = millisecond.replace('.', "")
    return hours, minutes, seconds, millisecond

def play_video(video_fp, save_dir):
    save_dir_current = os.path.join(save_dir, os.path.basename(video_fp).split("-")[-1])
    Path(save_dir_current).mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(video_fp)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sleeping_time = 0

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_id = cap.get(cv2.CAP_PROP_POS_FRAMES)

        if ret == True:
            # Display the resulting frame
            frame_copy = frame.copy()
            progress_str = "%i / %i"%(frame_id,  total_frames)
            cv2.putText(frame_copy, progress_str, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Frame', frame_copy)
            
            # Press Q on keyboard to exit
            time.sleep(sleeping_time)
            key = cv2.waitKey(22)
            print(key)
            if key == ord('p'):
                hours, minutes, seconds, millisecond = get_frame_time(frame_id, fps)
                time_str = hours + minutes + seconds + millisecond
                img_fp = os.path.join(save_dir_current, time_str + ".png")
                print("image save to: ", img_fp)
                cv2.imwrite(img_fp, frame)

            if key == 44: # right
                print("< pressed: decrease sleeping time")
                sleeping_time = sleeping_time-0.1 if sleeping_time-0.1 > 0 else sleeping_time

            if key == 46: # right
                print("> pressed: increase sleeping time")
                sleeping_time = sleeping_time+0.1 if sleeping_time+0.1 <2 else sleeping_time

            if key == 3: # right
                print("right")
                frame_id_target = int(frame_id + (10 * fps))
                print("frame_id_target", frame_id_target)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id_target)

            if key == 2: # left
                print("37")
                frame_id_target = int(frame_id - (10 * fps))
                frame_id_target = 0 if frame_id_target < 0 else frame_id_target
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id_target)

            if key == ord('q'):
                break
    
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import glob 
    from datetime import datetime
    
    video_dir = os.path.join("data", "river_data_prediction_20221204")
    video_fps = glob.glob(os.path.join(video_dir, "*.avi"))
    dt_str = datetime.now().strftime("%Y%m%d%H%M%S")
    save_dir = os.path.join('save', 'save_' + os.path.basename(video_dir) + "_" + dt_str)
    for video_fp in video_fps:
        play_video(video_fp, save_dir)



    # video_fp = "data/2022-09-30-114704.webm"
    # play_video(video_fp, save_dir)
