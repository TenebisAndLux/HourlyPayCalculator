import re
import math

def calculate_work_hours(time_str):
    pattern = r'^(?P<hours>\d+):(?P<minutes>\d+)$'
    match = re.match(pattern, time_str)
    if match:
        return float(match.group('hours')) + float(match.group('minutes')) / 60
    else:
        print("Неверный формат времени.")
        return 0

def calculate_monthly_hours():
    total_hours = 0
    previous_time = None
    count = 0
    while True:
        time_str = input("Введите время работы (через двоеточие, например 4:30), "
                        "для завершения введите 'exit' или 'del' для удаления предыдущего значения: ").lower()
        if time_str == 'exit':
            break
        elif time_str == 'del':
            if previous_time is not None:
                total_hours -= previous_time
                previous_time = None
                count -= 1
            else:
                print("Нет предыдущих значений для удаления.")
        else:
            try:
                time_hours = calculate_work_hours(time_str)
                total_hours += time_hours
                previous_time = time_hours
                count += 1
            except ValueError:
                print("Неверный формат времени.")
    return total_hours, count

def calculate_salary(total_hours):
    return total_hours * 625

def calculate_salary_tax(total_hours):
    return calculate_salary(total_hours) * 0.87

if __name__ == '__main__':
    total_monthly_hours, count = calculate_monthly_hours()
    total_salary = calculate_salary(total_monthly_hours)
    total_salary_tax = calculate_salary_tax(total_monthly_hours)
    print("Общее количество отработанных часов за месяц:", total_monthly_hours)
    print("Общая сумма заработной платы:", total_salary)
    print("Сумма заработной платы после удержания налогов:", total_salary_tax, '\n')
    print("Дней отработано:", count)
    print("Часов в день:", total_monthly_hours/count)