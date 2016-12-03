import requests
import datetime
import json


def tvlisting(channel):
    t=datetime.datetime.now()
    channel=channel.lower()
    channel=channel.replace(" ","-")
    print channel
    year=str(t.year)
    day=t.day
    month=t.month
    if day<10:
        day="0"+str(day)
    if month<10:
        month="0"+str(month)

    date=str(day)+str(month)+year
    tv=requests.get("http://indian-television-guide.appspot.com/indian_television_guide?channel="+channel+"&date="+date)
    content=json.loads(tv.content)
    time=roundofftime(t)
    shows=content["listOfShows"]

    for show in shows:
        if (show["showTime"]==time):
            return show["showTitle"]







def roundofftime(t):
    hour=t.hour
    minute=t.minute
    second="00"

    if (minute)<=30:
        minute="00"

    else:
        minute="30"


    time=str(hour)+":"+str(minute)+":"+str(second)

    return time
