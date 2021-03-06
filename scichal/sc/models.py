from django.db import models
from scichal.reg.models import JosUsers, JosContent
from pytz import timezone, utc

class Entrant(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    mentor_name = models.CharField(max_length=128)
    mentor_phone = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    comment = models.CharField("How heard about us", max_length=128)
    mentor_relation = models.CharField(max_length=128)
    postal = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    school_address = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    entry_year = models.IntegerField()
    user = models.ForeignKey(JosUsers, null=True, blank=True)
    
    def __unicode__(self):
    	return self.name

    def has_submitted(self):
    	c = JosContent.objects.filter(created_by=self.user.pk)
    	if len(c) > 0:
    		return True
    	else:
    		return False
    	
    def submitted(self):
    	c = JosContent.objects.filter(created_by=self.user.pk)
    	if len(c) > 0:
    	    return "CONT" + str(self.entry_year) + str(c[0].pk)
    	else:
    	    return "No"
    
    def date_registered(self):
    	utc_dt = utc.localize(self.user.registerdate)
    	user_tz = timezone('Australia/Melbourne')
    	user_dt = user_tz.normalize(utc_dt.astimezone(user_tz))
    	return user_dt.replace(tzinfo=None).strftime("%a %d %b, %I:%M %p")
    
    # Compatibility with existing email code
    def mentor(self):
    	return str(self.mentor_name)

class EmailMessage(models.Model):
	subject = models.CharField("Subject", max_length=256)
	body = models.TextField("Message Body")
	from_name = models.CharField("From Name", max_length=64)
	from_address = models.EmailField("From Address")
	reply_address = models.CharField("Reply Address", max_length=64)
	html = models.BooleanField("HTML", blank=True)
	
	def __unicode__(self):
		return self.subject
