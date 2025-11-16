# vanity_evm_generator.py
import os
import hashlib
import eth_keys
from eth_keys import keys
import time
from typing import Optional

# -------------------------------
# КРАСИВЫЕ ШАБЛОНЫ (можно расширять)
# -------------------------------
PATTERNS = [
    "0x000",      # начинается с 000
    "0x111",      # начинается с 111
    "0xabc",      # содержит abc
    "0xdead",     # содержит dead
    "0xbeef",     # содержит beef
    "0x123",      # содержит 123
    "0xaaa",      # три одинаковые
    "0x888",      # три восьмёрки
    "0x999",      # три девятки
    "0x4242",     # повторяющийся паттерн
    "0x6969",     # мем
    "0xc0de",     # code
    "0xbabe",     # babe
]

def generate_private_key() -> str:
    """Генерирует случайный 256-битный приватный ключ в hex."""
    return keys.PrivateKey(os.urandom(32)).to_hex()

def private_to_address(private_key_hex: str) -> str:
    """Преобразует приватный ключ в адрес EVM (checksum)."""
    private_key_bytes = bytes.fromhex(private_key_hex[2:])  # убираем 0x
    private_key = keys.PrivateKey(private_key_bytes)
    public_key = private_key.public_key
    address = public_key.to_checksum_address()
    return address.lower()  # для удобного поиска

def is_vanity_address(address: str) -> Optional[str]:
    """Проверяет, соответствует ли адрес хотя бы одному шаблону."""
    address_lower = address.lower()
    for pattern in PATTERNS:
        if pattern[2:] in address_lower[2:]:  # игнорируем 0x
            return pattern
    return None

def generate_vanity_wallet() -> dict:
    """Генерирует один красивый кошелёк."""
    while True:
        private_key = generate_private_key()
        address = private_to_address(private_key)
        pattern = is_vanity_address(address)
        if pattern:
            return {
                "private_key": private_key,
                "address": address,
                "pattern": pattern,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

def save_wallet(wallet: dict, filename: str = "vanity_wallets.txt"):
    """Сохраняет кошелёк в файл."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Найден красивый кошелёк!\n")
        f.write(f"Время: {wallet['timestamp']}\n")
        f.write(f"Паттерн: {wallet['pattern']}\n")
        f.write(f"Адрес: {wallet['address']}\n")
        f.write(f"Приватный ключ: {wallet['private_key']}\n")
        f.write(f"{'='*60}\n")
    print(f"Найден! {wallet['pattern']} → {wallet['address']}")

# -------------------------------
# ОСНОВНОЙ ЦИКЛ
# -------------------------------
if __name__ == "__main__":
    print("Генератор красивых EVM-кошельков запущен...")
    print("Ищем адреса с паттернами:", ", ".join(PATTERNS))
    print("Нажмите Ctrl+C для остановки.\n")

    found = 0
    start_time = time.time()

    try:
        while True:
            wallet = generate_vanity_wallet()
            save_wallet(wallet)
            found += 1
            elapsed = time.time() - start_time
            print(f"Найдено: {found} | Время: {elapsed:.1f} сек | Скорость: {found/elapsed:.2f} шт/сек")
    except KeyboardInterrupt:
        print(f"\nОстановлено. Найдено кошельков: {found}")
