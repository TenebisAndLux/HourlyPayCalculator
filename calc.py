def calculate_work_hours(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60


def calculate_monthly_hours():
    total_hours = 0
    while True:
        time_str = input("Введите время работы (через двоеточие, например 4:30), "
                        "для завершения введите 'exit': ").lower()
        if time_str == 'exit':
            break
        total_hours += calculate_work_hours(time_str)
    return total_hours


def calculate_salary(total_hours):
    return total_hours * 625


def calculate_salary_tax(total_hours):
    return calculate_salary(total_hours) * 0.87


if __name__ == '__main__':
    total_monthly_hours = calculate_monthly_hours()
    total_salary = calculate_salary(total_monthly_hours)
    total_salary_tax = calculate_salary_tax(total_monthly_hours)
    print("Общее количество отработанных часов за месяц:", total_monthly_hours)
    print("Общая сумма заработной платы:", total_salary)
    print("Сумма заработной платы после удержания налогов:", total_salary_tax)

