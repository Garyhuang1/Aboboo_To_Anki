import re  # 导入re正则表达式库
import os  # operating system
import random  # 生成随机数命名文件
import shutil  # Move files
import tkinter.messagebox  # dialogue boxes


# get current directory
current_dir = os.getcwd()

# Final txt path to Anki
Input_Anki_txt_path = current_dir + "\\" + r"Input_Anki.txt"

# get anki media path
anki_media_path = os.path.expandvars(r'%APPDATA%\Anki2\用户1\collection.media')

# a list contains all the folders within current folder
subFolderPath = [f.path for f in os.scandir(current_dir) if f.is_dir()]

# convert subFolderPath to string
outputFolderPath = " ".join(subFolderPath)  # all files contained in this folder which is output from Aboboo



def main():
    # 从0-9中选择8个随机且独立的元素；返回的是字符串
    random_number_10 = ''.join(str(x) for x in random.sample(range(0, 9), 8))

    allFileOutput = os.listdir(outputFolderPath)

    # algorithm to find the

    max = 0

    for name in allFileOutput:
        num = int(os.path.splitext(name)[0])
        max = num if num > max else max

    # new way to loop through all the mp3 and lrc files
    for i in range(1,max + 1):
        old_lrc_path = outputFolderPath + "\\" + str(i) + r".lrc"
        old_mp3_path = outputFolderPath + "\\" + str(i) + r".mp3"

        new_random_number_10 = random_number_10 + str(i)
        print(old_mp3_path)
        print(os.path.isfile(old_mp3_path))

        # check whether the ".lrc" and ".mp3" file exists at the same time
        if ((os.path.isfile(old_lrc_path) and os.path.isfile(old_mp3_path)) == True):
            with open(old_lrc_path, "r+", encoding="utf-8") as Text:  # 打开单个字幕文本写入Text

                # 提取带时间戳的字幕文本到列表sentence_with_timeline
                sentence_with_timeline = Text.readlines()

                # 列表转字符串，以便正则替换时间戳
                convert_subtitle_to_string = " ".join(sentence_with_timeline)

                # 正则删去时间戳
                Delete_timeline = re.sub("^(.*?)]", "", convert_subtitle_to_string)

                # 换行替换制表符，并添加sound标签以随机数为索引。
                final_subtitle = "[sound:" + new_random_number_10 + ".mp3]" + "\t" + Delete_timeline + "\n"

                # append the text into final txt file
                open(Input_Anki_txt_path, "a+", encoding="utf-8").write(final_subtitle)

            # rename mp3 name：
            # os.rename funciton is just like cut
            new_old_mp3_name = anki_media_path + "\\" + new_random_number_10 + ".mp3"
            os.rename(old_mp3_path, new_old_mp3_name)

            # delete lrc
            os.remove(old_lrc_path)

            # os.remove(old_mp3_path)

        else:
            continue

if __name__ == '__main__':
    main()
    shutil.rmtree(outputFolderPath, ignore_errors=True) # 如果把这个放在main中直接第一次就删除文件夹，要放在main结束后才对
    tkinter.messagebox.showinfo("Aboboo To Anki", 'Successfully ! Please continue to input the "Input_Anki.txt" to Anki. Have a good day !')
