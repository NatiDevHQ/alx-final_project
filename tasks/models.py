from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    completed = models.BooleanField(_('Completed'), default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def __str__(self):
        return self.title
