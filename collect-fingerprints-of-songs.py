#!/usr/bin/python
import os
import sys
import libs
import libs.fingerprint as fingerprint

from tqdm import tqdm as tqdm
import multiprocessing

from termcolor import colored
from libs.reader_file import FileReader
from libs.db_sqlite import SqliteDatabase
from libs.config import get_config

path = "../spotify_dataset/data/"

def read_and_fingerprint(filename, verbose = 0):
    reader = FileReader(path + filename)
    audio = reader.parse_audio()

    song = db.get_song_by_filehash(audio['file_hash'])
    song_id = db.add_song(filename, audio['file_hash'])
    if verbose >1:
        msg = ' * {0} {1}: {2}'.format(
            colored('id={0}', 'white', attrs=['dark']),       # id
            colored('channels=%d', 'white', attrs=['dark']), # channels
            colored('{1}', 'white', attrs=['bold'])           # filename
            )
        print(msg.format(song_id, len(audio['channels']), filename))

    if song:
      hash_count = db.get_song_hashes_count(song_id)

      if hash_count > 0 and verbose >1:
        msg = '   already exists (%d hashes), skip' % hash_count
        print(colored(msg, 'red'))
        return 0
    if verbose>1:
        print(colored('   new song, going to analyze..', 'green'))

    hashes = set()
    channel_amount = len(audio['channels'])

    for channeln, channel in enumerate(audio['channels']):
      if verbose>1:
          msg = '   fingerprinting channel %d/%d'
          print(colored(msg, attrs=['dark']) % (channeln+1, channel_amount))

      channel_hashes = fingerprint.fingerprint(channel, Fs=audio['Fs'], plots=config['fingerprint.show_plots'])
      channel_hashes = set(channel_hashes)

      if verbose >1:
          msg = '   finished channel %d/%d, got %d hashes'
          print(colored(msg, attrs=['dark']) % (
            channeln+1, channel_amount, len(channel_hashes)
            ))

      hashes |= channel_hashes
    if verbose>1:
         msg = '   finished fingerprinting, got %d unique hashes'
         msg = '   storing %d hashes in db' % len(values)
         print(colored(msg, 'green'))
    values = [(song_id, hash, offset) for hash, offset in hashes]
    db.store_fingerprints(values)
    return 0

if __name__ == '__main__':
  config = get_config()

  db = SqliteDatabase()

  # fingerprint all files in a directory
  l = [f for f in os.listdir(path) if f.endswith(".ogg")]
  total_l = len(l)
  with multiprocessing.Pool(3) as pool:
      #for filename in tqdm(l, total = len(l)):
      #  values = read_and_fingerprint(path, filename)
      ind = 0
      for _ in tqdm(pool.map(read_and_fingerprint, l), total = total_l):
          pass
          #print('Processed {0}%'.format(ind/total_l *100)); ind = ind+1

  print('end')
