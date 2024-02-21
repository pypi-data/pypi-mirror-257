import pymysql
from constants.database_config import HOST_DICT, PASSWD_DICT
ENV = "test"


def get_mpi_connection():
    """
    获取ncpcs_mpi库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[ENV], port=4000, user="root", passwd=PASSWD_DICT[ENV],
                           db="ncpcs_mpi", charset="utf8")


def get_sibling_connection():
    """
    获取ncpcs_sibling库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[ENV], port=4000, user="root", passwd=PASSWD_DICT[ENV],
                           db="ncpcs_sibling", charset="utf8")


def get_medical_data_analyze_connection():
    """
    获取ncpcs_medical_data_analyze库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[ENV], port=4000, user="root", passwd=PASSWD_DICT[ENV],
                           db="ncpcs_medical_data_analyze", charset="utf8")


def get_tumour_stage_connection():
    """
    获取ncpcs_solid_tumour_stage库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[ENV], port=4000, user="root", passwd=PASSWD_DICT[ENV],
                           db="ncpcs_tumour_stage", charset="utf8")


def get_tumor_connection():
    """
    获取ncpcs_solid_tumour_stage库的连接
    :return: 数据库连接
    """
    return pymysql.connect(host=HOST_DICT[ENV], port=4000, user="root", passwd=PASSWD_DICT[ENV],
                           db="ncpcs_tumor", charset="utf8")
