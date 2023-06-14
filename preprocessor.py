import re
import pandas as pd
from datetime import datetime


def preproces(data):
     pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[AP]M\s-\s'
     messages = re.split(pattern, data)[1:]
     dates = re.findall(pattern, data)
     dates = [date.replace('\u202f', '').replace(' - ', '') for date in dates]
     dates = [datetime.strptime(date, '%m/%d/%y, %I:%M%p').strftime('%Y-%m-%d %H:%M') for date in dates]
     df = pd.DataFrame({'user_message': messages, 'date': dates})
     users = []
     messages = []
     for message in df['user_message']:
         entry = re.split('([\w\W]+?):\s', message)
         if entry[1:]:  # user name
             users.append(entry[1])
             messages.append(" ".join(entry[2:]))
         else:
             users.append('group_notification')
             messages.append(entry[0])
     df['user'] = users
     df['message'] = messages
     df.drop(columns=['user_message'], inplace=True)
     df['Year'] = pd.to_datetime(df['date']).dt.year
     df['month']=pd.to_datetime(df['date']).dt.month_name()
     df['day']=pd.to_datetime(df['date']).dt.day
     df['hour']=pd.to_datetime(df['date']).dt.hour
     df['month_num'] = pd.to_datetime(df['date']).dt.month
     df['only_date'] = pd.to_datetime(df['date']).dt.date
     df['day_name'] = pd.to_datetime(df['date']).dt.day_name()
     df['minute']=pd.to_datetime(df['date']).dt.minute
     period = []
     for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

     df['period'] = period
     return df



