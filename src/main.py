from src.services import profitable_cashback
from src.views import main_page
from utils import greeting_user


def main ():
    print(greeting_user())
    file_operations = input('Укажите путь к файлу с операциями:      ')
    print('Введите входящую дату для анализа:')
    day_user = input('Укажите день:  ')
    mouth_user = input('Укажите месяц:  ')
    year_user = input('Укажите год:  ')
    date_list =  []
    date_list.append(day_user)
    date_list.append(mouth_user)
    date_list.append(year_user)
    date_views = ".".join(date_list)
    main_page(file_operations, date_views)

    print("Анализ какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка")
    number_mouth = input('Введите месяц:  ')
    number_year = input('Введите год: ')
    profitable_cashback(file_operations, number_mouth, number_year)

    print('Отчет трат по заданной категории за последние три месяца (от переданной даты).')
    file_out = input('Введите путь куда вывести отчет в формате Excel')








    return date_views


print(main())