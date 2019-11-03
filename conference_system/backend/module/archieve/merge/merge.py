import os


def merge(video_path1="./human.mp4", cut_position="500:500:390:220", cut_time_during="60", scale_size="100:100", # human video args
          video_path2="./speech.mp4", merge_position="W-w:H-h",  # speech video args
          audio_name="./audio.mp3", output_path="./output.mp4", # audio args
          use_configuration_file=False):
    """
    following is the use of param.
    :param video_path1: human video's path
    :param cut_position: human video's cut position, the format is (width,height,x1,y1)
    :param cut_time_during: how long should the human video be cutted
    :param scale_size:the size to scale the human video
    :param video_path2: speech video's path
    :param merge_position: two video's merge position, position that we need to overlay (x1,y1)
    :param audio_name: audio name
    :param output_path: the final audio's output path
    :param use_configuration_file: whether to use configuration file
    :return: None
    """
    if use_configuration_file:
        with open("./configuration.txt") as f:
            line = f.readline()
            para = line.split(' ')
            video_path1 = para[0]
            cut_position = para[1]
            cut_time_during = para[2]
            scale_size = para[3]
            video_path2 = para[4]
            merge_position = para[5]
            audio_name = para[6]
            output_path = para[7]
    cut_human = "ffmpeg "+"-i " + video_path1 + " -vf crop=" + cut_position + ",scale=" + scale_size +" ./cutted_human.mp4"  # command to cut human head

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
    return 0



if __name__=="__main__":
    merge()
    print("Done Well!!!")
