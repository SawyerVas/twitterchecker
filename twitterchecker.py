import tweepy
import json

def load_tokens(filename):
    """Загружает токены из файла"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def authenticate_twitter(api_key, api_secret, access_token, access_token_secret):
    """Аутентификация в API Twitter"""
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def check_accounts(api, accounts):
    """Проверяет, существуют ли указанные аккаунты Twitter"""
    valid_accounts = []
    for account in accounts:
        try:
            user = api.get_user(screen_name=account)
            print(f"Аккаунт @{account} валиден. Имя: {user.name}")
            valid_accounts.append(account)
        except tweepy.TweepError as e:
            print(f"Аккаунт @{account} не найден или ошибка: {e}")
    return valid_accounts

def main():
    # Загрузка токенов из файла
    tokens = load_tokens("tokens.txt")
    
    # Пример: список аккаунтов для проверки
    accounts_to_check = ["Twitter", "InvalidAccount123", "elonmusk"]

    # Перебор токенов
    for token in tokens:
        print(f"Проверяем с использованием токена: {token['API_KEY']}")
        api = authenticate_twitter(
            token["API_KEY"],
            token["API_SECRET"],
            token["ACCESS_TOKEN"],
            token["ACCESS_TOKEN_SECRET"]
        )
        try:
            valid_accounts = check_accounts(api, accounts_to_check)
            print("\nВалидные аккаунты:")
            print(valid_accounts)
            break  # Если успешно, выходим из цикла
        except tweepy.RateLimitError:
            print("Лимит запросов исчерпан. Пробуем следующий токен.")
        except Exception as e:
            print(f"Ошибка с токеном: {e}")
    
    print("\nПроверка завершена.")

if __name__ == "__main__":
    main()
