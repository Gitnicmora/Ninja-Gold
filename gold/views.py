from django.shortcuts import render, redirect
from datetime import datetime
from pytz import timezone
import random,pytz

# Create your views here.

def index(request):
    if 'gold' not in request.session or 'activities' not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    context = {
        "activities": request.session['activities']
    }
    return render(request, 'index.html', context)

def reset(request):
    request.session.flush()
    return redirect('/')


def process_money(request):
    if request.method == 'POST':
        myGold = request.session['gold']
        activities = request.session['activities']
        form_name = request.POST['location']
        print('form_name:', form_name)

        if form_name == 'farm':
            current_gold = round(random.random() * 10 + 10)
        elif form_name == 'cave':
            current_gold = round(random.random() * 5 + 10)
        elif form_name == 'house':
            current_gold = round(random.random() * 3 + 2)
        else:
            winOrLose =round(random.random())
            if winOrLose == 1:
                current_gold = round(random.random() * 50)
                print("getting gold!")
            else:
                current_gold = (round(random.random() * 50) * -1)
                print("taking gold")

        date_format='%m/%d/%Y %H:%M:%S %Z'
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        myTime = date.strftime(date_format)

        myGold += current_gold
        request.session['gold'] = myGold
        print(current_gold)

        if current_gold >= 0:
            str = f"Earned {current_gold} gold from the {form_name} at {myTime}"
        else:
            str = f"Lost {current_gold} gold from the {form_name} at {myTime}"

        activities.append(str)
        request.session['activities'] = activities
        return redirect('/')
    else:
        if request.method == 'GET':
            return redirect('/')