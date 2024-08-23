from phyphox.data_getter import get_phyphox_data

my_data = get_phyphox_data("day_1")[0]

my_data.set_time_window(1, 8, False)

print(my_data.plot('xya', fit=True))
