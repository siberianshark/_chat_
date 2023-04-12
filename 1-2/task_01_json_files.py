import json


def write_order_to_json(item, quantity, price, buyer, date):
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    with open('orders.json', 'a') as f:
        json.dump(order, f, indent=4)
        f.write('\n')


write_order_to_json("mcbook", 2, 2400, "John", "2023-04-07")
write_order_to_json("iphone", 1, 1500, "Kate", "2023-04-07")