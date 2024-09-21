import math
import numpy as np


class Station:
    def __init__(self, number: list[int]):
        self.__number = number

    def broadcast_1(self):
        return self.__number

    def broadcast_0(self):
        rec_number = []
        for n in self.__number:
            rec_number.append(n * -1)
        return rec_number


class Receiver:
    def __init__(self, sts: dict):
        self.__stations = sts

    def listen(self, msg: list[int]):
        print("\nПринятое сообщение:")
        m = []
        for st in self.__stations.values():
            s = 0
            number = st.broadcast_1()
            for n in range(len(msg)):
                s += msg[n] * number[n]

            s /= len(msg)
            if s < 0:
                s = 0
            m.append(int(s))
        print([int(i) for i in m])


class Transmitter:
    def __init__(self, sts: list[Station]):
        self.__stations = sts

    def speak(self, msg: list[int]):
        crypto = []
        for i in range(len(self.__stations[0].broadcast_1())):
            crypto.append(0)

        for n in range(len(msg)):
            if msg[n] == 0:
                code = self.__stations[n].broadcast_0()
            else:
                code = self.__stations[n].broadcast_1()

            for c in range(len(code)):
                crypto[c] += code[c]

        print("\nОтправлена сумма сообщений:")
        print([int(c) for c in crypto])

        return crypto


def hadamard_matrix(n: int) -> np.ndarray:
    """Рекурсивная функция для создания матрицы Адамара размерности 2^n."""
    if n == 0:
        return np.array([[1]])  # Базовый случай: матрица размером 1x1

    # Рекурсивно создаём меньшую матрицу
    h_n_minus_1 = hadamard_matrix(n - 1)

    # Строим матрицу размерности 2^n
    top = np.hstack((h_n_minus_1, h_n_minus_1))
    bottom = np.hstack((h_n_minus_1, -h_n_minus_1))

    return np.vstack((top, bottom))


def generate_stations(count: int, code_len: int) -> dict:
    n = int(math.log2(code_len))
    matrix = hadamard_matrix(n)
    sts = {}

    for c in range(count):
        number = []
        for i in range(code_len):
            number.append(matrix[c, i])
        sts[c] = Station(number)

    return sts


def get_data():
    while True:
        try:
            num_stations = int(input("Введите количество станций: "))
            if num_stations <= 0:
                print("Количество станций должно быть положительным числом.")
                continue
            break
        except ValueError:
            print("Введите корректное целое число для количества станций.")

    while True:
        try:
            code_length = int(input("Введите длину кода станции: "))
            if code_length <= 0:
                print("Длина кода станции должна быть положительным числом.")
                continue
            break
        except ValueError:
            print("Введите корректное целое число для длины кода станции.")

    while True:
        message = input(f"Введите сообщение (не более {num_stations} символов): ")
        if len(message) > num_stations:
            print(f"Сообщение не должно превышать длину {num_stations} символов. Повторите ввод.")
        else:
            break

    msg = []
    for m in message:
        msg.append(int(m))

    return num_stations, code_length, msg


if __name__ == '__main__':

    count_station, code_length, message = get_data()

    stations = generate_stations(count_station, code_length)

    print(f"\nИсходное сообщение: {message}")
    print("\nНабор станций:")
    for i in range(len(stations)):
        print(i, ": ", [int(n) for n in stations[i].broadcast_1()])

    tr = Transmitter(stations)
    cr = tr.speak(message)

    rs = Receiver(stations)
    rs.listen(cr)
