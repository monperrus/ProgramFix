from read_data.read_data import read_train_data_effect_all_c_error_records, read_train_data_all_c_error_records, \
    read_compile_success_c_records, read_fake_common_c_error_records, read_fake_random_c_error_records
from common.util import disk_cache, compile_c_code_by_gcc_c89, group_df_to_grouped_list
from common.constants import CACHE_DATA_PATH


def filter_distinct_table_key(data_df, key, max_num=None):
    if max_num is None:
        max_num = float('inf')
    group_list = group_df_to_grouped_list(data_df, key)
    print('group_list', len(group_list))
    num = min(max_num, len(group_list[0]))
    group_res = group_list[0].sample(num).copy(deep=True)
    i = 0
    for group in group_list[1:]:
        print('filter_distinct_table_key: {} in {}'.format(i, len(group_list)))
        i += 1
        num = min(max_num, len(group))
        group_res = group_res.append(group.sample(num), ignore_index=True)
    return group_res


def filter_distinct_problem_user_id(data_df):
    data_df = filter_distinct_table_key(data_df, 'problem_user_id', max_num=1)
    return data_df


def filter_distinct_problem(data_df, max_num=None):
    data_df = filter_distinct_table_key(data_df, 'problem_id', max_num=max_num)
    return data_df


def filter_distinct_user(data_df, max_num=None):
    data_df = filter_distinct_table_key(data_df, 'user_id', max_num=max_num)
    return data_df


def filter_distinct_test_c_data(data_df):
    data_df = filter_distinct_problem_user_id(data_df)
    data_df = filter_distinct_problem(data_df, 10)
    data_df = filter_distinct_user(data_df, 10)
    return data_df


@disk_cache(basename='read_distinct_problem_user_c_records', directory=CACHE_DATA_PATH)
def read_distinct_problem_user_c_records():
    data_df = read_train_data_all_c_error_records()
    print('origin data size: ', len(data_df))
    data_df = data_df[data_df['distance'].map(lambda x: x != -1)]
    print('after filter distance!=-1 size: ', len(data_df))
    data_df = filter_distinct_problem_user_id(data_df)
    print('after filter distinct problem user size: ', len(data_df))
    return data_df


@disk_cache(basename='read_read_distinct_problem_user_c_records_less_10_error_and_c89', directory=CACHE_DATA_PATH)
def read_read_distinct_problem_user_c_records_less_10_error_and_c89():
    df = read_distinct_problem_user_c_records()
    df = df[df['distance'].map(lambda x: 0 < x < 10)]
    total = len(df)
    print(total)
    count = 0

    def compile_c89(code):
        nonlocal count
        print('now {}/{}'.format(count, total))
        count += 1
        file_path = '/dev/shm/a.c'
        res = compile_c_code_by_gcc_c89(code, file_path)
        return res

    df = df[df['similar_code'].map(compile_c89)]
    success_count = len(df)
    count = 0
    df = df[df['code'].map(lambda x: not compile_c89(x))]
    print('after success {} after failed: {}'.format(success_count, len(df)))
    return df


@disk_cache(basename='read_distinct_problem_user_compile_success_c_records', directory=CACHE_DATA_PATH)
def read_distinct_problem_user_compile_success_c_records():
    data_df = read_compile_success_c_records()
    print('origin data size: ', len(data_df))
    data_df = data_df[data_df['gcc_compile_result'].map(lambda x: x == 1)]
    print('after filter success records: {}'.format(len(data_df)))
    data_df = filter_distinct_problem_user_id(data_df)
    print('after filter distinct problem user size: ', len(data_df))
    return data_df


def read_distinct_problem_user_ac_c_records_filter_error_code():
    ac_df = read_distinct_problem_user_compile_success_c_records()
    print('total distinct ac c records: {}'.format(len(ac_df)))
    error_df = read_distinct_problem_user_c_records()
    print('total error c records: {}'.format(len(error_df)))
    ac_df = ac_df[~ac_df['user_id'].isin(error_df['user_id'])]
    # ac_df = ac_df[ac_df['user_id'].map(lambda x: x not in error_df['user_id'])]
    print('ac df length after filter user_id in error df: {}'.format(len(ac_df)))
    return ac_df


@disk_cache(basename='read_distinct_problem_user_fake_c_random_records', directory=CACHE_DATA_PATH)
def read_distinct_problem_user_fake_c_random_records():
    data_df = read_fake_random_c_error_records()
    print('origin data size: ', len(data_df))
    data_df = data_df[data_df['distance'].map(lambda x: 0 < x < 10)]
    print('after filter distance length between 0 and 10: ', len(data_df))
    data_df = filter_distinct_problem_user_id(data_df)
    print('after filter distinct problem user size: ', len(data_df))
    return data_df


@disk_cache(basename='read_distinct_problem_user_fake_c_common_records', directory=CACHE_DATA_PATH)
def read_distinct_problem_user_fake_c_common_records():
    data_df = read_fake_common_c_error_records()
    print('origin data size: ', len(data_df))
    data_df = data_df[data_df['distance'].map(lambda x: 0 < x < 10)]
    print('after filter distance length between 0 and 10: ', len(data_df))
    data_df = filter_distinct_problem_user_id(data_df)
    print('after filter distinct problem user size: ', len(data_df))
    return data_df


if __name__ == '__main__':
    # df = read_distinct_problem_user_ac_c_records_filter_error_code()
    df = read_read_distinct_problem_user_c_records_less_10_error_and_c89()
    print(len(df))
