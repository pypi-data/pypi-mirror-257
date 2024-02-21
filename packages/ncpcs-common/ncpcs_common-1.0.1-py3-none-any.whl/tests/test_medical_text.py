from service.medical_text import extract_all_relation_key, extract_medical_text, sentence_count
from util.database_connection_util import get_tumour_stage_connection


class TestSqlUtil:
    def test_extract_all_relation_key(self):
        pass
        # conn = get_tumour_stage_connection()
        # cursor = conn.cursor()
        # relation_key_list = extract_all_relation_key(cursor)
        # print(len(relation_key_list))

    def test_extract_medical_text(self):
        conn = get_tumour_stage_connection()
        cursor = conn.cursor()
        relation_key_list = extract_all_relation_key(cursor)[:1000]
        sentence_list = []
        for relation_key in relation_key_list:
            medical_text_list = extract_medical_text(cursor, relation_key)
            for medical_text in medical_text_list:
                sentence_list.extend(medical_text['文本列表'])
        sentence_count(sentence_list)


    def test_sentence_count(self):
        sentence_list = ["测试", "测试", "四大皆空", "第三方i哦", "第三方i哦", "第三方i哦"]
        sentence_count(sentence_list)
