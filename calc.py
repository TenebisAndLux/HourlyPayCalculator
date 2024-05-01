import re


def calculate_work_hours(time_str):
    """Преобразует время в формате "ЧЧ:ММ" в количество часов"""
    pattern = r'^(?P<hours>\d+):(?P<minutes>\d+)$'
    match = re.match(pattern, time_str)
    if match:
        return float(match.group('hours')) + float(match.group('minutes')) / 60
    else:
        raise ValueError("Неверный формат времени")


def load_data_from_file(path):
    """Загружает данные из файла 'work_hours.txt' и возвращает список их значений"""
    try:
        with open(path, 'r') as f:
            return [float(line.strip()) for line in f]
    except FileNotFoundError:
        return []


def save_data_to_file(data, path):
    """Сохраняет данные в файл 'work_hours.txt'"""
    with open(path, 'w') as f:
        for value in data:
            f.write(f'{value:.2f}\n')


def add_time(data, time_str, path):
    """Добавляет время в формате "ЧЧ:ММ" в список значений"""
    try:
        data.append(calculate_work_hours(time_str))
        save_data_to_file(data, path)
        return "Значение добавлено."
    except ValueError:
        return "Неверный формат времени."


def calculate_monthly_hours(data, hourly_rate=625):
    """Посчитывает общее количество часов за месяц,
    общую сумму заработной платы и сумму заработной платы после удержания налогов"""
    total_monthly_hours = sum(data)
    count = len(data)
    if count:
        return (
                f"Общее количество отработанных часов за месяц: {total_monthly_hours:.2f}\n" +
                f"Общая сумма заработной платы: {total_monthly_hours * hourly_rate:.2f}\n" +
                f"Сумма заработной платы после удержания налогов: {total_monthly_hours * hourly_rate * 0.87:.2f}\n" +
                f"Дней отработано: {count}\n" +
                f"Часов в день: {total_monthly_hours / count:.2f}"
        )
    else:
        return "Для расчета необходимо добавить значения."
