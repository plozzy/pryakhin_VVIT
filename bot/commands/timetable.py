from datetime import date

from db.operations import simple_select
from db.db import conn, cur

week_day = {'пн': range(0, 5),
            'вт': range(5, 10),
            'ср': range(10, 15),
            'чт': range(15, 20),
            'пт': range(20, 25),
            'сб': range(25, 30)}


spaces = '&#4448;&#4448;&#4448;&#4448;&#4448;'
long_lines = '--'
short_lines = '-'
days = ['ПН (ОП)',
        'ВТ (АМ)',
        'СР (АМ)',
        'ЧТ (ОП)',
        'ПТ (ОП)',
        'СБ',
        'ВС']

days_with_spaces = [f'{short_lines}{day}{short_lines}' for day in days]

time = [' 09:30-11:05 -', ' 11:20-12:55 -', ' 13:10-14:45 -', ' 15:25-17:00 -', ' 17:15-18:50 -']


def timetable(message):
    message_array = message.split(' ')
    delta = delta_func()

    nech = simple_select(conn, cur, select_what=['class_name'], select_from='timetable', where="week = 'неч'")
    ch = simple_select(conn, cur, select_what=['class_name'], select_from='timetable', where="week = 'чет'")

    week_type = {'чет': ch, 'нечет': nech}

    if len(message_array) == 1 and message_array[0] == 'Все':
        rasp = ch if (delta // 7) % 2 != 0 else nech
        day = []
        for r in range(0, 30):
            day.append(rasp[r])

        text = rasp_with_time(day, 6)
        return text

    elif len(message_array) == 1 and message_array[0] != 'Все':
        arg = message_array[0].lower()
        day = []
        rasp = ch if (delta // 7) % 2 != 0 else nech
        for r in week_day[arg]:
            day.append(rasp[r])

        text = rasp_with_time(day, 1)
        return text

    elif len(message_array) == 2:
        arg = message_array[1]
        if arg in week_day:

            day = []
            rasp = ch if (delta // 7) % 2 != 0 else nech
            for r in week_day[arg]:
                day.append(rasp[r])

            text = rasp_with_time(day, 1)
            return text

        elif arg in week_type:
            rasp = week_type[arg]

            day = []
            for r in range(0, 30):
                day.append(rasp[r])

            text = rasp_with_time(day, 6, nofw=False)
            return text

    elif len(message_array) == 3:
        day_of_the_week = message_array[1]
        type_of_the_week = message_array[2]
        rasp = week_type[type_of_the_week]

        day = []
        for r in week_day[day_of_the_week]:
            day.append(rasp[r])
        text = f'{day_of_the_week.capitalize()} | {type_of_the_week.capitalize()}ная неделя\n{rasp_with_time(day, 1, nofw=False)}'
        return text


def rasp_with_time(pr, mn, nofw=True):
    if nofw:
        delta = delta_func()
        week_number = (delta // 7) + 1
        week = f'Четная неделя ({week_number})' if (delta // 7) % 2 != 0 else f'Нечетная неделя ({week_number})'

        text = f'{week}\n'
    else:
        text = ''

    for i, item in enumerate(time * mn):
        if i % 5 == 0 and mn > 1:
            text = text + days_with_spaces[i//5] + '\n'
        if pr[i] != None:
            text = text + str(item) + ' ' + pr[i] + '\n'
    return text


def delta_func():
    first_day = date(2021, 8, 30)
    today = date.today()
    delta = (today - first_day).days
    return delta