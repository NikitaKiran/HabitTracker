from .models import DefaultActivites, activitylog
from datetime import timedelta, date

def timewise_day(user_id, any_date): 
    labels=[]
    
    for instance in DefaultActivites.objects.filter(user=user_id):
        labels.append(instance.name)
    

    values=[0]*len(labels)

    for instance in activitylog.objects.filter(user=user_id, date=any_date):
        if instance.activity in labels:
            
            ind=labels.index(instance.activity)
            values[ind]=float(instance.duration)
            values[ind]=round(values[ind],1)
    return labels,values



def timewise_month(user_id, month1): 
    labels=[]
    
    for instance in DefaultActivites.objects.filter(user=user_id):
        labels.append(instance.name)
    year1=date.today().year

    values=[0]*len(labels)
    if month1>date.today().month :
        year1=date.today().year - 1
    
    for instance in activitylog.objects.filter(user=user_id, date__month=month1,date__year=year1):
        if instance.activity  in labels:
            
            ind=labels.index(instance.activity)
            values[ind]+=float(instance.duration)
            values[ind]=round(values[ind],1)
    return labels,values

def timewise_week(user_id, week_num): 
    labels=[]
    
    for instance in DefaultActivites.objects.filter(user=user_id):
        labels.append(instance.name)
    today_date=date.today()
    if week_num==0:
        week=[(today_date-timedelta(days=6)),today_date]
    elif week_num==1:
        week=[(today_date-timedelta(days=13)),(today_date-timedelta(days=7))]
    elif week_num==2:
        week=[(today_date-timedelta(days=20)),(today_date-timedelta(days=14))]
    elif week_num==3:
        week=[(today_date-timedelta(days=27)),(today_date-timedelta(days=21))]    

    values=[0]*len(labels)

    for instance in activitylog.objects.filter(user=user_id, date__range=week):
        if instance.activity in labels:
            
            ind=labels.index(instance.activity)
            values[ind]+=float(instance.duration)
            values[ind]=round(values[ind],1)
    return labels,values

def activity_weeks(user_id, activity_name):
    labels=['10 weeks ago','9 weeks ago','8 weeks ago','7 weeks ago','6 weeks ago','5 weeks ago','4 weeks ago','3 weeks ago','2 weeks ago','This Week']
    values=[0]*10
    today_date=date.today()

    #10 weeks
    range_date=[(today_date-timedelta(days=69)),today_date]
    week_10=[(today_date-timedelta(days=69)),(today_date-timedelta(days=63)),10]
    week_9=[(today_date-timedelta(days=62)),(today_date-timedelta(days=56)),9]
    week_8=[(today_date-timedelta(days=55)),(today_date-timedelta(days=49)),8]
    week_7=[(today_date-timedelta(days=48)),(today_date-timedelta(days=42)),7]
    week_6=[(today_date-timedelta(days=41)),(today_date-timedelta(days=35)),6]
    week_5=[(today_date-timedelta(days=34)),(today_date-timedelta(days=28)),5]
    week_4=[(today_date-timedelta(days=27)),(today_date-timedelta(days=21)),4]
    week_3=[(today_date-timedelta(days=20)),(today_date-timedelta(days=14)),3]
    week_2=[(today_date-timedelta(days=13)),(today_date-timedelta(days=7)),2]
    current_week=[(today_date-timedelta(days=6)), today_date,1]

    all_weeks=[week_10, week_2, week_3, week_4, week_5, week_6, week_7, week_8, week_9, current_week]

    for instance in activitylog.objects.filter(user=user_id, date__range=range_date,activity=activity_name):
            for week in all_weeks:
                if instance.date<=week[1] and instance.date>=week[0]:
                    ind=10-week[2]
                    values[ind]+=float(instance.duration)
                    values[ind]=round(values[ind],1)
    
    return labels,values

def activity_days(user_id, activity_name):
    labels=[]
    values=[0]*7
    today_date=date.today()
    week=[(today_date-timedelta(days=6)),today_date]
    dates_of_week=[(today_date-timedelta(days=6)),(today_date-timedelta(days=5)),(today_date-timedelta(days=4)),(today_date-timedelta(days=3)),(today_date-timedelta(days=2)),(today_date-timedelta(days=1)),today_date]
    
    for dt in dates_of_week:
        labels.append(str(dt))#Or, labels.append(date.weekday()) ,if days look better
        
    for instance in activitylog.objects.filter(user=user_id, date__range=week,activity=activity_name):
            ind=dates_of_week.index(instance.date)

            values[ind]+=float(instance.duration)
            values[ind]=round(values[ind],1)

    return labels,values

def activity_months(user_id, activity_name):
    labels=[]
    values=[0]*10
    all_months_num=[1,2,3,4,5,6,7,8,9,10,11,12]
    today_date=date.today()

    current_month_num=int(today_date.month)
    current_year=int(today_date.year)
    
    first_month_num=current_month_num-9
    if first_month_num<0:
        first_month_num+=12
        final_months_num=all_months_num[first_month_num-1:12]+all_months_num[0:current_month_num]
        first_year=current_year-1
    else:
        final_months_num=all_months_num[first_month_num-1:current_month_num]
        first_year=current_year

    range_date=[str(first_year)+'-'+str(first_month_num)+'-01', str(current_year)+'-12-31']
  
    for instance in activitylog.objects.filter(user=user_id, date__range=range_date,activity=activity_name):
            ind=final_months_num.index(int(str(instance.date)[5:7])) 
            values[ind]+=float(instance.duration) 
            values[ind]=round(values[ind],1)
            
    for num in final_months_num:
        labels.append(date(2000, num, 1).strftime('%b'))
    '''for num in final_months_num:
        for month in all_months:
            if month[1]==num:
                labels.append(month[0])'''        
    return labels,values



           