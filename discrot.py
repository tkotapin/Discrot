import time
import requests
from alive_progress import alive_bar
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Securely retrieve the token and channel ID
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("Error: Missing environment variables. Check your .env file.")
    exit(1)

# Adjusted headers for personal token
HEADERS = {
    "Authorization": f"{TOKEN}",
    "Content-Type": "application/json"
}

# Trigger words and natural responses
TRIGGER_RESPONSES = {
    "hello": "Yo, what up dawg? Hope ya vibin' good!",
    "hi": "Heyyy, what’s crackin’?",
    "bye": "Aight, peace out homie! Stay fly!",
    "i'm sad": "Aw snap, what’s messin’ with ya vibe? Hit me up, I gotchu!",
    "i'm happy": "Yasss! Keep that glow up poppin', fam!",
    "sup": "Yo, what’s poppin’ playa?",
    "yo": "Yo yo yo! Spill the deets, fam!",
    "what's up": "Ain’t much, just chillin’. How ‘bout you?",
    "brb": "Aight, bounce back soon tho!",
    "gtg": "Cool, see ya on the flip side!",
    "lol": "Haha fr, that’s jokes!",
    "lmao": "Brooo, I’m rollin’ over here!",
    "wyd": "Just kickin’ it, you?",
    "idk": "Fair, sometimes life’s a mystery bruh!",
    "ikr": "Frfr, it’s wild out here!",
    "omg": "Brooo, spill the tea ASAP!",
    "yolo": "Straight up, live it large, fam!",
    "no cap": "No lie, that’s the truth, facts only!",
    "bet": "Say less, I’m with ya!",
    "lit": "That’s fire, dawg! Keep it turnt!",
    "fam": "Yo fam, what’s the 411?",
    "vibe": "Catchin’ them vibes, stay smooth!",
    "sus": "Sussy af, explain yoself!",
    "mood": "Big mood, I’m feelin’ that!",
    "deadass": "No cap, straight facts!",
    "slay": "Yooo, you straight up slayin’, boo!",
    "bffr": "Be fr rn, stop playin’!",
    "nah": "Nah fam, no way!",
    "bro": "Yo bro, what’s the tea?",
    "sis": "Hey sis, spill the deets!",
    "ayy": "Ayyooo, let’s get it!",
    "tf": "Bruh, wtf is even goin’ on?",
    "hbu": "I’m vibin’, you?",
    "tbh": "Tbh, you spittin’ facts, no lies!",
    "jk": "Haha, ya got me! Nice one!",
    "ngl": "Ngl, you right tho!",
    "on god": "Swear down, facts only!",
    "oop": "Big oop, feels bad man!",
    "shook": "I’m shooketh, wtf fam!",
    "extra": "Bruh, you extra af but I’m here for it!",
    "tea": "Spill that hot tea, fam!",
    "cringe": "Big yikes, that’s cringy af!",
    "mfw": "My face rn… can’t even!",
    "irl": "Frfr, real talk tho!",
    "bruh": "Bruhhhh, no way!",
    "smh": "Shakin’ my head, can’t believe this!",
    "pog": "Poggers! That’s hype af!",
    "based": "Facts, that’s based af!",
    "yeet": "Yeet! Catchin’ vibes!",
    "oof": "Oof, that hits hard!",
    "gg": "GG fam, that was lit!",
    "ez": "Ez clap, ya crushed it!",
    "noob": "Bruh, we all start somewhere. Keep grindin’!",
    "pro": "You pro af, no lies!",
    "clutch": "Big clutch, MVP vibes!",
    "rekt": "Straight up rekt! GG no re!",
    "whack": "That’s hella whack, smh!",
    "dope": "Mad dope, keep it real!",
    "boom": "Boom, headshot vibes!",
    "goat": "Frfr, you the GOAT!",
    "cap": "Cap, big lies detected!",
    "bussin": "Sheeesh, that’s bussin’ no cap!",
    "chill": "Stay chill fam, don’t trip!",
    "swag": "Drippin’ swag, keep flexin’!",
    "thirsty": "Bruh, grab some water and chill!",
    "woke": "Stay woke fam, it’s real out here!",
    "lowkey": "Lowkey tho, I feel ya!",
    "highkey": "Highkey, you spittin’ facts!",
    "savage": "You savage af, keep slayin’!",
    "gucci": "All Gucci here, hope you good too!",
    "hype": "Big hype, keep it goin’!",
    "noice": "Noiceee, that’s clean!",
    "flex": "Big flex, respect bruh!",
    "cracked": "Straight cracked, you insane!",
    "dubs": "Dubs only fam, keep grindin’!",
    "vibes": "Good vibes only, let’s keep it rollin’!",
    "goofy": "Lol, you goofy af but we love it!",
    "drip": "Drippin’ too hard, keep killin’ it!",
    "fire": "Straight fire, no cap!",
    "boss": "Boss moves, keep leadin’ the way!",
    "lag": "Big lag, rip fam!",
    "tryhard": "Chill fam, it’s not that deep!",
    "afk": "Catch you when you back, fam!",
    "pogchamp": "Certified PogChamp moment!",
    "boosted": "Boosted af, but we all been there!",
    "weeb": "Big anime vibes, what you watchin’?",
    "simp": "Bruh, stop simpin’, c’mon!",
    "sus": "Hella sus, what’s the real tea?",
    "op": "That’s mad OP, nerf incoming!",
    "cheese": "Mad cheesy, but I’m into it!",
    "meh": "Meh, coulda been better!",
    "rip": "RIP fam, feels bad!",
    "fr": "Frfr, facts only fam!",
    "troll": "Haha, big troll energy!",
    "hacker": "Hackerman vibes, respect!",
    "rekt": "Rekt ‘em hard, no lie!",
    "wtf": "Yo, wtf just happened?!",
    "gg ez": "GG EZ, light work fam!",
    "ez clap": "Ez clap, you too OP!",
    "boost": "Boosted vibes, but we move!",
    "struggle": "Big struggle bus, but keep grindin’!",
    "wth": "Wth fam, that’s wild!",
    "omw": "On my way fam, hold tight!",
    "glhf": "Good luck, have fun! Let’s win!",
    "xd": "XD moment, can’t stop laughin’!",
    "ay": "Ayyy, let’s vibe fam!",
    "yikes": "Big yikes, what’s goin’ on?!",
    "bad": "Bruh, bad moves but you good!",
    "carry": "Straight carry vibes, MVP!",
    "bot": "Don’t be a bot fam, let’s go!",
    "trap": "Watch out fam, big trap vibes!",
    "pro play": "That’s mad pro play, GG fam!",
    "nerf": "Need a nerf ASAP, too OP!",
    "buff": "Buff it up fam, we need power!",
    "team": "Big team diff, regroup and go!",
    "clown": "Don’t clown me like that fam, haha!",
    "toxic": "Bruh, no need for toxic vibes!",
    "sweat": "Sweatin’ hard fam, chill a bit!",
    "meta": "That’s mad meta, good play!",
    "hardstuck": "Big hardstuck vibes, but keep grindin’!",
    "rank": "Rank diff, but you’ll climb!",
    "adc": "Big ADC vibes, keep carryin’!",
    "mid": "Mid diff is real, GG!",
    "jg": "Big jungle diff, keep it movin’!",
    "top": "Top gap huge, keep flexin’!",
    "feed": "Stop feedin’ fam, let’s win!",
    "camp": "Mad camp energy, stay safe!",
    "gank": "Nice gank fam, keep pushin’!",
    "play": "Solid play, keep it up!",
    "throw": "Bruh, stop throwin’, we got this!",
    "macro": "Macro diff, but we climb!",
    "micro": "Micro on point, respect!",
    "gap": "Big gap, you the MVP!"
}

