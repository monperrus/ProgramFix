from common.constants import ACTUAL_C_ERROR_RECORDS, CPP_TESTCASE_ERROR_RECORDS, C_COMPILE_SUCCESS_RECORDS, \
    RANDOM_C_ERROR_RECORDS, COMMON_C_ERROR_RECORDS, SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN, \
    SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID, SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST

CREATE_ACTUAL_C_ERROR_RECORDS = r'''CREATE TABLE IF NOT EXISTS actual_c_error_records (
  id TEXT PRIMARY KEY,
  submit_url TEXT,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  code TEXT,
  gcc_compile_result INTEGER, 
  pycparser_result INTEGER, 
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1
)'''

CREATE_CPP_TESTCASE_ERROR_RECORDS = r'''CREATE TABLE IF NOT EXISTS cpp_testcase_error_records (
  id TEXT PRIMARY KEY,
  submit_url TEXT,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  code TEXT,
  gcc_compile_result INTEGER, 
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1, 
  testcase TEXT DEFAULT ''
)'''

CREATE_C_COMPILE_SUCCESS_RECORDS = r'''CREATE TABLE IF NOT EXISTS c_compile_success_records (
  id TEXT PRIMARY KEY,
  submit_url TEXT,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  language TEXT,
  status TEXT, 
  error_test_id TEXT, 
  gcc_compile_result INTEGER, 
  code TEXT
)
'''

CREATE_RANDOM_C_ERROR_RECORDS = r'''CREATE TABLE IF NOT EXISTS random_c_error_records (
  id TEXT PRIMARY KEY,
  submit_url TEXT,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  code TEXT,
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1
  )
'''

CREATE_COMMON_C_ERROR_RECORDS = r'''CREATE TABLE IF NOT EXISTS common_c_error_records (
  id TEXT PRIMARY KEY,
  submit_url TEXT,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  code TEXT,
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1
  )
'''


CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN = r'''CREATE TABLE IF NOT EXISTS slk_sample_common_c_error_records_train  (
  id TEXT PRIMARY KEY,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  includes TEXT, 
  code TEXT,
  sample_code TEXT,
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1, 
  original_modify_action_list TEXT DEFAULT '', 
  original_distance INTEGER DEFAULT -1
  )
'''

CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID = r'''CREATE TABLE IF NOT EXISTS slk_sample_common_c_error_records_valid  (
  id TEXT PRIMARY KEY,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  includes TEXT, 
  code TEXT,
  sample_code TEXT,
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1, 
  original_modify_action_list TEXT DEFAULT '', 
  original_distance INTEGER DEFAULT -1
  )
'''

CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST = r'''CREATE TABLE IF NOT EXISTS slk_sample_common_c_error_records_test  (
  id TEXT PRIMARY KEY,
  problem_id TEXT,
  user_id TEXT,
  problem_user_id TEXT,
  includes TEXT, 
  code TEXT,
  sample_code TEXT,
  similar_code TEXT DEFAULT '', 
  modify_action_list TEXT DEFAULT '', 
  distance INTEGER DEFAULT -1, 
  original_modify_action_list TEXT DEFAULT '', 
  original_distance INTEGER DEFAULT -1
  )
'''



FIND_CPP_TESTCASE_DISTINCT_PROBLEM_USER_ID = r'''SELECT DISTINCT problem_user_id from cpp_testcase_error_records'''
FIND_RANDOM_C_ERROR_RECORDS_DISTINCT_PROBLEM_USER_ID = r'''SELECT DISTINCT problem_user_id from random_c_error_records'''
FIND_COMMON_C_ERROR_RECORDS_DISTINCT_PROBLEM_USER_ID = r'''SELECT DISTINCT problem_user_id from common_c_error_records'''

INSERT_IGNORE_ACTUAL_C_ERROR_RECORDS = r'''INSERT OR IGNORE INTO actual_c_error_records (id, submit_url, problem_id, user_id, problem_user_id, code, gcc_compile_result, pycparser_result, similar_code, modify_action_list, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_CPP_TESTCASE_ERROR_RECORDS = r'''INSERT OR IGNORE INTO cpp_testcase_error_records (id, submit_url, problem_id, user_id, problem_user_id, code, gcc_compile_result, similar_code, modify_action_list, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_C_COMPILE_SUCCESS_RECORDS = r'''INSERT OR IGNORE INTO c_compile_success_records (id, submit_url, problem_id, user_id, problem_user_id, language, status, error_test_id, gcc_compile_result, code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_RANDOM_C_ERROR_RECORDS = r'''INSERT OR IGNORE INTO random_c_error_records (id, submit_url, problem_id, user_id, problem_user_id, code, similar_code, modify_action_list, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_COMMON_C_ERROR_RECORDS = r'''INSERT OR IGNORE INTO common_c_error_records (id, submit_url, problem_id, user_id, problem_user_id, code, similar_code, modify_action_list, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN = r'''INSERT OR IGNORE INTO slk_sample_common_c_error_records_train (id, problem_id, user_id, problem_user_id, includes, code, sample_code, similar_code, original_modify_action_list, original_distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID = r'''INSERT OR IGNORE INTO slk_sample_common_c_error_records_valid (id, problem_id, user_id, problem_user_id, includes, code, sample_code, similar_code, original_modify_action_list, original_distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST = r'''INSERT OR IGNORE INTO slk_sample_common_c_error_records_test (id, problem_id, user_id, problem_user_id, includes, code, sample_code, similar_code, original_modify_action_list, original_distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

sql_dict = {ACTUAL_C_ERROR_RECORDS: {'create': CREATE_ACTUAL_C_ERROR_RECORDS,
                                     'insert_ignore': INSERT_IGNORE_ACTUAL_C_ERROR_RECORDS, },
            CPP_TESTCASE_ERROR_RECORDS: {'create': CREATE_CPP_TESTCASE_ERROR_RECORDS,
                                         'insert_ignore': INSERT_IGNORE_CPP_TESTCASE_ERROR_RECORDS,
                                         'find_distinct_problem_user_id': FIND_CPP_TESTCASE_DISTINCT_PROBLEM_USER_ID},
            C_COMPILE_SUCCESS_RECORDS: {'create': CREATE_C_COMPILE_SUCCESS_RECORDS,
                                        'insert_ignore': INSERT_IGNORE_C_COMPILE_SUCCESS_RECORDS},
            RANDOM_C_ERROR_RECORDS: {'create': CREATE_RANDOM_C_ERROR_RECORDS,
                                     'insert_ignore': INSERT_IGNORE_RANDOM_C_ERROR_RECORDS,
                                     'find_distinct_problem_user_id': FIND_RANDOM_C_ERROR_RECORDS_DISTINCT_PROBLEM_USER_ID},
            COMMON_C_ERROR_RECORDS: {'create': CREATE_COMMON_C_ERROR_RECORDS,
                                     'insert_ignore': INSERT_IGNORE_COMMON_C_ERROR_RECORDS,
                                     'find_distinct_problem_user_id': FIND_COMMON_C_ERROR_RECORDS_DISTINCT_PROBLEM_USER_ID},
            SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN: {'create': CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN,
                                                      'insert_ignore': INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TRAIN},
            SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID: {'create': CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID,
                                                        'insert_ignore': INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_VALID},
            SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST: {'create': CREATE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST,
                                                        'insert_ignore': INSERT_IGNORE_SLK_SAMPLE_COMMON_C_ERROR_RECORDS_TEST}
}
