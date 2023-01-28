from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.
def getcontent(city):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city=city.replace(' ','+')
    html_content=session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content

def home(request):
    weatherdata=None
    if 'place' in request.GET:
        place=request.GET.get('place')
        if(place.isnumeric()):
            # pop up alert
            return HttpResponse('Please enter a valid place name')
        else:
            content=getcontent(place)
            if(content==None):
                return HttpResponse('Please enter a valid place name')
            else:
                soup=BeautifulSoup(content,'html.parser')
                weatherdata=dict()
                weatherdata['region']=soup.find('span',attrs={'class':'BNeawe tAd8D AP7Wnd'}).text
                weatherdata['temp']=soup.find('div',attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
                weatherdata['status']=soup.find('div',attrs={'class':'BNeawe tAd8D AP7Wnd'}).text
                return render(request,'core/home.html',{'weather':weatherdata})
    return render(request,'core/home.html')