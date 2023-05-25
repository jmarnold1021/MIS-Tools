OPTIONS = {
    "fill_empty" : None
}


def _parse_line(spec, line): # here be lines

    fill_empty = OPTIONS["fill_empty"]

    line_data = []

    for rng in spec: # here be substring values

        if type(rng) == str:
            line_data.append(rng)
            continue

        start = rng[0]
        end   = rng[1]
        val   = line[start:end].strip()

        # handle empty values
        if val == '':
            val = fill_empty

        line_data.append(val)

    return line_data


def _configure(options):

    if options is None or \
       not isinstance(options, dict):
           return

    if "fill_empty" in options and \
       options["fill_empty"] is not None:
            OPTIONS["fill_empty"] = str(options["fill_empty"])


def _parse_lines(ff_spec, ff_lines):

    # output structure
    ff_file_data = []

    for line in ff_lines:

        line_data = _parse_line(ff_spec, line)

        ff_file_data.append(line_data)

    return ff_file_data


def parse_lines(ff_spec, ff_lines, options): # here be lines from a ff file

    '''
    Parse substrings from lines using the provided spec

    :param list ff_spec: list of lists containing start/end indicies of substrings
    :param list ff_liines: list of lines from a flat file
    :param dict options: list of ff parser options

    :rtype: list

    '''

    # handle options
    _configure(options)

    # adjust parameters

    # if 1 line make array
    if not isinstance(ff_lines, list):
        ff_lines = [ff_lines]

    return _parse_lines(ff_spec, ff_lines)


def parse_files(ff_spec, ff_file_path, options): # here be file paths
    '''
    Parse the provided flat files lines into a single 2D list of substrings

    :param list ff_spec: list of lists containing start/end indicies of substrings
    :param list ff_file_path: list of paths to flat files, a single path can be provided
    :param dict options: list of ff parser options

    :rtype: list

    '''

    # handle options
    _configure(options)

    # handle parameters

    # if 1 path make an array
    if not isinstance(ff_file_path, list):
        ff_file_path = [ff_file_path]

    # output structure
    ff_file_data = []

    for path in ff_file_path:

        with open(path) as file:
            lines = file.readlines()

        ff_file_data.extend(_parse_lines(ff_spec, lines))

    return ff_file_data

