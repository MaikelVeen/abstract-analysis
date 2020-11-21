import abstract_parser
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import argparse
import pandas as pd
from datetime import datetime

# TODO: read these from a file
COMMON = ['background', 'objetctive', 'objectives', 'introduction',
          'methods', 'method', 'importance', 'results', 'result', 'aim', 'aims' 'i', 'comment', 'on', 'in']


def _parse_argument():
    parser = argparse.ArgumentParser(description='Abstract Text Analysis')
    parser.add_argument("--f", "--folder", required=True)
    args = parser.parse_args()
    return args.f


def _preprocess_abstract(abstract):
    tokens = nltk.word_tokenize(abstract)
    stop_words = set(stopwords.words('english'))

    tokens = [w for w in tokens if not w in stop_words]  # Remove stop words
    tokens = [w.lower() for w in tokens if w.isalpha()]  # Only words lowercase
    tokens = [w for w in tokens if not w in COMMON]  # Remove common words

    return tokens


def _get_wordbags(abstracts):
    ab_wordbags = []

    for abstract in abstracts:
        ab_wordbags.append(_preprocess_abstract(abstract))

    return ab_wordbags


def _process_abstracts(dataframe):
    abstracts = dataframe['Abstract']
    total_count = abstracts.size
    ab_wordbags = _get_wordbags(abstracts)
    corpus = _get_uniquewords(ab_wordbags)

    dictionary = dict.fromkeys(corpus, 0)

    # Get count for each word by checking each word bag
    for word in dictionary:
        for bag in ab_wordbags:
            if word in bag:
                dictionary[word] += 1

    percentages = []
    for word, count in dictionary.items():
        percentages.append((count / total_count) * 100)

    # Create dataframe and export
    d = {'Word': dictionary.keys(), 'Count': dictionary.values(),
         'Representation': percentages}
    result_df = pd.DataFrame.from_dict(d)
    result_df.to_csv(
        f'word-export-{datetime.now().strftime("%H%M%S")}.csv', sep=';', index=False, header=False)


def _get_uniquewords(wordbags):
    unique_words = set()

    for bag in wordbags:
        unique_words = unique_words.union(set(bag))

    return unique_words


if __name__ == "__main__":
    nltk.download('stopwords')
    folder_path = _parse_argument()

    file_paths = []
    for (dirpath, _, filenames) in os.walk(folder_path):
        for f in filenames:
            file_paths.append(os.path.abspath(os.path.join(dirpath, f)))

    for file_path in file_paths:
        data = abstract_parser.parse_file(file_path)
        _process_abstracts(data)
