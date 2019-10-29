from libs import fingerprint
import argparse

import numpy as np
from scipy import stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_names', nargs = 2)
    args = parser.parse_args()

    song_1, song_2 = [ fingerprint.get_dict_for_file(f) for f in args.file_names]

    common_keys = set(song_1).intersection(set(song_2))
    offsets = np.array([song_1[c] - song_2[c] for c in common_keys])

    mode, count = stats.mode(offsets, axis = None)
    print('The offset is {0}, with {1} matching hash pairs'.format(mode[0], count[0]))

    #print(offsets)
