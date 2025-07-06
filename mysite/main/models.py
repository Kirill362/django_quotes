from django.db import models
from django.core.exceptions import ValidationError


class Quote(models.Model):
    text = models.TextField(
        unique=True,
        error_messages={'unique': 'Эта цитата уже есть в пуле.'})
    source = models.CharField(max_length=200)
    weight = models.PositiveIntegerField(default=1)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def clean(self):
        same_source_quotes = Quote.objects.filter(source=self.source)
        if not self.pk and same_source_quotes.count() >= 3:
            raise ValidationError(f"Нельзя добавлять больше 3-х цитат для одного источника: {self.source}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)