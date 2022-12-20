import telegram
import asyncio
import talib
import requests

# Replace YOUR_API_TOKEN with your Telegram bot's API token
bot = telegram.Bot(token='YOUR_API_TOKEN')

# Set the chat_id where you want to send the message
chat_id = 12345678

# Set the timeframe (in minutes) for checking the MACD line
timeframe = 15

async def main():
    # Set the previous price to None initially
    previous_price = None

    while True:
        # Send a GET request to the Bybit API to retrieve the latest MACD and signal line values
        url = 'https://api-testnet.bybit.com/v2/public/kline/list'
        params = {'symbol': 'BTCUSD', 'interval': f'{timeframe}m', 'limit': '1'}
        response = requests.get(url, params=params)
        data = response.json()
        macd = data['result'][0]['macd']
        signal = data['result'][0]['signal']

        # Use the crossover function from talib to check if the MACD line has crossed the signal line
        macd_crossed_signal = talib.crossover(macd, signal)

        # Check if the MACD line has crossed the signal line
        if macd_crossed_signal[-1] == 1:
            # MACD line crossed signal line upwards
            direction = 'upwards'
        elif macd_crossed_signal[-1] == -1:
            # MACD line crossed signal line downwards
            direction = 'downwards'
        else:
            # MACD line and signal line are equal, no crossing
            direction = None

        # Check if the price has risen or dropped since the last message
        last_price = data['result'][0]['close']
        if last_price > previous_price:
            # Price has risen
            price_change = 'risen'
        elif last_price < previous_price:
            # Price has dropped
            price_change = 'dropped'
        else:
            # Price has not changed
            price_change = 'not changed'

        # Save the current price as the previous price for the next iteration
        previous_price = last_price

        # If the MACD line crossed the signal line, send a message with the direction and price change
        if direction is not None:
            message = f'MACD line crossed signal line {direction}. Price has {price_change}.'
            bot.send_message(chat_id=chat_id, text=message)

        # Wait one minute before checking again
        await asyncio.sleep(60)

asyncio.run(main())

