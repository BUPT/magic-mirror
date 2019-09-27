import os


def merge(video_path1="./human.mp4", cut_position="500:500:390:220", cut_time_during="60",  # human video args
          video_path2="./speech.mp4", merge_position="W-w:H-h",  # speech video args
          audio_name="./audio.mp3", output_path="./output.mp4"):  # audio args
    """
    following is the use of param.
    :param video_path1: human video's path
    :param cut_position: human video's cut position, the format is (width,height,x1,y1)
    :param cut_time_during: how long should the human video be cutted
    :param video_path2: speech video's path
    :param merge_position: two video's merge position, position that we need to overlay (x1,y1)
    :param audio_name: audio name
    :param output_path: the final audio's output path
    :return: None
    """
    cut_human = "ffmpeg -ss 00:00:00 -i " + video_path1 + " -vf crop="
    cut_human = cut_human + cut_position + " ./cutted_human.mp4"  # command to cut human head

    overlay = "ffmpeg -i " + video_path2 + " -i ./cutted_human.mp4" + " -filter_complex overlay=" \
              + merge_position + " -max_muxing_queue_size 1024 ./overlay.mp4"  # command to merge two video

    add_audio = "ffmpeg -i " + "./overlay.mp4" + " -i " + audio_name + \
                " -map 0:v -map 1:a -c copy -shortest " + output_path # command to add audio

    # run all the command
    print("Start cut.")
    os.system(cut_human)
    print("cut finish.")
    print("Start merge.")
    os.system(overlay)
    print("merge finish.")
    print("Start add audio.")
    os.system(add_audio)
    print("add audio finish.")
    if os.path.exists("./cutted_human.mp4"):
        os.remove("./cutted_human.mp4")
    if os.path.exists("./overlay.mp4"):
        os.remove("./overlay.mp4")
    #if os.path.exists("./output.mp4"):
        #os.remove("./output.mp4")
    return 0



if __name__=="__main__":
    merge()
    print("Done Well!!!")