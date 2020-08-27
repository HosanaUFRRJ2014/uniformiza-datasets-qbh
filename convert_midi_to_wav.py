import subprocess

__all__ = ["convert"]

def convert(filenames_list):
    print("Converting songs...")
    midi_songs_list = []
    for filename in filenames_list:
        with open(filename, 'r') as ms:
            midi_songs_list.extend(
                ms.readlines()
            )

    for song in midi_songs_list:
        song = song.replace('\n', '')
        converted_song_name = song.split('/')[-1].replace('.mid', '.wav')
        command = 'timidity {} -Ow -o songs_wav/{}'.format(
            song, converted_song_name
        )
        # print(command)
        subprocess.run(command, shell=True)
