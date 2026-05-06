from tqdm import tqdm
import os

MAX_CLASSES = 100          # set None for all classes
MAX_VIDEOS_PER_CLASS = 30 # limit per class

class_counter = {}
selected_classes = set()

for item in tqdm(data):
    cls = item["gloss"]

    # limit number of classes
    if MAX_CLASSES is not None:
        if cls not in selected_classes:
            if len(selected_classes) >= MAX_CLASSES:
                continue
            selected_classes.add(cls)

    save_dir = os.path.join(DATASET_DIR, cls)
    os.makedirs(save_dir, exist_ok=True)

    # initialize counter
    if cls not in class_counter:
        class_counter[cls] = 0

    for inst in item["instances"]:
        # limit videos per class
        if class_counter[cls] >= MAX_VIDEOS_PER_CLASS:
            break

        url = inst.get("url", None)
        if not url:
            continue

        # filter only youtube links (important!)
        if "youtube" not in url and "youtu.be" not in url:
            continue

        video_id = inst["video_id"]
        out_path = os.path.join(save_dir, f"{video_id}.mp4")

        # skip if already downloaded (resume support)
        if os.path.exists(out_path):
            class_counter[cls] += 1
            continue

        success = download_video(url, out_path)

        if success:
            class_counter[cls] += 1