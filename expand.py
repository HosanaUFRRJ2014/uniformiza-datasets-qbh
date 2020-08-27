import subprocess

from utils import (
    generate_name,
    build_command,
    get_result_name
)


def write_correlation(file, correlations):
    data = [
        '{}\t{}\n'.format(old_path, new_file)
        for old_path, new_file in correlations
    ]
    file.writelines(data)


def write_midi_list(lmd_midi_list_file, correlations):
    data = [
        new_file + '\n'
        for _old, new_file in correlations
    ]
    lmd_midi_list_file.writelines(data)


def get_last_index():
    """Gets last index of song from mirex normalization"""

    with open("midi_songs.list", "r") as midi_songs:
        last_song = midi_songs.readlines()[-1]
    
    last_index = last_song.split("/")[-1].replace(".mid", "")

    return int(last_index)


def normalize_expansion_songs(correlation_file, repo_path, songs_list, last_index):
    commands = []
    correlations = []
    for id, song_path in enumerate(songs_list, last_index + 1):
        song_path = song_path.replace('\n', '')
        song_name = song_path.split('/')[-1].split('.mid')[0]
        new_file_name = generate_name(id)

        # correlation
        old_path = repo_path + song_path
        new_filepath = 'songs/{}.mid'.format(new_file_name)
        correlations.append(
            (old_path, new_filepath)
        )
        # command
        command = build_command(repo_path + song_path, new_filepath)
        commands.append(command)


    # correlation file
    write_correlation(
        correlation_file,
        correlations
    )

    return commands, correlations


def expand():
    lmd_path = "lmd_matched/"
    lmd_songs_filepath = '{}midi.list'.format(lmd_path)
    
    with open(lmd_songs_filepath, 'r') as lmd:
        lmd_song_list = lmd.readlines()

    # Saves the relationship between queries of the real dataset and
    # of the proposed dataset
    lmd_song_correlation_file = open('lmd_song_correlation_file.list', 'w') 
    lmd_midi_list_file = open( 'midi_songs_expanse.list', 'w')   

    last_index = get_last_index()

    print('Listing expansion songs...')
    commands, correlations = normalize_expansion_songs(
        correlation_file=lmd_song_correlation_file,
        repo_path=lmd_path,
        songs_list=lmd_song_list,
        last_index=last_index
    )

    write_midi_list(lmd_midi_list_file, correlations)

    # Execute copy commands
    print('Copying files...')
    for command in commands:
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    expand()