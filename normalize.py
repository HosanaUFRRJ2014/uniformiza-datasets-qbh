import subprocess

from utils import (
    generate_name,
    build_command,
    get_result_name
)

__all__ = ["normalize"]


def write_correlation(file, old_path, new_file):
    file.write('{}\t{}\n'.format(old_path, new_file))


def normalize_songs(correlation_file, repo_path, songs_list, last_index=0):
    commands = []
    song_name_mapping = {}
    for id, song_path in enumerate(songs_list, last_index + 1):
        song_path = song_path.replace('\n', '')
        song_name = song_path.split('/')[-1].split('.mid')[0]
        new_file_name = generate_name(id)
        # correlation file
        write_correlation(
            correlation_file,
            repo_path + song_path,
            'songs/{}.mid'.format(new_file_name)
        )
        # print('{}\tsongs/{}'.format(song_path, new_file_name))

        song_name_mapping[song_name] = new_file_name

        # command
        path = 'songs/{}.mid'.format(new_file_name)
        command = build_command(repo_path + song_path, path)
        # print(command)
        commands.append(command)

    return id, commands, song_name_mapping


def normalize_queries(
    correlation_file, expected_results_file, repo_path,
    queries_list, song_mapping, last_index=0
):
    commands = []
    for id, query in enumerate(queries_list, last_index + 1):
        query = query.replace('\n', '')
        new_file_name = generate_name(id)

        # correlation file
        if repo_path == 'IOACAS_QBH/':
            old_name = query.split('\t')[0]
            query = 'waveFile/' + query.split('\t')[-1] + '.wav'
        else:
            old_name = query

        write_correlation(
            correlation_file, '{}{}'.format(repo_path, old_name),
            'queries/{}.wav'.format(new_file_name)
        )

        # Results
        result = get_result_name(repo_path, query)
        expected_results_file.write(
            'queries/{}.wav\t{}\n'.format(new_file_name, song_mapping[result])
        )

        # command
        path = 'queries/{}.wav'.format(new_file_name)
        command = build_command(repo_path + old_name, path)
        commands.append(command)

    return id, commands


def normalize():
    mir_path = 'MIR-QBSH-corpus/'
    ioacas_path = 'IOACAS_QBH/'

    commands = []  # Acumulates all program commands
    _commands = []  # Receives commands from functions
    mir_song_mapping = {}
    ioacas_song_mapping = {}

    mir_songs_filepath = '{}midi.list'.format(mir_path)
    ioacas_songs_filepath = '{}midi.list'.format(ioacas_path)

    mir_queries_filepath = '{}query-wav.list'.format(mir_path)
    ioacas_queries_filepath = '{}query.list'.format(ioacas_path)

    with open(mir_songs_filepath, 'r') as ms:
        mir_song_list = ms.readlines()

    with open(ioacas_songs_filepath, 'r') as _is:
        ioacas_song_list = _is.readlines()

    with open(mir_queries_filepath, 'r') as mq:
        mir_query_list = mq.readlines()

    with open(ioacas_queries_filepath, 'r') as iq:
        ioacas_query_list = iq.readlines()

    # Saves the relationship between queries of the real dataset and
    # of the proposed dataset
    mir_song_correlation_file = open('mir_song_correlation_file.list', 'w')
    ioacas_song_correlation_file = open('ioacas_song_correlation_file.list', 'w')
    mir_query_correlation_file = open('mir_query_correlation_file.list', 'w')
    ioacas_query_correlation_file = open('ioacas_query_correlation_file.list', 'w')

    # normalize songs
    print('Listing songs...')
    last_index, _commands, mir_song_mapping = normalize_songs(
        mir_song_correlation_file, mir_path, mir_song_list
    )
    commands.extend(_commands)

    _, _commands, ioacas_song_mapping = normalize_songs(
        ioacas_song_correlation_file, ioacas_path, ioacas_song_list, last_index
    )
    commands.extend(_commands)
    # Saves all expected queries results
    expected_results_file = open('expected_results.list', 'w')

    # normalize queries
    print('Listing queries...')
    last_index, _commands = normalize_queries(
        mir_query_correlation_file, expected_results_file,
        mir_path, mir_query_list, mir_song_mapping
    )
    commands.extend(_commands)

    _last_index, _commands = normalize_queries(
        ioacas_query_correlation_file, expected_results_file,
        ioacas_path, ioacas_query_list, ioacas_song_mapping, last_index
    )
    commands.extend(_commands)

    # Generates unified midi songs list file
    commands.append("ls songs/ > midi_songs.list")

    # Execute copy commands
    print('Copying files...')
    for command in commands:
        # print command
        subprocess.run(command, shell=True)
