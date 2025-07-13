import datetime

def greeting_user () -> str:
    dict_time = {
"Доброе утро":[6, 7, 8, 9, 10],
"Добрый день":[11, 12, 13, 14, 15],
"Добрый вечер":[16, 17, 18, 19, 20, 21, 22],
"Доброй ночи":[0, 1, 2, 3, 4, 5, 23],
             }

    current_date_time = datetime.datetime.now()
    current_time = current_date_time.time()
    hour = current_time.hour
    for i in dict_time:
        d = dict_time[i]
        if hour in d:
           return (i)

