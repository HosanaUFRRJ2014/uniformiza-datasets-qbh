import os
from argparse import (
    ArgumentParser,
    RawDescriptionHelpFormatter
)
from distutils.util import strtobool

from normalize import normalize
from expand import expand
from convert_midi_to_wav import convert

CHOICES_TO_MIDI_FILES = {
    "all": ["midi_songs.list", "midi_songs_expanse.list"],
    "only_mirex": ["midi_songs.list"],
    "only_lmd": ["midi_songs_expanse.list"]
}

def process_args():
    parser = ArgumentParser()

    default_normalize = True
    default_expand = True
    default_convert = "none"

    parser.add_argument(
        "--normalize_datasets",
        "-norm",
        type=strtobool,
        help=" ".join([
            "Normalize MIR-QBSH-corpus and IOACAS dataset,",
            "i.e normalize audios names and unify the data.",
            "Also correlates source datasets to the unified one. Default: ",
            str(default_normalize)
        ]),
        default=default_normalize
    )

    parser.add_argument(
        "--expand_dataset",
        "-expand",
        type=strtobool,
        help=" ".join([
            "Normalize lmd dataset, i.e,",
            "normalize audios names and add the data to the unified dataset.",
            "Also correlates source datasets to the expanded one. Default: ",
            str(default_expand)
        ]),
        default=default_expand
    )

    parser.add_argument(
        "--convert_midi_to_wav",
        "-convert",
        type=str,
        help=" ".join([
            "Convert songs from midi to wav, given a dataset choice, i.e,",
            "normalize audios names and add the data to the unified dataset.",
            "Default: ",
            str(default_convert)
        ]),
        choices=["all", "only_mirex", "only_lmd", "none"],
        default=default_convert
    )


    args = parser.parse_args()

    normalize_datasets = args.normalize_datasets
    expand_dataset = args.expand_dataset
    conversion_mode = args.convert_midi_to_wav
    conversion_mode = None if conversion_mode == "none" else conversion_mode

    # return num_audios, min_tfidf
    return normalize_datasets, expand_dataset, conversion_mode


def validate_options(normalize_datasets, expand_datasets, conversion_mode):
    is_valid = True
    message = ""
    if conversion_mode:
        required_files = CHOICES_TO_MIDI_FILES[conversion_mode]
        is_valid = all(
            os.path.exists(filename)
            for filename in required_files
        ) or (expand_datasets and conversion_mode == "only_lmd")

        if not is_valid:
            message = " ".join([
                "You must perform at least normalization step before converting",
                "midi songs to wav.",
                "If you're trying to convert the expanded dataset, you must",
                "execute dataset expansion first.\n"
            ])

    if expand_datasets:
        normalization_done = os.path.exists("expected_results.list")
        is_valid = is_valid and normalization_done
        if not normalization_done:
            message += " ".join([
                "You must perform dataset normalization before",
                "trying to expand the dataset."
            ])

    
    if not is_valid:
        raise Exception(message)
    


def main():
    normalize_datasets, expand_datasets, conversion_mode = process_args()

    print(normalize_datasets, expand_datasets, conversion_mode)

    validate_options(
        normalize_datasets,
        expand_datasets,
        conversion_mode
    )

    if normalize_datasets:
        # Do mir/ioacas dataset unification and normalization
        normalize()
    if expand_datasets:
        # Apply algorithm to expand dataset (includes name normalization)
        # verify if the above step is done
        expand()
    if conversion_mode:
        midi_filenames = CHOICES_TO_MIDI_FILES[conversion_mode]
        convert(midi_filenames)




if __name__ == "__main__":
    main()