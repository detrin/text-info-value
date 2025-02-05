import os
import polars as pl

base_dir = 'data/topics'
file_list = []
unique_topics = set()
# Iterate over each topic directory in the base directory
for topic in os.listdir(base_dir):
    topic_path = os.path.join(base_dir, topic)
    
    # Check if it's a directory (to ignore any files in base_dir)
    if os.path.isdir(topic_path):
        tmp_txt_path = os.path.join(topic_path, 'tmp_txt')
        
        # Check if tmp_txt directory exists
        if os.path.exists(tmp_txt_path) and os.path.isdir(tmp_txt_path):
            # Iterate over each file in the tmp_txt directory
            for filename in os.listdir(tmp_txt_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(tmp_txt_path, filename)
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    # Append the dictionary to the list
                    video_title, video_id = filename.split('[')[:-1], filename.split('[')[-1]
                    video_title = '['.join(video_title)
                    video_id = video_id.split("]")[0]
                    vide_url = f"https://www.youtube.com/watch?v={video_id}"
                    file_list.append({
                        'topic': topic,
                        'youtube_url': vide_url,
                        'youtube_title': video_title,
                        'fileText': content
                    })
                    unique_topics.add(topic)
                    # print(filename)

# Now file_list contains the desired list of dictionaries
print(file_list[-1])
print(f"Total files processed: {len(file_list)}")
print(f"Unique topics: {len(unique_topics)}")
print(unique_topics)

pl.DataFrame(file_list).write_parquet('data/dataset.parquet')