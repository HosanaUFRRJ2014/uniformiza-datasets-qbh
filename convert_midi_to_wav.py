import subprocess

with open('midi_songs.list', 'r') as ms:
    midi_songs_list = ms.readlines()


for song in midi_songs_list:
    song = song.replace('\n', '')
    converted_song_name = song.split('/')[-1].replace('.mid', '.wav')
    command = 'timidity {} -Ow -o songs_wav/{}'.format(
        song, converted_song_name
    )
    # print(command)
    subprocess.run(command, shell=True)
