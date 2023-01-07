import sqlite3, datetime, pytz, json

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

def get_attendance(emp_id, day):
    c.execute(f"SELECT * FROM Attendance WHERE employee='{emp_id}' and day='{day}'")
    pk = c.fetchone()[0]
    c.execute(f"SELECT * FROM AttendanceActions WHERE AttendanceId='{pk}'")
    data = c.fetchall()
    time = []
    for i in data:
        now = datetime.datetime.strptime(i[2], "%Y-%m-%d %I:%M %p")
        now = (now.hour*60)+now.minute
        if 'CheckIn' in i:
            now = -now
        time.append(now)
    if len(time) > 2:
        time.append(24*60)
    minutes = sum(time)
    hours = f'{minutes//60:02}:{minutes%60:02}'
    return {'attended' : bool(data), 'duration' : hours }


def attendance_history(emp_id):
    history = {'days' : []}
    c.execute(f"SELECT * FROM Attendance WHERE employee='{emp_id}'")
    data = c.fetchall()
    for i,d in enumerate(data):
        history['days'].append({'date' : d[1], 'actions' : []})
        c.execute(f"SELECT * FROM AttendanceActions WHERE AttendanceId='{d[0]}'")
        attendance_data = c.fetchall()
        for ad in attendance_data:
            now = datetime.datetime.strptime(ad[-2], "%Y-%m-%d %I:%M %p")
            Cairo_tz = pytz.timezone('Africa/Cairo')
            now = Cairo_tz.localize(now)
            utc = now.astimezone(pytz.timezone('UTC'))
            action = {'action' : ad[-1], 'time' : f'{utc}'}
            history['days'][i]['actions'].append(action)
    return json.dumps(history, indent=2)

print(get_attendance('EMP01', '2020-04-02'))
print(attendance_history('EMP01'))
