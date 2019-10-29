from libs.reader_file import FileReader
from libs.db_sqlite import SqliteDatabase
from libs.config import get_config
from libs import fingerprint
import argparse
from functools import partial

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seconds', default = 5)
    parser.add_argument('-f', '--file_name')
    args = parser.parse_args()

    file_name, seconds = args.file_name, args.seconds
    reader = FileReader(filename = file_name)
    audio = reader.parse_audio()
    data = audio['channels']
    Fs = fingerprint.DEFAULT_FS
    channel_amount = len(data)

    config = get_config()
    db = SqliteDatabase()
    find_matches_with_db = partial(fingerprint.find_matches, db = db)
    #try:
    matches = []
    for channeln, channel in enumerate(data):
        # TODO: Remove prints or change them into optional logging.
        matches.extend(find_matches_with_db(samples = channel))

        #msg = '   finished channel %d/%d, got %d hashes'
        #print(colored(msg, attrs=['dark']) % (
        #  channeln+1, channel_amount, len(m)
        #))
    m = [m for m in matches]
    song = fingerprint.align_matches(m)
    print(song)
    #except Exception as e:
    #    print('Did not manage to get to the end', e)
