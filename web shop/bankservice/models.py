from django.db import models

class UserManager(models.Manager):
    def add_user(self, user_ref_id, username, password, email, fullname, identity_number, pin):
        AddUser = self.create(user_ref_id=user_ref_id, 
                        username=username, 
                           password=password, 
                                email=email,
                                    fullname=fullname, 
                                        identity_number=identity_number,
                                            pin=pin)
    
    def get_user(self, username, password):
        try:
            user = self.get(username=username, password=password)
        except self.model.DoesNotExist:
            user = None
        return user
    
    def get_user_by_name(self, username):
        try:
            user = self.get(username = username)
        except self.model.DoesNotExist:
            user = None
        return user
    
    def get_user_by_id(self, user_ref_id):
        try:
            user = self.get(user_ref_id = user_ref_id)
        except self.model.DoesNotExist:
            user = None
        return user
    

class keyGetter(models.Manager):
    def publicKey(self, user_ref_id):
        user_key = self.get(user_ref_id=user_ref_id)
        return user_key.e, user_key.n
    
    def privKey(self, user_ref_id):
        user_key = self.get(user_ref_id=user_ref_id)
        return user_key.d, user_key.n

# Create your models here.
class user_model(models.Model):
    user_ref_id = models.CharField(max_length=200, unique=True, verbose_name='userRefId')
    fullname = models.CharField(max_length=200, verbose_name='fullname')
    username = models.CharField(max_length=200, verbose_name='username')
    password = models.CharField(max_length=200, verbose_name='password')
    email = models.CharField(max_length=100, verbose_name='email')
    identity_number = models.CharField(max_length=100, verbose_name='idnumber')
    pin = models.CharField(max_length=200, verbose_name='pin')
    account_balance = models.FloatField(default=0.0, verbose_name='accountBalance')
    
    objects = UserManager()
    
    class Meta:
        db_table = '_user_'

    def __str__(self):
        return "ALL USER"

class personalKey(models.Model):
    user_ref_id = models.CharField(max_length=200, unique=True, verbose_name='userRefId')
    e = models.CharField(max_length=8)
    d = models.CharField(max_length=259)
    n = models.CharField(max_length=259)
    objects = keyGetter()

class transactionManager(models.Manager):
    def get_by_ref_id(self, ref_id):
        data = self.get(ref_id=ref_id)
        return data
    def get_by_sender(self, sender):
        try:
            data = self.get(from_user=sender)
        except:
            data = None
        return data
    
    def get_by_recv(self, recv):
        data = self.get(to_user=recv)
        return data
    
class transaction(models.Model):
    ref_id = models.CharField(max_length=200, unique=True)
    from_user = models.CharField(max_length=200)
    to_user = models.CharField(max_length=200)
    amount = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=200)
    time_stamp = models.DateField(auto_now_add=True)     
    is_verify = models.BooleanField()    
     
          
