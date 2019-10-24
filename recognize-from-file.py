from libs.reader_file import FileReader
import argparse

#song = None
#seconds = 5

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seconds', default = 5)
    parser.add_argument('-f', '--file_name')
    args = parser.parse_args()

    file_name, seconds = args.file_name, args.seconds
    r = FileReader(filename = file_name)
    r.recognize(seconds= seconds)

    print(song)
