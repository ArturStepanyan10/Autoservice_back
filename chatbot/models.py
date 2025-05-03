from django.contrib.postgres.search import SearchVector
from django.db import models


class FAQ(models.Model):
    question = models.CharField(max_length=500, unique=True, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                SearchVector('question', config='russian'),
                name='faq_search_idx'
            )
        ]

