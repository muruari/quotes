from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = []

        if len(postData.get('name')) and len(postData.get('alias')) < 3:
            is_valid = False
            errors.append('Name and alias must have at least 3 characters each. Please try again.')

        if len(User.objects.filter(name = postData.get("name"))) > 0:
            is_valid = False
            errors.append('That name is already taken. Please try a different one.')

        if not re.search(r'^[a-z" "A-Z]+$', postData.get('name')):
            is_valid = False
            errors.append('Name must be alphabetical characters only. Please try again.')

        if len(postData.get('password')) < 5:
            is_valid = False
            errors.append('Passwords must have at least 6 characters. Please try again.')

        if postData.get('password_confirmation') != postData.get('password'):
            is_valid = False
            errors.append('Passwords do not match. Please try again.')
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    date_of_birth = models.DateField(default = 'none')    
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __str__(self):
        return "name:{}, alias:{}, email:{}, date_of_birth:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.alias, self.email, self.date_of_birth, self.password, self.created_at, self.updated_at)



class QuoteManager(models.Manager):
    def validate_quote(self, postData):
        errors = []

        if len(postData.get('quote_by')) or len(postData.get('quote_text_input')) < 3:
            is_valid = False
            errors.append('Both Quoted By and /Message fields must have at least 3 characters each. Please try again.')

        return errors


class Quote(models.Model):
    quoter = models.CharField(max_length = 255)
    quote_text = models.CharField(max_length = 255)    
    quotes = models.ManyToManyField(User, related_name="all_quotes")
    posted_by = models.ForeignKey(User, related_name="posted_by")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()











