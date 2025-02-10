# SpotifyStats

One of my good friends was showing me an app that he paid a few dollars for. It showed him the complete history of his spotify account; his most listened to songs and artists and how many times/minutes he listened to each of them. I then come to find out that the data can actually be requested from Spotify for free. This means that the paid stats app is just providing the nice interface and data analysis. Each "song listen" in the Spotify data is just a json object, so a quick python script should give me the functionality I want. 

As of right now, the script will print:
- The top 50 most listened to songs, artists, and albums in the history of my (or any) spotify account, which was created in 2013. 
- The number of times I played a song that falls under each of these categories as well as the amount of minutes I spent listening.
- The total number of unique songs, artists, and albums that I've Listened to.
- The total number of minutes of music I've listened to on the account.
- The total number of songs I've listened to.

The data provided by Spotify includes every single time a song was played on your spotify account, even if just for a few seconds. Because of this, I filtered out songs that were not played for more than 30 seconds at a time. I do listen to some songs that are even shorter than that, so I made sure to only filter out these shorter play times if the "reason_end" field is not "endplay". The "endplay" value indicates that the reason that a song ended was because the song finished, and not because the user skipped to the next song, closed the app, etc. Another thing I noticed is that there was a song in my top 50 that had null values for the artist and song name, which may indicate that the song was taken off of Spotify. I filter out these songs too in my script. Finally, back in the day my sisters and mom used to share my Spotify account. The only artists in my top 50 that were common to me and my sisters/mom were easily identifiable, so I filtered them out too.
