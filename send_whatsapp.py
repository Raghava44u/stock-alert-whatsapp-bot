import os
from dotenv import load_dotenv
from twilio.rest import Client
from fetch_data import get_top_stocks
from generate_charts import generate_chart
from upload_to_imgur import upload_image_to_imgur

load_dotenv()

def send_whatsapp_message():
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_number = os.getenv("YOUR_WHATSAPP_NUMBER")
    imgur_client_id = os.getenv("IMGUR_CLIENT_ID")

    top_stocks = get_top_stocks()

    msg_text = "🔥 *Top Gaining US Stocks Today*\n\n"
    for idx, row in top_stocks.iterrows():
        msg_text += f"{row['symbol']}: ${row['current']} ({row['percent_change']}%)\n"

    msg_text += "\n📊 Charts will follow..."

    client.messages.create(
        from_=from_number,
        to=to_number,
        body=msg_text
    )

    for symbol in top_stocks["symbol"]:
        chart_path = generate_chart(symbol)
        if chart_path:
            image_url = upload_image_to_imgur(chart_path, imgur_client_id)
            if image_url:
                client.messages.create(
                    from_=from_number,
                    to=to_number,
                    body=f"📈 {symbol} Price Chart:",
                    media_url=[image_url]
                )
            else:
                client.messages.create(
                    from_=from_number,
                    to=to_number,
                    body=f"⚠️ Failed to upload {symbol} chart."
                )

if __name__ == "__main__":
    send_whatsapp_message()
