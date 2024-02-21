import argparse
from common_utils import read_ip_addresses_from_file
import ipv4_utils
import ipv6_utils


def main() -> None:
    # Создаем парсер аргументов командной строки.
    parser = argparse.ArgumentParser(description="Определение минимальной подсети для списка IP-адресов.")
    # Добавляем аргументы для парсера: путь к файлу и версия IP.
    parser.add_argument("file_path", type=str, help="Путь к файлу с IP-адресами.")
    parser.add_argument("ip_version", type=int, choices=[4, 6], help="Версия IP адресов (4 или 6).")
    # Парсинг аргументов командной строки.
    args = parser.parse_args()

    # Чтение списка IP-адресов из файла.
    ip_addresses = read_ip_addresses_from_file(args.file_path)

    try:
        if args.ip_version == 4:
            # Вызов функции для работы с IPv4, если указана версия 4.
            result = ipv4_utils.minimal_subnet_from_ips(ip_addresses)
            print(result)
        elif args.ip_version == 6:
            # Вызов функции для работы с IPv6, если указана версия 6.
            result = ipv6_utils.minimal_subnet_from_ips(ip_addresses)
            print(result)

    except ValueError as e:
        # Обработка ошибок, связанных с невалидными значениями.
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
