from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class FinnotechTokenBase(models.Model):
    token = models.TextField(unique=True, db_index=True)
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def revoke(self):
        self.is_active = False
        self.save()
    
    class Meta:
        abstract = True
        ordering = [
            "-updated_at",
        ]


class FinnotechRefresh(FinnotechTokenBase):     
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refresh_tokens")
       
    def __str__(self):
        return self.refresh

    class Meta:
        verbose_name = _("Finnotech Refresh")
        verbose_name_plural = _("Finnotech Refreshes")


class FinnotechToken(FinnotechTokenBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finnotech_refresh_tokens")
    ttl = models.IntegerField()
    refresh_token = models.ForeignKey(FinnotechRefresh, on_delete=models.CASCADE, related_name="finnotech_tokens")
    
    def remaining_ttl(self):
        return self.ttl - (timezone.now() - self.created_at).seconds
    
    def expires_at(self):
        return self.created_at + timezone.timedelta(seconds=self.ttl)
        
    def __str__(self):
        return self.token

    class Meta:
        verbose_name = _("Finnotech Token")
        verbose_name_plural = _("Finnotech Tokens")
