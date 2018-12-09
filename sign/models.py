from django.db import models

# Create your models here.

#发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    participant_number= models.IntegerField()
    status= models.BooleanField()
    address= models.CharField(max_length=200)
    start_time = models.DateTimeField('events time ')
    create_time = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.name

    class Meta:
        db_table = "event"

#嘉宾表
class Guest(models.Model):
    event  = models.ForeignKey(Event)
    realname = models.CharField(max_length=64)

    phone =  models.CharField(max_length=16)

    email= models.EmailField()

    sign = models.BooleanField()


    create_time =models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guest"

    unique_together =("event" ,"phone")

    def __str__ (self):
        return self.realname
class User(models.Model):
    account = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    role = models.BooleanField()
    isdelete = models.BooleanField()
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


    def __str__ (self):
        return self.account#,self.username,self.phone
    class Meta:
        db_table = "user"
