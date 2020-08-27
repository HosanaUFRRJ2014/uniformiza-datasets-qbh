
def build_command(old_path, new_path):
    return 'cp {} {}'.format(old_path, new_path)


def generate_name(id):
    '''
    Generates a filename adding at most six left zeros.
    e.g: 000001 , 000045, etc
    '''
    max_zero_amount = 6
    str_id = str(id)
    amount_of_zeros = '0' * (max_zero_amount - len(str_id))
    return '{}{}'.format(amount_of_zeros, id)


def get_result_name(query):
    return query.split('/')[-1].replace('.wav', '')

