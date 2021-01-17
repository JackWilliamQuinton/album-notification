import secret
import json
import spotipy
import smtplib
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
arctic_monkeys_id = '7Ln80lUS6He07XvHI8qqHH'

class Spotify:
    def __init__(self, artist_id):
        self.artist_id = artist_id 
        self.connection = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secret.client_id,
                                                                                client_secret=secret.client_secret))

    def current_album_data(self):  # Creates a dictionary for the DB with the artist ID as akey and a list of albums as the value.
        album_dict = {self.artist_id: []}
        album_data = self.connection.artist_albums(self.artist_id)
        for album in album_data['items']:
            album_dict[self.artist_id].append(album['id'])
        return album_dict

    def write_to_db(self, data):  # Writes a dictionary to the json DB.
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)

    def read_db(self):  # Reads the json DB.
        with open('database.json', 'r') as f:
            return json.load(f)

    def check_for_new(self): #  Checks the current albums on Spotify agaisnt the ones stored on the DB. Calls the email function if a new album is out.
        db = self.read_db()
        all_albums = self.current_album_data()
        if len(db[self.artist_id]) < len(all_albums[self.artist_id]):
            latest_album = (spot.connection.album(spot.current_album_data()[arctic_monkeys_id][0]))
            message = f"From: New Album Update <{secret.gmail_email}> \nSubject:{latest_album['artists'][0]['name']} - {latest_album['name']} \nFollow this link to be directed to the album\n{latest_album['external_urls']['spotify']}"
            send_message(secret.gmail_email, "jackwilliamquinton@gmail.com", message)
            print('email sent')
            self.write_to_db(all_albums)
        print('no new album')
    

def send_message(sender_email, receiver_email, msg):  # Opens a SMTP server via to connect to gmail and send a message. 
    with smtplib.SMTP_SSL("smtp.gmail.com") as server:
        server.login(secret.gmail_email, secret.gmail_password)
        server.sendmail(sender_email, receiver_email, msg)

spot = Spotify(arctic_monkeys_id)
while True:
    spot.check_for_new()
    sleep(5)
