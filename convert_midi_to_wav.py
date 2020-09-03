import subprocess

__all__ = ["convert"]


MIDI_TO_WAV_LIST = {
    "midi_songs.list": "wav_songs.list",
    "midi_songs_expanse.list": "wav_songs_expanse.list"
}


def write_wav_list(song_midi_path, converted_names):
    song_wav_list_filename = MIDI_TO_WAV_LIST[song_midi_path]
    with open(song_wav_list_filename, 'w') as list_file:
        lines = [
            filename + '\n'
            for filename in converted_names
        ]
        list_file.writelines(lines)


def convert(filenames_list):
    print("Converting songs...")
    midi_songs = []
    for filename in filenames_list:
        with open(filename, 'r') as ms:
            midi_songs.extend(
                (
                    filename,
                    ms.readlines()
                )
            )

    commands = []
    for source, songs in midi_songs:
        converted_names = []
        for song in songs:
            song = song.replace('\n', '')
            converted_song_name = song.split('/')[-1].replace('.mid', '.wav')
            converted_song_pathname = 'songs_wav/{}'.format(
                converted_song_name
            )
            converted_names.append(converted_song_pathname)
            command = 'timidity {} -Ow -o {}'.format(
                song, converted_song_pathname
            )
            commands.append(command)
     
        write_wav_list(song_midi_path=source, converted_names=converted_names)

        
    for command in commands:
        subprocess.run(command, shell=True)
