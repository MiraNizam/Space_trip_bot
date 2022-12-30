# Space trip bot

**Space trip bot** Telegram channel that works with the participation of a telegram bot. 
The channel publishes photos from Spaсe_X API and NASA API. You can also add photos and **Space trip bot** publish them.

## Getting Started

Below you will find instructions on how to use **Space trip bot**.  

### Prerequisites

Please be sure that **Python3** is already installed. 

### Installing
1. Clone the repository:
```
git clone https://github.com/MiraNizam/Space_trip_bot.git
```
2. Create a new virtual environment env in the directory
```
python -m virtualenv env
```
3. Activate the new environment
```
source env/bin/activate
``` 
4. Use pip (or pip3, if there is a conflict with Python2) to install dependencies in new environment:
```
pip install -r requirements.txt
```
### How to use it:
#### The first part (NASA API and SpaceX API)

5. The scripts use API from two sites: Public [SpaceX API](https://github.com/r-spacex/SpaceX-API#readme) and Private NASA API.  

6. Now you need to generate your own unique **API Key** to do this, you need to fill the form on the site [api.nasa.gov](https://api.nasa.gov/).
You receive **API Key** on the Email.
7. Create **.env** file with unique environmental variable, that was generated above.

| NASA_KEY="unique value"    | 
|----------------------------|

#### The second part (Telegram API):

8. You need to create Telegram Bot and receive telegram - TOKEN:
   using [@BotFather](https://telegram.me/BotFather) in Telegram app push ```/newbot```, follow instructions, copy the token to access the HTTP API. 

9. After we create a telegram channel and assign the bot as its Administrator so that it can publish photos on the channel. This article will help: [How to create Telegram Channel](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

10. Add in **.env** file your unique token and chat_id.

| TG_TOKEN="unique value" | 
|-------------------------|
| TG_CHAT_ID="@chat_id"   |

Now everything is ready.

### How to run code:


The script takes the launch_id for spacex API as an argument or use "latest" as default meaning.
```
python3 main.py "5eb87d46ffd86e000604b388"
```

The script takes the interval for publishing photos as an argument or use 14400 seconds = 4 hours as default meaning.
```
python3 telegram_api.py 30
```

Enjoy Space!

### Project Goals
This code was written for educational purposes as part of an online course for web developers at dvmn.org.






