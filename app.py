import csv
from typing import Iterable


def read_csv(
    path: str, return_header: bool = False,
    delimeter: str = ';'
) -> Iterable[list[str]]:
    """
    Read a CSV file and yield its rows as lists of strings.
    """
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=delimeter)

        row = next(reader)
        if return_header:
            yield row

        for row in reader:
            yield row


def get_hierarchy(path: str) -> dict:
    """
    Retrieve and organize department hierarchy from a CSV file.
    """
    hierarchy = {}
    reader = read_csv(path)

    for row in reader:
        department, team = row[1], row[2]
        if department not in hierarchy:
            hierarchy[department] = set()
        hierarchy[department].add(team)

    return hierarchy


def print_hierarchy(hierarchy: dict) -> None:
    """
    Print the department hierarchy in a readable format.
    """
    print('\n', 'Иерархия команд:', '\n', sep='')
    for department, teams in hierarchy.items():
        print(department)
        for team in teams:
            print(f'\t{team}')
    print()


def get_statistics(path: str) -> dict:
    """
    Calculate and return statistics on employee salaries by department.
    """
    statistics = {}
    reader = read_csv(path)
    for row in reader:
        department, salary = row[1], int(row[-1])

        if department not in statistics:
            statistics[department] = {
                'count': 0,
                'sum_salary': 0,
                'min_salary': float('inf'),
                'max_salary': float('-inf')
            }

        statistics[department]['count'] += 1
        statistics[department]['sum_salary'] += salary

        curr_min_salary = statistics[department]['min_salary']
        curr_max_salary = statistics[department]['max_salary']
        statistics[department]['min_salary'] = min(curr_min_salary, salary)
        statistics[department]['max_salary'] = max(curr_max_salary, salary)

    return statistics


def print_statistics(statistics: dict) -> None:
    """
    Print a summary report of departmental statistics in a readable format.
    """
    print('\n', 'Сводный отчет по департаментам:', '\n', sep='')
    for department, stats in statistics.items():
        count = stats["count"]
        min_salary = stats["min_salary"]
        max_salary = stats["max_salary"]
        avg_salary = stats["sum_salary"] / stats["count"]

        print(department)
        print(f'\tЧисленность: {count} человек')
        print(f'\tВилка зарплат: {min_salary} - {max_salary} рублей')
        print(f'\tСредняя зарплата: {avg_salary:.2f} рублей')
    print()


def save_statistics(
    statistics: dict, path: str, *, save_header: bool = True,
    delimeter: str = ';', rounding: int = 2
) -> None:
    """
    Save departmental statistics to a CSV file.
    """
    with open(path, 'w', encoding='utf-8') as file:
        if save_header:
            columns = [
                'Департамент', 'Численность', 'Минимальная зарплата',
                'Максимальная зарплата', 'Средняя зарплата'
            ]
            row = delimeter.join(columns) + '\n'
            file.write(row)

        for department, stats in statistics.items():
            count = stats["count"]
            min_salary = stats["min_salary"]
            max_salary = stats["max_salary"]
            avg_salary = round(stats["sum_salary"] / stats["count"], rounding)

            columns = [department, count, min_salary, max_salary, avg_salary]
            row = delimeter.join(map(str, columns)) + '\n'
            file.write(row)


def print_menu() -> None:
    """
    Print the main menu options for interacting with employee data.
    """
    print('Меню:')
    print('1. Вывести в понятном виде иерархию команд')
    print('2. Вывести сводный отчёт по департаментам')
    print('3. Сохранить сводный отчёт из предыдущего пункта в виде csv-файла')
    print('Любой символ, чтобы выйти')


def main() -> None:
    """
    Main program to interact with employee data and perform tasks.
    """
    statistics = None
    hierarchy = None

    while True:
        print_menu()
        task = input('Введите номер нужного действия: ').strip()

        if task == '1':
            if not hierarchy:
                hierarchy = get_hierarchy('Corp_Summary.csv')
            print_hierarchy(hierarchy)

        elif task == '2':
            if not statistics:
                statistics = get_statistics('Corp_Summary.csv')
            print_statistics(statistics)

        elif task == '3':
            if not statistics:
                statistics = get_statistics('Corp_Summary.csv')
            save_statistics(statistics, 'Corp_Summary_Statistics.csv')

        else:
            break


if __name__ == '__main__':
    main()
