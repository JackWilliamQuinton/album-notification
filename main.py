import secrets
import json
import spotipy
import smtplib
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep
arctic_monkeys_id = '7Ln80lUS6He07XvHI8qqHH'

class Spotify:
    def __init__(self, artist_id):
        self.artist_id = artist_id
        self.connection = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets.client_id,
                                                                                client_secret=secrets.client_secret))
        self.latest_album = (self.connection.album(self.current_album_data()[arctic_monkeys_id][0]))

    def current_album_data(self): 
        album_dict = {self.artist_id:[]}
        album_data = self.connection.artist_albums(self.artist_id)
        for album in album_data['items']:
            album_dict[self.artist_id].append(album['id'])
        return album_dict

    def write_to_db(self, data):
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)

    def read_db(self):
        with open('database.json', 'r') as f:
            return json.load(f)

    def check_for_new(self):
        db = self.read_db()
        all_albums = self.current_album_data()
        if len(db[self.artist_id]) < len(all_albums[self.artist_id]):
            send_message(secrets.gmail_email, "jackwilliamquinton@gmail.com", message)
            print('Email sent')
            self.write_to_db(all_albums)
        print('No new album')

def send_message(sender_email, receiver_email, msg):
    with smtplib.SMTP_SSL("smtp.gmail.com") as server:
        server.login(secrets.gmail_email, secrets.gmail_password)
        server.sendmail(sender_email, receiver_email, msg)

spot = Spotify(arctic_monkeys_id)
message = f"From: New Album Update <{secrets.gmail_email}> \nSubject:{spot.latest_album['artists'][0]['name']} - {spot.latest_album['name']} \nFollow this link to be directed to the album\n{spot.latest_album['external_urls']['spotify']}"
spot.write_to_db(spot.current_album_data())
while True:
    spot.check_for_new()
    sleep(5)
