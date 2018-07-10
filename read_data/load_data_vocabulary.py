import json

import more_itertools

from common.constants import CACHE_DATA_PATH
from common.pycparser_util import tokenize_by_clex_fn
from common.util import disk_cache
from read_data.read_experiment_data import read_fake_common_c_error_dataset_with_limit_length
from vocabulary.word_vocabulary import load_vocabulary


@disk_cache(basename='read_filter_without_include_ac_token', directory=CACHE_DATA_PATH)
def read_filter_without_include_ac_token():
    train_df, _, _ = read_fake_common_c_error_dataset_with_limit_length(500)
    transform_lextoken_to_token_fn = lambda token_list: [i.value for i in token_list]
    tokenize_fn = tokenize_by_clex_fn()
    parse_tokens = [transform_lextoken_to_token_fn(tokenize_fn(code)) for code in train_df['similar_code']]
    return parse_tokens


@disk_cache(basename='read_modify_action_token', directory=CACHE_DATA_PATH)
def read_modify_action_token():
    train_df, _, _ = read_fake_common_c_error_dataset_with_limit_length(500)
    train_df['modify_action_list'] = train_df['modify_action_list'].map(json.loads)
    extract_to_token_fn = lambda actions: [act['to_char'] for act in actions]
    act_tokens = [extract_to_token_fn(actions) for actions in train_df['modify_action_list']]
    return act_tokens


@disk_cache(basename='get_common_error_vocabulary', directory=CACHE_DATA_PATH)
def get_common_error_vocabulary_set():
    tokens = set(more_itertools.collapse(read_filter_without_include_ac_token()))
    action_tokens = set(more_itertools.collapse(read_modify_action_token()))
    return tokens | action_tokens


@disk_cache(basename='get_common_error_vocabulary_id_map', directory=CACHE_DATA_PATH)
def get_common_error_vocabulary_id_map():
    word_list = sorted(get_common_error_vocabulary_set())
    return {word: i for i, word in enumerate(word_list)}


@disk_cache(basename='create_common_error_vocabulary', directory=CACHE_DATA_PATH)
def create_common_error_vocabulary(begin_tokens, end_tokens, unk_token, addition_tokens=None):
    vocab = load_vocabulary(get_common_error_vocabulary_set, get_common_error_vocabulary_id_map, begin_tokens=begin_tokens, end_tokens=end_tokens, unk_token=unk_token, addition_tokens=addition_tokens)
    return vocab


if __name__ == '__main__':
    res = get_common_error_vocabulary_set()
    print(type(res), len(res))
    res = get_common_error_vocabulary_id_map()
    print(type(res), len(res))