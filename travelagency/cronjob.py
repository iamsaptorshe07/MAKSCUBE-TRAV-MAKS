from datetime import date
import datetime
from .models import *
def autoPublish():
    today = date.today() - datetime.timedelta(days=2)
    for user in Tour.objects.filter(creationDate=date.today() ,publish_mode=False):
        user.publish_mode = True
        user.save()