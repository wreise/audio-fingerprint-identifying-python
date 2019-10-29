from libs.config import get_config
from libs.db_sqlite import SqliteDatabase
import pandas as pd

if __name__=='__main__':
    config = get_config()
    db = SqliteDatabase()

    distinct_names_in_db = db.executeAll(" SELECT id,name,filehash FROM songs")
    
    df = pd.DataFrame.from_dict([{c: cv for cv, c in zip(r,['id','name', 'hash'])} for r in distinct_names_in_db])
    df.to_pickle('./db/fingerprinted_songs.pkl')
