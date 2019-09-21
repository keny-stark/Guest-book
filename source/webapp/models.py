from django.db import models
product_status_choices = [('active', 'active'), ('blocked', 'blocked')]


class BookGuest(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Name')
    text = models.TextField(max_length=2000, null=False, blank=False, verbose_name='Text')
    email = models.EmailField(max_length=100, null=False, blank=False, verbose_name='Email')
    status = models.CharField(max_length=40, null=False,
                              blank=False, choices=product_status_choices, default='active', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of add')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Time of update')

    def __str__(self):
        return self.name
