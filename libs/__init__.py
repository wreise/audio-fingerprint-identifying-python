import matplotlib
# matplotlib.use('Agg')
matplotlib.use('TkAgg')

__all__ = ['config',
            'db_mongo', 'db_sqlite', 'db', 'fingerprint',
            'reader_file', 'reader_microphone', 'reader',
            'visualizer', 'visualizer_console', 'visualizer_plot']
