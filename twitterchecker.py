import tweepy
import json
import asyncio
import aiohttp
from aiofiles import open as aio_open

# Настройки
PROXY_FILE = "proxies.txt"
TOKEN_FILE = "tokens.txt"
LOG_FILE = "checker.log"
ACCOUNTS_FILE = "accounts_to_check.txt"

async def load_file(filename):
    """Загружает данные из файла"""
    async with aio_open(filename, 'r', encoding='utf-8') as file:
        return await file.read()

def authenticate_twitter(api_key, api_secret, access_token, access_token_secret, proxy=None):
    """Аутентификация в API Twitter с использованием прокси"""
    auth = tweepy.OAuthHandler(api_key, api_secret, proxy=proxy)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

async def check_account(api, account, session, proxy):
    """Проверяет валидность аккаунта Twitter"""
    try:
        user = api.get_user(screen_name=account)
        result = f"Аккаунт @{account} валиден. Имя: {user.name}\n"
    except tweepy.TweepError as e:
        result = f"Аккаунт @{account} не найден или ошибка: {e}\n"
    await log_result(result)
    return result

async def log_result(result):
    """Записывает результат в лог"""
    async with aio_open(LOG_FILE, 'a', encoding='utf-8') as log_file:
        await log_file.write(result)

async def main():
    # Загрузка данных
    tokens = json.loads(await load_file(TOKEN_FILE))
    proxies = (await load_file(PROXY_FILE)).splitlines()
    accounts = (await load_file(ACCOUNTS_FILE)).splitlines()

    # Перебор токенов и прокси
    async with aiohttp.ClientSession() as session:
        for token in tokens:
            for proxy in proxies:
                print(f"Проверяем с использованием токена: {token['API_KEY']} и прокси: {proxy}")
                try:
                    api = authenticate_twitter(
                        token["API_KEY"],
                        token["API_SECRET"],
                        token["ACCESS_TOKEN"],
                        token["ACCESS_TOKEN_SECRET"],
                        proxy=proxy
                    )
                    # Асинхронная проверка аккаунтов
                    tasks = [check_account(api, account, session, proxy) for account in accounts]
                    results = await asyncio.gather(*tasks)
                    print("\n".join(results))
                    return  # Если успешно, завершаем проверку
                except tweepy.RateLimitError:
                    print("Лимит запросов исчерпан. Пробуем следующий прокси.")
                except Exception as e:
                    print(f"Ошибка с токеном или прокси: {e}")
    print("\nПроверка завершена.")

if __name__ == "__main__":
    asyncio.run(main())
