from libs import fingerprint

import argparse
import numpy as np
from scipy import stats
import pandas as pd
import json
from tqdm import tqdm as tqdm

from multiprocessing import Pool

def process_pair(s_name1, s_name2):
    song_1, song_2 = [fingerprint.get_dict_for_file(f) for f in [s_name1, s_name2]]

    common_keys = set(song_1).intersection(set(song_2))
    offsets = [[song_1[c], song_2[c]] for c in common_keys]

    mode, count = stats.mode(np.diff(offsets, axis = 1), axis = None)
    return (s_name1, s_name2, offsets), (s_name1, s_name2, mode, count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    pairs_df = pd.read_pickle(args.file)

    all_alignments = []
    all_matches = {}
    for pair in pairs_df:
        id1, id2 = pair.id1, pair.id2
        matches, alignment = process_pair(id1, id2)
        all_matches.update({(id1, id2): matches})
        all_alignments.append({c: cv for c,cv in zip(['id1','id2', 'alignment', 'count'], alignment})

    with open('one_vs_one_matches.json', 'wb+') as f:
        json.dumps(all_matches)

    with open('one_vs_one_alignments.json', 'wb+') as f:
        json.dumps(all_alignments)
