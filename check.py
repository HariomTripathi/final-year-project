import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACf0227b3f25d89d9a7437e089f110696a"
auth_token = os.environ["3226380472cbe0c3509a7d4099d104f1"]
client = Client(account_sid, auth_token)

message = client.messages.create(
  body="Hello from Twilio",
  from_="+13855263051",
  to="+919653124327"
)

print(message.sid)