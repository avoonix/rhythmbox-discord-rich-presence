from pypresence import Client
import time
import dbus
import re

bus = dbus.SessionBus()


def get_current_playing_song():
    try:
        for service in bus.list_names():
            # if re.match('org.mpris.MediaPlayer2.', service):
            if re.match("org.mpris.MediaPlayer2.rhythmbox", service):
                player = bus.get_object(service, "/org/mpris/MediaPlayer2")
                position = player.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "Position",
                    dbus_interface="org.freedesktop.DBus.Properties",
                )
                status = player.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "PlaybackStatus",
                    dbus_interface="org.freedesktop.DBus.Properties",
                )
                metadata = player.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "Metadata",
                    dbus_interface="org.freedesktop.DBus.Properties",
                )
                if status != "Playing":
                    return None
                return {
                    "title": str(metadata["xesam:title"]),
                    "artist": str(metadata["xesam:artist"][0]),
                    "genre": str(metadata["xesam:genre"][0]),
                    "length": int(metadata["mpris:length"]) / 1000000,
                    "position": int(position) / 1000000,
                }
    except:
        print("error")
    return None


def show_presence(RPC):
    connected = False
    while not connected:
        try:
            RPC.start()
            connected = True
        except:
            print("discord not started, reconnecting in 30s")
            time.sleep(30)

    last_song = None
    while True:
        song = get_current_playing_song()
        start_time = time.time()
        if song:
            if not (last_song and song["title"] == last_song["title"]):
                print(
                    RPC.set_activity(
                        details=f"{song['title']}",
                        state=f"by {song['artist']} ({song['genre']})",
                        start=start_time - song["position"],
                        large_image="music-note",
                        # small_image="music-note",
                        # party_id="myparty0",
                        # party_size=[current_party, max_party],
                        # join="partyjoin0",
                        # spectate="spectate0",
                        # match="match0",
                        instance=True,
                        buttons=[
                            {
                                "label": "Don't click this",
                                "url": "https://youtu.be/dQw4w9WgXcQ",
                            }
                        ],
                    )
                )
        else:
            RPC.clear_activity()
        last_song = song
        time.sleep(5)


def main():
    while True:
        try:
            RPC = Client("806910592983367730")
            show_presence(RPC)
        except KeyboardInterrupt:
            exit()
        except:
            print("rpc connection failed")


if __name__ == "__main__":
    main()
