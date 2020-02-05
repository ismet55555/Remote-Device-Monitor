import os

hostname = "71.41.66.6"
port = '443'

# response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
response = os.system("nc -vz " + hostname + " " + port + " > /dev/null 2>&1")

# 256 is local network error
# 512 is remote offline

print(response)
if response == 0:
  print(hostname, 'is up!')
elif response == 256:
  print('Local internet connection issues')
else:
  print(hostname, 'is down!')




#################################################################




# import os
# import slack
# from datetime import datetime


# SLACK_API_TOKEN = 'xoxb-BLAH-BLAH'
# client = slack.WebClient(token=SLACK_API_TOKEN)


# ip = '192.168.0.13'
# status_text = 'DOWN'

# # Defining the message
# message_parts = [
#   '```'
#   '#################################################################',
#   '      ATTENTION: {}       '.format('blah'),
#   '#################################################################',
#   '  • Datetime:          {}'.format(datetime.now()),
#   '  • Router IP:         {}'.format(ip),
#   '  • Router Status:     {}'.format(status_text),
#   '#################################################################',
#   '```'
# ]
# # Comgining all parts
# message_text = "\n".join(message_parts)

# response = client.chat_postMessage(
#     channel='#testing_slack_stuff',
#     text=message_text)

# print(response['ok'])
# # assert response["ok"]
# # assert response["message"]["text"] == "Hello world!"