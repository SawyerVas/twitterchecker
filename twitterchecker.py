import tweepy

# Ваши ключи Twitter API
API_KEY = "ваш API ключ"
API_SECRET = "ваш секретный ключ API"
ACCESS_TOKEN = "ваш токен доступа"
ACCESS_TOKEN_SECRET = "ваш секретный токен доступа"

def authenticate_twitter():
    """Аутентификация в API Twitter"""
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
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
    # Пример: список аккаунтов для проверки
    accounts_to_check = ["Twitter", "InvalidAccount123", "elonmusk"]
    
    # Аутентификация
    api = authenticate_twitter()
    
    # Проверка аккаунтов
    valid_accounts = check_accounts(api, accounts_to_check)
    
    # Результаты
    print("\nВалидные аккаунты:")
    print(valid_accounts)

if __name__ == "__main__":
    main()
