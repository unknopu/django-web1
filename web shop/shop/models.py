from django.db import models

# Create your models here.
class AddWallet_request(models.Manager):
    def waiting(self, is_verify, ref_id):
        try:
            data = self.get(ref_id=ref_id, is_verify=is_verify)
        except self.model.DoesNotExist:
            data = None
        return data
    
class NewWallet(models.Model):
    ref_id = models.CharField(max_length=200)
    time_stamp = models.DateTimeField(auto_now_add=True)    
    is_verify = models.BooleanField(default=False)    
    objects = AddWallet_request()