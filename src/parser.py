import argparse
import pandas as pd
import numpy as np
from datetime import datetime

def _parse_argument():
	parser = argparse.ArgumentParser(description='Abstract Text Parser')
	parser.add_argument("--fp", "--filepath", required=True)
	args = parser.parse_args()
	return args.fp


def _read_file(filename):
	data = []

	with(open(filename, mode='r', encoding='utf-8-sig')) as fp:
		title = []
		abstract = []

		abstract_num = 2
		white_line = 0
		translated = False

		for line in fp:
			ab_line = 4
			if translated:
				ab_line = 5

			if line.startswith(f'{abstract_num}. '):
				white_line = 0
				translated = False
				abstract_num = abstract_num + 1

				if title and abstract:
					if len(abstract) > 3:
						data.append([''.join(title),''.join(abstract)])
					else: 
						data.append([''.join(title),''])

					title.clear()
					abstract.clear()

			if white_line == 1:
				if(line.startswith('[')):
					translated = True

				title.append(line.strip())
				title.append(' ')
			
			if white_line == ab_line:
				abstract.append(line.strip())
				abstract.append(' ')

			if line == '\n':
				white_line = white_line + 1
	
	return data
	  
def _save_csv(raw_data):
	dataframe = pd.DataFrame(raw_data, columns=['Title', 'Abstract'])
	dataframe.to_csv(f'export-{datetime.now().strftime("%H%M%S")}.csv', sep=';', index=False, header=False)

if __name__ == "__main__":
	filename = _parse_argument()
	raw_data = _read_file(filename)
	_save_csv(raw_data)
