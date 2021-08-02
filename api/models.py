from django.db import models

class group(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title

class questions(models.Model):
    question = models.CharField(max_length=200)
    group = models.ManyToManyField(group)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['question']

    def __str__(self):
        return self.question
