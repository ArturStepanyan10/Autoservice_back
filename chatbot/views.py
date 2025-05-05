import requests
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from requests import HTTPError, RequestException
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from chatbot.models import FAQ
from chatbot.serializers import FAQSerializer


class FAQSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'error': 'Введите запрос'}, status=400)

        search_vector = SearchVector('question', config='russian')
        search_query = SearchQuery(query, config='russian')

        results = FAQ.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

        if results.exists():
            serializer = FAQSerializer(results, many=True)
            return Response(serializer.data)

        answer = self.ask_deepseek(query)
        if answer:
            faq_entry = FAQ.objects.create(question=query, answer=answer)
            serializer = FAQSerializer(faq_entry)
            return Response(serializer.data)

        return Response({'error': "Не удалось получить ответ"}, status=500)

    def ask_deepseek(self, question):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            'Authorization': f"Bearer {settings.API_KEY}",
            'Content-Type': 'application/json'
        }
        auto_service_info = (
            "Это автосервис Автомастер, предоставляющий услуги по ремонту и обслуживанию автомобилей. "
            "Мы работаем с такими марками как отечественные (Лада, Волга, ГАЗ) и иностранные (BMW, Fiat, "
            "Toyota и т.д.). Кроме этого в нашем автосервисе работают профессионалы, которые любят свое дело."
            "У нас есть только мобильное приложение, в котором можно записываться на обслуживание, "
            "выбрав услугу и время. Но помимо онлайн-записи, у нас также присутствует запись по звонку, либо приехав "
            "лично в автосервис: ******"
            "Также нам можно позвонить по номеру +7 900 589 52 17."

        )
        payload = {
            "model": "deepseek/deepseek-r1",
            "messages": [
                {"role": "system", "content": "Ты виртуальный помощник мобильного приложения автосервиса. "
                                              "Ты должен помогать клиентам по каким-то вопросам и отвечать по делу."},
                {"role": "user", "content": f"{auto_service_info}\n\nВопрос клиента: {question}"}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print("DeepSeek status:", response.status_code)
            print("DeepSeek response body:", response.text)

            response.raise_for_status()

            data = response.json()

            choices = data.get("choices")
            if not choices or not isinstance(choices, list):
                print("Unexpected response format:", data)
                return None

            return choices[0].get("message", {}).get("content")

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"Request error: {req_err}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None
