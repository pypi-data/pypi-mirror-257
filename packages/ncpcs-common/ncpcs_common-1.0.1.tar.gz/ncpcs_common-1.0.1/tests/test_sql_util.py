from util.sql_util import get_insert_columns_and_values


class TestSqlUtil:
    def test_get_insert_columns_and_values(self):
        columns, values = get_insert_columns_and_values({
            "a": "深爱",
            "b": ['1', '2', '3'],
            "c": 5
        })
        assert columns == 'a,b,c'
        print(values)
        assert values == "'深爱','1,2,3',5"
