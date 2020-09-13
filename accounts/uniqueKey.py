# Import necesary libraries --------------------
import random,math
from .models import AccountType
# Importing ends here ---------------------

# Genereting unique Id for travellers -------------
def travellerId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="k"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(userId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(userId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(userId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TRAVMAKSUSER',uniqueId])
# Genereting unique Id for travellers end here -------------

# Genereting unique Id for seller agency -------------
def sellerId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="k"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(agentId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(agentId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(agentId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TRAVMAKSSELL',uniqueId])
# Genereting unique Id for seller agency end here -------------

# Genereting unique Id for guide -------------
def guidId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="k"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(guideId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(guideId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    if AccountType.objects.filter(guideId=uniqueId).exists():
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TRAVMAKSGUID',uniqueId])
# Genereting unique Id for guide end here -------------
