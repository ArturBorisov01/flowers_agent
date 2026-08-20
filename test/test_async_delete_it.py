import asyncio
import os
from dotenv import load_dotenv
import json

load_dotenv()

import httpx 


MAX_CONCURRENT_REQUESTS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def process_message(client, prompt, message_id):
    async with semaphore:
        print(f"[Поток] Сообщение #{message_id} пошло в обработку...")
        try:
            response = await client.post(
                url = "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json",
                },
                data = json.dumps({
                    "model": os.getenv("MODEL_NAME"),
                    "messages": [{"role": "user", "content": prompt}],
                    "reasoning": {"enabled": True, "effort": "minimal"}
                }),
                timeout=60.0
            )

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"[Готово] Сообщение #{message_id} обработано: {content}")
            return content

        except Exception as e:
            print(f"[Ошибка] Сообщение #{message_id} упало: {e}")
            return f"Error for #{message_id}"


async def generate(num: int) -> str:
    # Симулируем большой поток из 15 входящих сообщений
    input_prompts = [f"Напиши число {i} словами" for i in range(1, num)]
    
    async with httpx.AsyncClient() as client:
        tasks = [
            process_message(client, prompt, idx)
            for idx, prompt in enumerate(input_prompts, start=1)
        ]

        print(f"--- Запускаем поток из {len(tasks)} сообщений с лимитом в {MAX_CONCURRENT_REQUESTS} ---")

        results = await asyncio.gather(*tasks)

    print(f"----------------------------------------")
    print(f"Всего обработано сообщений: {len(results)}")
    return results

if __name__ == "__main__":
    num = 5
    asyncio.run(generate(num + 1))




# async def make_request(client, prompt, task_number):
#     print(f"[Старт] Запрос №{task_number} отправлен...")
#     start_task = time.time()
    
#     response = await client.post(
#         url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#             "Content-Type": "application/json",
#         },
#         data=json.dumps({
#             "model": os.getenv("MODEL_NAME"),
#             "messages": [{"role": "user", "content": prompt}],
#             "reasoning": {
#                 "enabled": True,
#                 "effort": "minimal"
#             }
#         }),
#         timeout=60.0
#     )
#     end_task = time.time()
#     result = response.json()
#     content = result["choices"][0]["message"]["content"]
    
#     print(f"[Финиш] Запрос №{task_number} вернулся за {end_task - start_task:.2f} сек.")
#     return content



# async def main():
#     start_total = time.time()
    
#     async with httpx.AsyncClient() as client:
        
#         # Описываем две разные задачи
#         task1 = make_request(client, "How many r's are in the word 'strawberry'?", 1)
#         task2 = make_request(client, "How many p's are in the word 'strawberry'?", 2)
        
#         print("--- Запускаем оба запроса параллельно ---")
#         # asyncio.gather запускает их одновременно и ждет выполнения обоих
#         results = await asyncio.gather(task1, task2)
#         print("----------------------------------------\n")
        
#         # Выводим результаты
#         print(f"Ответ 1: {results[0]}\n")
#         print(f"Ответ 2: {results[1]}\n")
        
#     end_total = time.time()
#     print(f"Всего затрачено времени на оба запроса: {end_total - start_total:.2f} сек.")

# asyncio.run(main())


