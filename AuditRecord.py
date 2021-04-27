from datetime import date
from datetime import datetime
import queue
import csv

class AuditRecord:
    def __init__(self, audit_str, user_id):
        self.time_created = datetime.now().strftime("%H:%M:%S")
        self.date = date.today().strftime("%m/%d/%Y")
        self.audit_type = audit_str
        self.user_id = user_id

    def __str__(self):
        val = str(self.date) + ";" + str(self.time_created) + ";" + str(self.audit_type) + ";" + str(self.user_id) + "\n"
        return(val)

def AddAuditRecord(cur_audit_log, audit_type, user_id):
    new_record = AuditRecord(audit_type, user_id)
    if cur_audit_log.full() == True:
        cur_audit_log.get()
    cur_audit_log.put(new_record)


def SaveAuditLogs(cur_audit_log):
    f = open("AuditLogs.csv", "w+")
    while cur_audit_log.empty() != True:
        audit_record = cur_audit_log.get()
        f.write(str(audit_record))
    f.close()


def ImportAuditLog(filename, cur_audit_log):
    with open(filename,'rt') as f:
        data = csv.reader(f)
        for row in data:
            new_entry = AuditRecord(row[3], row[4])
            new_entry.date = row[0]
            new_entry.time_created = row[1]
            if cur_audit_log.full() == True:
                cur_audit_log.get()
            cur_audit_log.put(new_entry)


def DisplayAuditLog(cur_audit_log, userID = ""):
    for elem in list(cur_audit_log.queue):
        print(elem)

