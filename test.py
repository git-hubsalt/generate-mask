from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
# AWS_ACCESS
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

print(AWS_ACCESS_KEY_ID)
print(AWS_SECRET_ACCESS_KEY)
print(type(AWS_ACCESS_KEY_ID), type(AWS_SECRET_ACCESS_KEY))
