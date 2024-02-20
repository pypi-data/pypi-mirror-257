from datetime import datetime
import pytz

# Get the timezone object for China
tz_SH = pytz.timezone("Asia/Shanghai")


def now() -> str:
    datetime_SH = datetime.now(tz_SH)
    return datetime_SH.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(now())
