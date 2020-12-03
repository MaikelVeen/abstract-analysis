import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import string
import os 

FILTER = ['DOI', 'PMI']

def _parse_argument():
    parser = argparse.ArgumentParser(description='Abstract Text Parser')
    parser.add_argument("--fp", "--filepath", required=True)
    args = parser.parse_args()
    return args.fp


def parse_file(filename):
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

                if abstract[0][:3] not in FILTER and len(abstract) > 0:
                    data.append([''.join(title), ''.join(abstract)])

                title.clear()
                abstract.clear()

            if white_line == 1:
                if line.startswith('['):
                    translated = True

                title.append(line.strip())
                title.append(' ')

            if white_line == ab_line:
                abstract.append(line.strip())
                abstract.append(' ')

            if line == '\n':
                white_line = white_line + 1

    return data


def _save_csv(dataframe):
    dataframe.to_csv(
        f'export-{datetime.now().strftime("%H%M%S")}.csv', sep=';', index=False, header=False)


def _save_textfiles(data):
    """Save abstract dataframe to text files"""
    for entry in data: 
        filename = _slugify(entry[0]) + '.txt'
        save_dir = '/Users/maikelveen/Projects/abstract-analysis/data'
        path = os.path.join(save_dir, filename)
        
        with open(path, 'a') as file:
            file.write(entry[1])


def _slugify(s):
    s = s.strip()
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  
    filename = filename.replace('.', '')
    return filename[:100]

if __name__ == "__main__":
    filename = _parse_argument()
    data = parse_file(filename)
    #_save_csv(data)
    _save_textfiles(data)
