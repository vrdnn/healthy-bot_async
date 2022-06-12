import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS").split(',')
IP = os.getenv("ip")
DATABASE_URL = os.getenv("DATABASE_URL")

TIMEZONE = os.getenv("TIMEZONE")

TIME_BETWEEN_NOTIFICATION_UPDATES = int(os.getenv("TIME_BETWEEN_NOTIFICATION_UPDATES", 60))
