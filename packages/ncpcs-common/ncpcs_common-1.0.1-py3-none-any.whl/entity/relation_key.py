class RelationKey:
    def __init__(self, medical_institution_code, medical_record_no, discharge_time):
        self.medical_institution_code = medical_institution_code
        self.medical_record_no = medical_record_no
        self.discharge_time = discharge_time

    def __repr__(self):
        return '<RelationKey [机构代码：%s， 病案号：%s，出院时间：%s]>' % (self.medical_institution_code, self.medical_record_no, self.discharge_time)