# Function to test the token
def test_personal_token():
    url = "https://discord.com/api/v10/users/@me"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Token is valid! Logged in as: {response.json()['username']}")
    else:
        print(f"Token test failed: {response.status_code} - {response.text}")
        exit(1)

# Test the personal token
test_personal_token()

# Function to send a message to the channel
def send_message(content, reply_to_message_id=None):
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    data = {"content": content}
    if reply_to_message_id:
        data["message_reference"] = {"message_id": reply_to_message_id}
    response = requests.post(url, headers=HEADERS, json=data)
    if response.ok:
        print(f"Sent: {content}")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

# Function to fetch the latest message from the channel
def get_latest_message():
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=1"
    response = requests.get(url, headers=HEADERS)
    if response.ok:
        return response.json()[0]  # Return the latest message
    else:
        print(f"Failed to fetch messages: {response.status_code} - {response.text}")
        return None

# Main loop to monitor the channel and respond to trigger words
def main():
    last_message_id = None

    while True:
        try:
            # Reduced delay to improve response time
            with alive_bar(1000, title="Monitoring messages", bar=None, spinner="dots") as bar:
                while True:
                    time.sleep(10)  # Reduced sleep interval for faster message processing
                    bar()  # Advance the progress spinner

                    # Check for new messages
                    message = get_latest_message()
                    if message:
                        # Check if the message is new
                        if message['id'] != last_message_id:
                            last_message_id = message['id']
                            content = message['content'].lower()  # Convert message to lowercase
                            author_id = message['author']['id']

                            # Avoid responding to your own messages
                            if author_id not in (os.getenv("BOT_USER_ID"), TOKEN):
                                for trigger, response in TRIGGER_RESPONSES.items():
                                    if trigger in content:
                                        send_message(response, reply_to_message_id=message['id'])
                                        break  # Stop checking further triggers
                        break  # Exit the spinner loop when a new message is fetched

        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(20)  # Reduced wait time before retrying

# Run the script
if __name__ == "__main__":
    main()
