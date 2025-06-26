

import datetime

# Get current UTC time
current_utc_time = datetime.utcnow()


recorddatetime=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

print(recorddatetime)
