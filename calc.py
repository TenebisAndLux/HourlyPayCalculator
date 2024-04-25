import re


def calculate_work_hours(time_str):
    pattern = r'^(?P<hours>\d+):(?P<minutes>\d+)$'
    match = re.match(pattern, time_str)

    if match:
        return float(match.group('hours')) + float(match.group('minutes')) / 60
    else:
        raise ValueError("Неверный формат времени.")


def load_data_from_file():
    try:
        with open('work_hours.txt', 'r') as f:
            return [float(line.strip()) for line in f]
    except FileNotFoundError:
        return []


def save_data_to_file(data):
    with open('work_hours.txt', 'w') as f:
        for value in data:
            f.write(f'{value}\n')


def add_time(data):
    while True:
        time_str = input("Введите время работы (через двоеточие, например 4:30) или 'exit' для выхода: ")
        if time_str == 'exit':
            break
        else:
            try:
                data.append(calculate_work_hours(time_str))
                save_data_to_file(data)
                print("Значение добавлено.")
            except ValueError:
                print("Неверный формат времени.")


def calculate_monthly_hours(data):
    total_monthly_hours = sum(data)
    count = len(data)
    if count:
        print("Общее количество отработанных часов за месяц:", total_monthly_hours)
        print("Общая сумма заработной платы:", total_monthly_hours * 625)
        print("Сумма заработной платы после удержания налогов:", total_monthly_hours * 625 * 0.87)
        print("Дней отработано:", count)
        print("Часов в день:", total_monthly_hours / count)
    else:
        print("Для расчета необходимо добавить значения.")


def main_input(data):
    while True:
        command = input(
            "Введите 'add' для добавления времени, 'calculate' для расчета, 'del' для удаления, 'clear' для очистки файла или 'exit' для выхода: ").lower()

        if command == 'add':
            add_time(data)
        elif command == 'calculate':
            calculate_monthly_hours(data)
        elif command == 'del':
            if data:
                data.pop()
                save_data_to_file(data)
                print("Последнее значение удалено.")
            else:
                print("Нет значений для удаления.")
        elif command == 'clear':
            data = []
            save_data_to_file(data)
            print("Файл очищен.")
        elif command == 'exit':
            break
        else:
            print("Неизвестная команда.")


if __name__ == '__main__':
    data = load_data_from_file()
    main_input(data)
