"""
    nero_time is just a funtion converting units like days and hours into seconds(int)
"""


def nero_time(days=0,
              hours=0,
              minutes=0,
              seconds=0):
    result = (((((days * 24) + hours) * 60) + minutes) * 60) + seconds
    return result
