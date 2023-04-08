import re
import csv


def get_data():
    manufacturers = []
    os_names = []
    os_codes = []
    os_types = []

    for i in range(1, 4):
        filename = f'info_{i}.txt'
        with open(filename, encoding='Windows-1251') as file:
            data = file.read()

            manufacturer = re.search(r'Изготовитель системы:\s+(.*)', data)
            if manufacturer:
                manufacturers.append(manufacturer.group(1).strip())

            os_name = re.search(r'Название ОС:\s+(.*)', data)
            if os_name:
                os_names.append(os_name.group(1).strip())

            os_code = re.search(r'Код продукта:\s+(.*)', data)
            if os_code:
                os_codes.append(os_code.group(1).strip())

            os_type = re.search(r'Тип системы:\s+(.*)', data)
            if os_type:
                os_types.append(os_type.group(1).strip())

    main_data = [
        ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    ]

    for i in range(len(manufacturers)):
        main_data.append(
            [manufacturers[i], os_names[i], os_codes[i], os_types[i]])

    return main_data


def task_csv(filename):
    # получение данных через вызов функции get_data()
    data = get_data()

    # сохранение подготовленных данных в CSV-файл
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# вызов функции write_to_csv()
task_csv('data_report.csv')