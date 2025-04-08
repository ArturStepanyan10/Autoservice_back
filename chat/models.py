from django.db import models

from aservice.models import Appointment, User


class Conversation(models.Model):
    sender = models.ForeignKey(User, related_name='sent_conversations', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_conversations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.last_name + ' -> ' + self.receiver.last_name


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.user.last_name + ': ' + self.text
