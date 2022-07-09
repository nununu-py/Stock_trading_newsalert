import requests
from twilio.rest import Client

API_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": "FILL WITH YOURS",
}

url = "https://www.alphavantage.co/query?"
response = requests.get(url, params=API_PARAMETERS)
json_data = response.json()["Time Series (Daily)"]
list_data = [value for key, value in json_data.items()]
yesterday_data = list_data[0]
yesterday_data_closing = yesterday_data["4. close"]
print("yesterday closing : ", yesterday_data_closing)

day_before_yesterday = list_data[1]
day_before_yesterday_closing = day_before_yesterday["4. close"]
print("before yesterday closing : ", day_before_yesterday_closing)

difference_price = abs(float(yesterday_data_closing) - float(day_before_yesterday_closing))
difference_percentages = (difference_price/float(yesterday_data_closing)) * 100
format_diff_percent = "{:.2f}".format(difference_percentages)
print("Stock Diff : ", format_diff_percent)

icon = ""
if difference_price > 1:
    icon = "📈"
else:
    icon = "📉"

news_apikey = "FILL WITH YOURS"
NEWS_PARAMETERS = {
    "apiKey": news_apikey,
    "q": "Tesla"
}

if difference_percentages > 1:
    response = requests.get("https://newsapi.org/v2/top-headlines?", params=NEWS_PARAMETERS)
    news_articles = (response.json())["articles"]
    show_articles = news_articles[:3]
    send_message = [f"Title : {items['title']}, Description : {items['description']}, Url : {items['url']}"
                    for items in show_articles]

    account_sid = "FILL WITH YOURS"
    auth_token = "FILL WITH YOURS"

    client = Client(account_sid, auth_token)

    for article in send_message:
        message = client.messages.create(
                body=f'Tesla Stock : {icon}{format_diff_percent}%\n{article}',
                from_='FILL WITH YOURS',
                to='FILL WITH YOURS')
