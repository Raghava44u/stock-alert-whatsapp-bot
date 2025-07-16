import os
from dotenv import load_dotenv
from twilio.rest import Client
from fetch_data import get_top_stocks
from generate_charts import generate_chart

load_dotenv()

def send_whatsapp_message():
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_number = os.getenv("YOUR_WHATSAPP_NUMBER")

    top_stocks = get_top_stocks()

    msg_text = "🔥 *Top Gaining US Stocks Today*\n\n"
    for idx, row in top_stocks.iterrows():
        msg_text += f"{row['symbol']}: ${row['current']} ({row['percent_change']}%)\n"

    msg_text += "\n📊 Charts will follow (saved locally for now)..."

    client.messages.create(
        from_=from_number,
        to=to_number,
        body=msg_text
    )

    for symbol in top_stocks["symbol"]:
        chart_path = generate_chart(symbol)
        print(f"✅ {symbol} chart saved locally at {chart_path}")

if __name__ == "__main__":
    send_whatsapp_message()
