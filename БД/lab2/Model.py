import psycopg2


class Model:
    conection = None
    cursor = None
    insert_query = 'INSERT INTO \"{table}\"({columns_name}) VALUES {values}'

    delete_query = 'Delete From \"{table}\"'
    select_query = 'Select {fields} from \"{table}\"'
    update_query = 'Update \"{table}\" Set {fields} Where {primary_key}'

    def __init__(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="bdfy45231",
                                           port="1111",
                                           database="test")
        self.cursor = self.connection.cursor()

    def insert_callback(self, current_table, values, columns_name):
        str_values = "("
        for i in range(0, len(values)):
            try:
                int(values[i])
                str_values += values[i]
            except:
                str_values += '\'{0}\''.format(values[i])
            str_values += ',' if (i != len(values) - 1) else ')'
        str_columns = ''
        for i in range(1, len(columns_name)):
            str_columns += columns_name[i]
            str_columns += ',' if i != (len(columns_name) - 1) else ''
        status, result = self.execute_query(self.insert_query.format(table=current_table,
                                                                     columns_name=str_columns,
                                                                      values=str_values))
        return status, result

    def create_filters_in_query(self, query, fields):
        filters = []
        for field_name, field in fields:
            if len(str(field)) > 0:
                try:
                    int(field)
                    filters.append(' {0} = {1} '.format(field_name, field))
                except:
                    filters.append(' {0} = \'{1}\' '.format(field_name, field))
        filters_count = len(filters)
        if filters_count > 0:
            query += ' WHERE'
            query += filters[0]
            for i in range(1, filters_count):
                if len(filters[i]) > 0:
                    query += ' AND '
                    query += filters[i]
        return query

    def select_callback(self, current_table, fields_value):
        query = self.select_query
        fields = '*'
        query = self.create_filters_in_query(query, fields_value)
        status, result = self.execute_query(query.format(fields=fields, table=current_table))
        return status, result

    def update_callback(self, current_table, primary_key, new_fields):
        primary_key_name, primary_key_value = primary_key
        if len(str(primary_key_value)) == 0:
            return 'Please set value to primary key ({name})'.format(name=primary_key_name)
        primary_key_part = "{name} = {value}".format(name=primary_key_name, value=primary_key_value)
        fields_part = ''
        for field_name, field_value in new_fields:
            if len(str(field_value)) != 0:
                try:
                    int(field_value)
                    fields_part += " {name} = {value} ".format(name=field_name, value=field_value)
                except:
                    fields_part += " {name} = \'{value}\' ".format(name=field_name, value=field_value)

        if len(fields_part) == 0:
            return 'Please set new value minimum for one field'.format(name=primary_key_name)
        status, result = self.execute_query(self.update_query.format(table=current_table,
                                                           fields=fields_part,
                                                           primary_key=primary_key_part), False)
        return status, result

    def select_from_all_tables(self, value1, value2):
        query = 'Select \"shop\".address, \"worker\".name, \"customer\".name, com.name, com.price ' \
                'From \"order\" ' \
                'Left Join \"assortment\" on \"assortment\".assortment_id = \"order\".assortment_id '\
                'Left Join \"customer\" On \"order\".customer_id = \"customer\".customer_id ' \
                'Left Join \"worker\" On \"worker\".worker_id = \"customer\".worker_id ' \
                'Left Join \"shop\" On \"shop\".shop_id = \"worker\".shop_id ' \
                'INNER Join  (Select * from \"commodity\" ' \
                                'WHERE price Between {value1} AND {value2}) com ' \
                '                       ON com.commodity_id = \"assortment\".commodity_id ' \
                'Order By \"customer\".name'.format(value1=value1, value2=value2)
        status, result = self.execute_query(query)
        return status, result

    def delete_callback(self, current_table, fields):
        query = self.delete_query
        query = self.create_filters_in_query(query, fields)
        status, result = self.execute_query(query.format(values=fields, table=current_table))
        return status, result

    def special_select_by_word(self, current_table, field, words):
        query = 'SELECT * FROM \"{table}\" ' \
                'WHERE to_tsvector(\"{field}\") @@ to_tsquery(\'{words}\')'.format(table=current_table,
                                                                                    field=field,
                                                                                    words=words)
        status, result = self.execute_query(query)
        return status, result

    def execute_query(self, query, is_need_to_fetch=True):
        print(query)
        try:
            self.cursor.execute(query)
            if not is_need_to_fetch:
                return 'Ok', ''
            result = ''
            for record in self.cursor.fetchall():
                result += str(record) + '\n'
            self.connection.commit()
            return 'Ok', result
        except Exception as err:
            self.connection.commit()
            return err, ''

