"""получает сообщение, применяет векторный поиск, 
возвращает контекст, + саммари и отвечает на вопрос по контексту """

from llm_service import process_message
import requests

URL = "http://192.168.2.102:3000/product/search"


async def make_request_search(query):
    params = {"limit": 5, "q": query}
    headers = {"accept": "*/*"}

    try:
        # 3. Выполняем сам запрос (добавлен timeout, чтобы поток не завис навсегда)
        response = requests.get(URL, headers=headers, params=params, timeout=5)
        
        # 4. Проверяем статус ответа сервера
        if response.status_code == 200:
            # Превращаем JSON-ответ в привычный словарь или список Python
            products = response.json()
            print("Запрос выполнен успешно!")
            return products
        else:
            print(f"Сервер вернул ошибку. Статус-код: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Обработка сетевых ошибок (например, если сервер 192.168.2.102 недоступен)
        print(f"Ошибка при запросе к серверу: {e}")

previos_summary = 'пользователь интересуется цветами'
json_forma = ''

async def chat_generation(query: str) -> str:
    search_result = await make_request_search(query)

    prompt = f"""
        Ты — профессиональный цветочный ассистент. Твоя задача — отвечать по контексту на новое сообщение. Контекст содержит в себе возвращаемые карточки товаров.
    
        Контекст:
        "{search_result}"
    
        Новое сообщение:
        "{query}"
    
        Инструкции:
        1. Отвечай только по контексту и ничего лишнего
        2. Пиши тезисно, в третьем лице, без лишней воды.
    
        Ответ должен содержать ТОЛЬКО ответ по контексту.
        """


    result = await process_message(prompt)
    return result


# if __name__ == "__main__":
#     num = 5
#     asyncio.run(bond_summary_message('новая ссесия', 'привет'))