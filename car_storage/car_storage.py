import csv
import os


class CarBase:

    def __init__(self, brand, photo_file_name, carrying, car_type):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
        self.car_type = car_type

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count, car_type="car"):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):

    def __init__(self, brand, photo_file_name, carrying, body_length, body_width, body_height, car_type="truck"):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.body_length = body_length
        self.body_width = body_width
        self.body_height = body_height

    def get_body_volume(self):
        if self.body_length == 0:
            return 0
        else:
            return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):

    def __init__(self, brand, photo_file_name, carrying, extra, car_type="spec_machine"):
        super().__init__(brand, photo_file_name, carrying, car_type)
        self.extra = extra


def parse_car_list(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if j == 2:
                if lst[i][j] == "":
                    lst[i][j] = None
                else:
                    lst[i][j] = int(lst[i][j])
            elif j == 4:
                if lst[i][j] == "":
                    lst[i][j] = [0 for i in range(3)]
                else:
                    lst[i][j] = [float(val) for val in lst[i][j].split("x")]
            elif j == 5:
                lst[i][j] = float(lst[i][j])
    return lst


def get_car_list(csv_filename):

    car_list = []
    unparsed_car_list = []

    with open(csv_filename, encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) < 7:
                continue
            unparsed_car_list.append(row)
        parsed_car_list = parse_car_list(unparsed_car_list)

    for i in range(len(parsed_car_list)):
        if parsed_car_list[i][0] == "car":
            car_list.append(Car(
                parsed_car_list[i][1],
                parsed_car_list[i][3],
                parsed_car_list[i][5],
                parsed_car_list[i][2]
            ))
        elif parsed_car_list[i][0] == "truck":
            car_list.append(Truck(
                parsed_car_list[i][1],
                parsed_car_list[i][3],
                parsed_car_list[i][5],
                parsed_car_list[i][4][0],
                parsed_car_list[i][4][1],
                parsed_car_list[i][4][2]
            ))
        elif parsed_car_list[i][0] == "spec_machine":
            car_list.append(SpecMachine(
                parsed_car_list[i][1],
                parsed_car_list[i][3],
                parsed_car_list[i][5],
                parsed_car_list[i][6]
             ))

    return car_list
