from django.db import models

class Chat(models.Model):
    user_message = models.TextField()
    assistant_reply = models.TextField()
    prompt_type = models.CharField(max_length=50, choices=[("analysis", "Analysis"), ("resume", "Resume")])
    timestamp = models.DateTimeField(auto_now_add=True)
