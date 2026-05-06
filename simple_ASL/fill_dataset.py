import os
import json
import yt_dlp
from tqdm import tqdm


JSON_PATH = "WLASL_v0.3.json"
OUTPUT_DIR = "datasets/WLASL_processed"

MAX_CLASSES = 10        # start with small classes
MAX_VIDEOS_PER_CLASS = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

# load JSON
with open(JSON_PATH, "r") as f:
    data = json.load(f)

print("Total entries in JSON:", len(data))


# process the dataset

class_count = 0

for item in tqdm(data):

    if class_count >= MAX_CLASSES:
        break

    label = item["gloss"]
    instances = item["instances"]

    class_folder = os.path.join(OUTPUT_DIR, label)
    os.makedirs(class_folder, exist_ok=True)

    video_count = 0

    for inst in instances:

        if video_count >= MAX_VIDEOS_PER_CLASS:
            break

        url = inst.get("url", None)
        vid = inst.get("video_id", None)

        if url is None or vid is None:
            continue

        save_path = os.path.join(class_folder, f"{vid}.mp4")

        # skip if the video is already downloaded
        if os.path.exists(save_path):
            continue

        try:
            ydl_opts = {
                "outtmpl": save_path,
                "format": "mp4",
                "quiet": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            video_count += 1

        except Exception as e:
            print(f"Failed video: {url}")

    # only count class ithat has has videos
    if video_count > 0:
        class_count += 1
        print(f"Finished class: {label} ({video_count} videos)")
    else:
        # remove empty folder
        os.rmdir(class_folder)

print("DONE: Dataset built successfully!")