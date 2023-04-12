import yaml


data = {
    'items_list': ['apple', 'banana', 'latte', 'milk', 'juice'],
    'items_quantity': 5,
    'items_price': {
        'apple': '1\x88',
        'banana': '0.5\x88',
        'latte': '3\x88',
        'milk': '1.1\x88',
        'juice': '0.7\x88'
    }

}

with open('products.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=False,
              allow_unicode=True, sort_keys=False)


with open('products.yaml', 'r', encoding='utf-8') as file_out:
    data_out = yaml.load(file_out, Loader=yaml.SafeLoader)


print(data == data_out)