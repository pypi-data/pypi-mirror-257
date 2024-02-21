import ipaddress
from typing import List


def minimal_subnet_from_ips(ip_addresses: List[str]) -> str:
    """
    Возвращает минимальную подсеть для списка IPv4 адресов.
    """
    if not ip_addresses:
        return ''

    # Фильтрация и валидация IP-адресов
    ips = []
    for ip_str in ip_addresses:
        try:
            ips.append(ipaddress.IPv4Address(ip_str))
        except ipaddress.AddressValueError as e:
            raise ValueError(f"Невалидный IP-адрес: {ip_str}") from e

    min_ip = min(ips)
    max_ip = max(ips)

    # Преобразуем IP-адреса в двоичный формат и находим общий префикс
    min_ip_bin = bin(int(min_ip))[2:].zfill(32)
    max_ip_bin = bin(int(max_ip))[2:].zfill(32)
    common_prefix_len = 0
    for min_bit, max_bit in zip(min_ip_bin, max_ip_bin):
        if min_bit == max_bit:
            common_prefix_len += 1
        else:
            break

    # Определяем необходимую длину маски подсети, чтобы охватить весь диапазон
    required_bits = 32 - common_prefix_len
    mask_length = 32 - required_bits

    # Создаем и возвращаем строку подсети
    subnet = ipaddress.IPv4Network((min_ip, mask_length), strict=False)
    return f"{subnet.with_prefixlen}"
