from datetime import datetime
from khayyam import JalaliDatetime

def to_jalali(dt):
    if dt is None:
        return "-"
    j = JalaliDatetime(dt)
    return j.strftime("%Y/%m/%d - %H:%M")