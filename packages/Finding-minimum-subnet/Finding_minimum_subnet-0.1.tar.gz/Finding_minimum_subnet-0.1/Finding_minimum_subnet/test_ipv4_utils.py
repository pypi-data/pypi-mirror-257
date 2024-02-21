import unittest
import tempfile
import os
from ipv4_utils import minimal_subnet_from_ips
from common_utils import read_ip_addresses_from_file


class TestIPv4Utils(unittest.TestCase):
    def write_to_temp_file(self, content):
        """Вспомогательная функция для записи во временный файл."""
        temp = tempfile.NamedTemporaryFile(delete=False)
        with open(temp.name, 'w') as file:
            file.write(content)
        return temp.name

    def test_mixed_ips_in_file(self):
        """Тестирование файла с IPv4 и IPv6 адресами для функции обработки IPv4.
        Проверяет, вызывается ли исключение ValueError при обработке файла с смешанными IP-адресами.
        """
        content = "192.168.1.1\n2001:db8::1"
        temp_file_path = self.write_to_temp_file(content)
        ip_addresses = read_ip_addresses_from_file(temp_file_path)
        with self.assertRaises(ValueError):
            minimal_subnet_from_ips(ip_addresses)
        os.unlink(temp_file_path)

    def test_minimal_subnet_single_ip(self):
        """Тестирование функции с одним IPv4-адресом."""
        ip_addresses = read_ip_addresses_from_file("data/ipv4_single_ip.txt")
        self.assertEqual(minimal_subnet_from_ips(ip_addresses), "192.168.1.1/32")

    def test_minimal_subnet_multiple_ips(self):
        """Тестирование функции с несколькими IPv4-адресами."""
        ip_addresses = read_ip_addresses_from_file("data/ipv4_multiple_ips.txt")
        self.assertEqual(minimal_subnet_from_ips(ip_addresses), "192.168.1.0/29")

    def test_minimal_subnet_empty_file(self):
        """Тестирование функции с пустым файлом."""
        ip_addresses = read_ip_addresses_from_file("data/empty_ips.txt")
        self.assertEqual(minimal_subnet_from_ips(ip_addresses), '')

    def test_minimal_subnet_invalid_ips(self):
        """Тестирование функции с файлом, содержащим невалидные IP-адреса."""
        ip_addresses = read_ip_addresses_from_file("data/ipv4_addresses_invalid.txt")
        with self.assertRaises(ValueError):
            minimal_subnet_from_ips(ip_addresses)


if __name__ == '__main__':
    unittest.main()
