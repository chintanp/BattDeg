from battdeg import PL_samples_file_joiner

data_dir = '/home/chintan/uwdirect/chintan/BattDeg/data/PL 12,14'
fnf = 'PL12(4).csv'
ignore_indices = [1, 2, 3]

out_df = PL_samples_file_joiner(data_dir, fnf, ignore_indices)