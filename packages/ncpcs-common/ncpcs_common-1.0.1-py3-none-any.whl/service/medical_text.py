from collections import Counter

from constants.level_dict import COLUMN_DICT
from entity.relation_key import RelationKey
from util.string_util import split_text

ORDER_TABLE_DICT = {
    "nc_daily_disease_course": {
        "pageUuid": "606010000",
        "orderSql": " order by nc_disease_course_no ASC,sort_time ASC, nc_record_time, nc_rid"
    },
    "nc_pathology_info": {
        "pageUuid": "611010000",
        "orderSql": " order by nc_pathology_no ASC,sort_time ASC"
    }
}

GET_TEXT_SQL_FORMAT = "select {} from {} where nc_medical_institution_code = '{}' and nc_medical_record_no = '{}' and "\
                     "nc_discharge_time = '{}' and nc_hedge = 0 and nc_data_status != 99"


def extract_medical_text(cursor, relation_key):
    medical_text = []
    for table_name, column_list in COLUMN_DICT.items():
        get_text_sql = GET_TEXT_SQL_FORMAT.format(','.join(column_list), table_name, relation_key.medical_institution_code,
                                                  relation_key.medical_record_no, relation_key.discharge_time)
        page_uuid, get_text_sql = generate_order_sql(get_text_sql)
        cursor.execute(get_text_sql)
        page = 1
        for ele in cursor.fetchall():
            medical_text.extend([
                {
                    "表名": table_name,
                    "字段名": column_list[i],
                    "文本列表": split_text(val),
                    "页码": page,
                    "组号": page_uuid
                }
                for i, val in enumerate(ele) if val]
            )
            page += 1
    return medical_text


def extract_all_relation_key(cursor):
    cursor.execute("select nc_medical_institution_code, nc_medical_record_no, nc_discharge_time from nc_medical_record_first_page")
    relation_key_list = []
    for ele in cursor.fetchall():
        relation_key_list.append(RelationKey(ele[0], ele[1], ele[2]))

    return relation_key_list


def generate_order_sql(sql):
    for table_name, order_info in ORDER_TABLE_DICT.items():
        if sql.count(table_name):
            return order_info['pageUuid'], sql + order_info['orderSql']
    return '', sql


def sentence_count(sentence_list):
    count_dict = Counter(sentence_list)
    for sentence, count in sorted(count_dict.items(), key=lambda t: t[1], reverse=True):
        print(sentence, count)