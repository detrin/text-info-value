# text-info-value

topic="rust"
question="What is $topic?"
# download subtitles from YT
mkdir -p data/topics/$topic/tmp_srt
bash download_yt_subtitles.sh -s "$question" -n 100 -o data/topics/$topic/tmp_srt
# convert subtitles to txt
mkdir -p data/topics/$topic/tmp_txt
bash convert_srt_to_txt.sh data/topics/$topic/tmp_srt data/topics/$topic/tmp_txt