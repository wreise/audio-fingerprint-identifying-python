from libs import fingerprint

import argparse
import numpy as np
from scipy import stats
import pandas as pd
import json
from tqdm import tqdm as tqdm

from multiprocessing import Pool

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def get_dict_for_file_local(s_name):
    try:
        return fingerprint.get_dict_for_file('../spotify_dataset/data/'+s_name+'.ogg')
    except:
        return fingerprint.get_dict_for_file('../spotify_dataset/transformed/'+s_name+'.ogg')

def process_pair(s_name1, s_name2):
    song_1, song_2 =  [get_dict_for_file_local(s) for s in [s_name1, s_name2]]

    common_keys = set(song_1).intersection(set(song_2))
    offsets = [[song_1[c], song_2[c]] for c in common_keys]

    mode, count = stats.mode(np.diff(offsets, axis = 1), axis = None)
    return (s_name1, s_name2, offsets), (s_name1, s_name2, mode[0], count[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    pairs_df = pd.read_pickle(args.file)

    results = []
    for (_, pair), _ in zip(pairs_df.iterrows(), range(5)):
        id1, id2 = pair.id1, pair.id2
        matches, alignment = process_pair(id1, id2)
        results.append({c: cv for c,cv in zip(['id1','id2', 'alignment', 'count', 'matches'], [*alignment, matches[2]])})
        
    with open('one_vs_one_alignments.json', 'w') as f_alignments:
        json.dump(results, f_alignments, cls = NpEncoder)
