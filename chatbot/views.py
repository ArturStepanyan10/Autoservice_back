import requests
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
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

        auto_service_info = """
        Это автосервис Автомастер, предоставляющий услуги по ремонту и обслуживанию автомобилей. 
        Мы работаем с такими марками как отечественные например лада, волга, газ, так и иностранные марки также 
        к примеру BMW, Fiat, Toyota и так далее.
        У нас есть только мобильное приложение, в котором можно записываться на обслуживание выбрав услугу. 
        Также нам можно позвонить по номеру +7 900 589 52 17
        """

        payload = {
            "model": "deepseek/deepseek-r1",
            "messages": [
                {"role": "system", "content": "Ты виртуальный помощник мобильного приложения автосервиса."},
                {"role": "user", "content": f"{auto_service_info}\n\nВопрос клиента: {question}"}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            print(response_data)
            return response_data["choices"][0]["message"]["content"] if "choices" in response_data else None
        except Exception as e:
            print(f"Ошибка запроса DeepSeek: {e}")
            return None
