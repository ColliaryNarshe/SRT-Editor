from glob import glob
import re
import os.path

# 01:02:22,890 --> 01:02:26,951

def adjust_time_digits(hr, m, sec, mil):
    '''Takes altered time and adjusts for below/above 0/60'''
    # adjust numbers for positive input

    if mil >= 1000:
        mil -= 1000
        sec += 1
    if sec >= 60:
        sec -= 60
        m += 1
    if m >= 60:
        m -= 60
        hr += 1

    # adjust numbers for negative input:
    if m < 0:
        m += 60
        hr -= 1
    if sec < 0:
        sec += 60
        m -= 1
    if mil < 0:
        mil += 1000
        sec -= 1
    return hr, m, sec, mil


def alter_srt(srt_file, min, sec, mil):
    # Creates a new srt file with altered times
    num = 1
    while True:
        new_filename = "new_SRT_file " + str(num).zfill(2) + ".srt"
        if os.path.exists(os.path.join(os.path.dirname(srt_file), new_filename)):
            num += 1
        else:
            break

    new_filename = os.path.join(os.path.dirname(srt_file), new_filename)

    new_file = open(new_filename, 'w')
    with open(srt_file) as f:
        for line in f:
            if '-->' in line:
                # index numbers:      1hr   2min   3sec   4milli    5    6hr    7min   8sec  9 milli
                times = re.search(r'(\d\d):(\d\d):(\d\d),(\d\d\d)( --> )(\d\d):(\d\d):(\d\d),(\d\d\d)', line)
                hr1 = int(times[1])
                min1 = int(times[2]) + min
                sec1 = int(times[3]) + sec
                mill1 = int(times[4]) + mil
                hr2 = int(times[6])
                min2 = int(times[7]) + min
                sec2 = int(times[8]) + sec
                mill2 = int(times[9]) + mil

                hr1, min1, sec1, mill1 = adjust_time_digits(hr1, min1, sec1, mill1)
                hr2, min2, sec2, mill2 = adjust_time_digits(hr2, min2, sec2, mill2)

                new_file.write(str(hr1).zfill(2)+':'+str(min1).zfill(2)+
                               ':'+str(sec1).zfill(2)+','+str(mill1).zfill(3)+times[5]+
                               str(hr2).zfill(2)+':'+str(min2).zfill(2)+
                               ':'+str(sec2).zfill(2)+','+str(mill2).zfill(3))
                new_file.write('\n')
            else:
                new_file.write(line)
    new_file.close()


def main():
    srt_files = glob('*.srt')
    if not srt_files:
        print("\n\nNo .srt files...")
        raise SystemExit

    print("\n\n\n\n------------------------\n")

    for idx, file in enumerate(srt_files):
        print(idx, file)

    print("\nEnter index number of file:")

    file_choice = srt_files[int(input('> '))]

    min_choice = int(input("Minutes: (Enter number between -59 & 59)\n> "))
    sec_choice = int(input("Seconds: (Enter number between -59 & 59)\n> "))
    milli_choice = int(input("Milliseconds: (Enter number between -999 & 999)\n> "))

    alter_srt(file_choice, min_choice, sec_choice, milli_choice)

    print("--------\nProcess done!")


if __name__ == '__main__':
    main()
