# Import necesary libraries --------------------
import random,math
from .models import AccountType
# Importing ends here ---------------------

# Genereting unique Id for travellers -------------
def travellerId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="e"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(userId=uniqueId).exists():
        uniqueId="k"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(userId=uniqueId).exists():
        uniqueId="s"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(userId=uniqueId).exists():
        uniqueId="r"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TMUSR',uniqueId])
# Genereting unique Id for travellers end here -------------

# Genereting unique Id for seller agency -------------
def sellerId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="k"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(agentId=uniqueId).exists():
        uniqueId="i"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(agentId=uniqueId).exists():
        uniqueId="y"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(agentId=uniqueId).exists():
        uniqueId="w"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TMAGE',uniqueId])
# Genereting unique Id for seller agency end here -------------

# Genereting unique Id for guide -------------
def guideId():
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="f"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(guideId=uniqueId).exists():
        uniqueId="l"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(guideId=uniqueId).exists():
        uniqueId="h"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if AccountType.objects.filter(guideId=uniqueId).exists():
        uniqueId="f"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TMGUI',uniqueId])
# Genereting unique Id for guide end here -------------
