from typing import List


def read_ip_addresses_from_file(file_path: str) -> List[str]:
    """
    Читает список IP-адресов из текстового файла.

    Args:
        file_path (str): Путь к файлу с IP-адресами.

    Returns:
        List[str]: Список прочитанных IP-адресов.

    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет доступа к файлу.
    """
    try:
        with open(file_path, 'r') as file:
            # Чтение каждой строки файла, удаление пробельных символов в начале и конце строки.
            # Формирование и возвращение списка непустых строк.
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу {file_path}.")

