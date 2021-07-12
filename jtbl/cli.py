import sys
import signal
import textwrap
import json
import tabulate
import shutil

__version__ = '1.1.7'


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None
    else:
        return sys.stdin.read()


def helptext():
    print_error(textwrap.dedent('''\
        jtbl:   Converts JSON and JSON Lines to a table

        Usage:  <JSON Data> | jtbl [OPTIONS]

                --cols=n   manually configure the terminal width
                -n         do not try to wrap if too long for the terminal width
                -t         truncate data instead of wrapping if too long for the terminal width
                -v         version info
                -h         help
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def wrap(data, columns, table_format, truncate):
    """
    Wrap or truncate the data to fit the terminal width.

    Returns a tuple of (data, table_format)
        data (dictionary)       a modified dictionary with wrapped or truncated string values.
                                wrapping is achieved by inserting \n characters into the value strings.

        table_format (string)   'simple' (for truncation) or 'grid' (for wrapping)
    """

    # find the length of the keys (headers) and longest values
    data_width = {}
    for entry in data:
        for k, v in entry.items():
            if k in data_width:
                if len(str(v)) > data_width[k]:
                    data_width[k] = len(str(v))
            else:
                data_width[k] = len(str(v))

    # highest_value calculations are only approximate since there can be left and right justification
    num_of_headers = len(data_width.keys())
    combined_total_list = []
    for k, v in data_width.items():
        highest_value = max(len(k) + 4, v + 2)
        combined_total_list.append(highest_value)

    total_width = sum(combined_total_list)

    if total_width > columns:
        # Find the best wrap_width based on the terminal size
        sorted_list = sorted(combined_total_list, reverse=True)
        wrap_width = sorted_list[0]
        scale = 2.5 if truncate else 4.5

        while wrap_width > 4 and total_width >= (columns - (num_of_headers * scale)):
            sorted_list = sorted(sorted_list, reverse=True)
            sorted_list[0] -= 1
            total_width = sum(sorted_list)
            wrap_width = sorted_list[0]

        # truncate or wrap every wrap_width chars for all field values
        for entry in data:
            delete_keys = []
            add_keys = []
            for k, v in entry.items():
                if v is None:
                    v = ''

                if truncate:
                    new_key = str(k)[0:wrap_width]
                    new_value = str(v)[0:wrap_width]
                    if k != new_key or v != new_value:
                        delete_keys.append(k)
                        add_keys.append((new_key, new_value))

                else:
                    table_format = 'grid'
                    new_key = '\n'.join([str(k)[i:i + wrap_width] for i in range(0, len(str(k)), wrap_width)])
                    new_value = '\n'.join([str(v)[i:i + wrap_width] for i in range(0, len(str(v)), wrap_width)])
                    if k != new_key or v != new_value:
                        delete_keys.append(k)
                        add_keys.append((new_key, new_value))

            for i in delete_keys:
                del entry[i]

            for i in add_keys:
                entry[i[0]] = i[1]

    return (data, table_format)


def make_table(input_data=None,
               truncate=False,
               nowrap=False,
               columns=None,
               table_format='simple'):
    """
    Generates the table from the JSON input.

    Returns a tuple of ([SUCCESS | ERROR], result)
        SUCCESS | ERROR (boolean)   SUCCESS (True) if no error, ERROR (False) if error encountered
        result (string)             text string of the table result or error message
    """
    SUCCESS, ERROR = True, False

    if input_data is None:
        return (ERROR, 'jtbl:   Missing piped data\n')

    if columns is None:
        columns = shutil.get_terminal_size().columns

    # only process if there is data
    if input_data and not input_data.isspace():

        try:
            data = json.loads(input_data)
            if type(data) is not list:
                data_list = []
                data_list.append(data)
                data = data_list

        except Exception:
            # if json.loads fails, assume the data is formatted as json lines and parse
            data = input_data.splitlines()
            data_list = []
            for i, jsonline in enumerate(data):
                try:
                    entry = json.loads(jsonline)
                    data_list.append(entry)
                except Exception as e:
                    # can't parse the data. Throw a nice message and quit
                    return (ERROR, textwrap.dedent(f'''\
                        jtbl:  Exception - {e}
                               Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                               {str(jsonline)[0:columns - 8]}
                               '''))

            data = data_list

        try:
            if not isinstance(data[0], dict):
                data = json.dumps(data)
                return (ERROR, textwrap.dedent(f'''\
                    jtbl:  Cannot represent this part of the JSON Object as a table.
                           (Could be an Element, an Array, or Null data instead of an Object):
                           {str(data)[0:columns - 8]}
                           '''))

        except Exception:
            # can't parse the data. Throw a nice message and quit
            return (ERROR, textwrap.dedent(f'''\
                jtbl:  Cannot parse the data (Not JSON or JSON Lines data):
                       {str(data)[0:columns - 8]}
                       '''))

        if not nowrap:
            data, table_format = wrap(data=data, columns=columns, table_format=table_format, truncate=truncate)

        return (SUCCESS, tabulate.tabulate(data, headers='keys', tablefmt=table_format))

    else:
        return (ERROR, '')


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    # break on pipe error. need try/except for windows compatibility
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    stdin = get_stdin()

    options = []
    long_options = {}
    for arg in sys.argv:
        if arg.startswith('-') and not arg.startswith('--'):
            options.extend(arg[1:])

        if arg.startswith('--'):
            try:
                k, v = arg[2:].split('=')
                long_options[k] = int(v)
            except Exception:
                helptext()

    nowrap = 'n' in options
    truncate = 't' in options
    version_info = 'v' in options
    helpme = 'h' in options

    columns = None
    if 'cols' in long_options:
        columns = long_options['cols']

    if version_info:
        print_error(f'jtbl:   version {__version__}\n')

    if helpme:
        helptext()

    succeeeded, result = make_table(input_data=stdin, truncate=truncate, nowrap=nowrap, columns=columns)

    if succeeeded:
        print(result)
    else:
        print_error(result)


if __name__ == '__main__':
    main()
