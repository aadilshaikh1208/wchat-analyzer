import re
import pandas as pd

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\u202f(?:AM|PM)\s-\s"
    print("Splitting messages...")
    messages = re.split(pattern, data)[1:]


    dates = re.findall(pattern, data)
    cleaned_dates = [d.replace(" - ", "") for d in dates]

    df = pd.DataFrame({'user_message': messages, 'date': cleaned_dates})
    print("DataFrame created. First 5 rows:")
    print(df.head())

    try:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')
    except Exception as e:
        print("❌ Error in datetime conversion:", e)
        return pd.DataFrame()

    users = []
    msgs = []

    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg)
        if len(entry) >= 3:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+ 1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period
    print("✅ DataFrame Created")

    return df
