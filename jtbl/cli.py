import io
import sys
import signal
import textwrap
import csv
import json
import tabulate
import shutil

__version__ = '1.6.0'
SUCCESS, ERROR = True, False

# START add DokuWiki table format
dokuwiki_format = {
    "dokuwiki": tabulate.TableFormat(
        lineabove=tabulate.Line("|", "-", "|", "|"),
        linebelowheader=tabulate.Line("|", "-", "|", "|"),
        linebetweenrows=None,
        linebelow=None,
        headerrow=tabulate.DataRow("^", "^", "^"),
        datarow=tabulate.DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=["lineabove", "linebelowheader"],
    )
}
tabulate._table_formats.update(dokuwiki_format)  # type: ignore
# END add DokuWiki table format

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

                --cols=n           manually configure the terminal width
                -c, --csv          CSV table output
                -d, --dokuwiki     DokuWiki table output
                -f, --fancy        fancy table output
                -h, --help         help
                -H, --html         HTML table output
                -m, --markdown     markdown table output
                -n, --no-wrap      do not try to wrap if too wide for the terminal
                -q, --quiet        quiet - don't print error messages
                -r, --rotate       rotate table output
                -t, --truncate     truncate data if too wide for the terminal
                -v, --version      version info
    '''))


def print_error(message, quiet=False):
    """print error messages to STDERR and quit with error code"""
    if not quiet:
        print(message, file=sys.stderr)
    sys.exit(1)


def wrap(data, columns, table_format, truncate):
    """
    Wrap or truncate the data to fit the terminal width.

    Returns a tuple of (data, table_format)
        data (list)     a modified list of dictionies with wrapped or truncated string values.
                        wrapping is achieved by inserting \n characters into the value strings.

        table_format (string)   'simple' (for truncation) or 'fancy_grid' (for wrapping)
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

    new_table = []
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
            add_keys = {}
            for k, v in entry.items():
                if v is None:
                    v = ''

                if truncate:
                    new_key = str(k)[0:wrap_width]
                    new_value = str(v)[0:wrap_width]
                    add_keys[new_key] = new_value

                else:
                    table_format = 'fancy_grid'
                    new_key = '\n'.join([str(k)[i:i + wrap_width] for i in range(0, len(str(k)), wrap_width)])
                    new_value = '\n'.join([str(v)[i:i + wrap_width] for i in range(0, len(str(v)), wrap_width)])
                    add_keys[new_key] = new_value

            new_table.append(add_keys)

    return (new_table or data, table_format)


def get_json(json_data, columns=None):
    """Accepts JSON or JSON Lines and returns a tuple of
       (success/error, list of dictionaries)
    """
    if not json_data or json_data.isspace():
        return (ERROR, 'jtbl:   Missing piped data\n')

    try:
        data = json.loads(json_data)
        if type(data) is not list:
            data_list = []
            data_list.append(data)
            data = data_list

        return SUCCESS, data

    except Exception:
        # if json.loads fails, assume the data is formatted as json lines and parse
        data = json_data.splitlines()
        data_list = []
        for i, jsonline in enumerate(data):
            try:
                if jsonline.strip():
                    entry = json.loads(jsonline)
                    data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                return (ERROR, textwrap.dedent(f'''\
                    jtbl:  Exception - {e}
                           Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                           {str(jsonline)[0:columns - 8]}
                            '''))
        return SUCCESS, data_list


def check_data(data=None, columns=0):
    """Return (SUCCESS, data) if data can be processed. (ERROR, msg) if not"""
    # only process if there is data
    if data:
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

        return SUCCESS, data

    if data == []:
        return SUCCESS, ''

    return ERROR, data


def get_headers(data):
    """scan the data and return a dictionary of all of the headers in order"""
    headers = []

    if isinstance(data, dict):
        headers.append(data.keys())

    elif isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                headers.extend(row.keys())

    # preserve field order by using dict.fromkeys()
    header_dict = dict.fromkeys(headers)

    return header_dict


def make_rotate_table(
    data=None,
    truncate=False,
    nowrap=False,
    columns=None,
    table_format='simple',
    rotate=False
):
    """generates a rotated table"""
    table = ''
    for idx, row in enumerate(data):
        rotated_data = []
        for k, v in row.items():
            rotated_data.append({'key': k, 'value': v})

        succeeded, result = make_table(
            data=rotated_data,
            truncate=truncate,
            nowrap=nowrap,
            columns=columns,
            table_format=table_format,
            rotate=rotate
        )

        if succeeded:
            if len(data) > 1:
                table += f'item: {idx}\n'
                table += '─' * columns + '\n'
            table += result + '\n\n'

    return (SUCCESS, table[:-1])


def make_csv_table(data=None):
    """generate csv table"""
    buffer = io.StringIO()
    headers = get_headers(data)

    writer = csv.DictWriter(
        buffer,
        headers,
        restval='',
        extrasaction='raise',
        dialect='excel'
    )

    writer.writeheader()

    if isinstance(data, dict):
        data = [data]

    if isinstance(data, list):
        for row in data:
            writer.writerow(row)

    return (SUCCESS, buffer.getvalue())


def make_table(
    data=None,
    truncate=False,
    nowrap=False,
    columns=None,
    table_format='simple',
    rotate=False
):
    """Generate simple or fancy table"""
    if not nowrap:
        data, table_format = wrap(
            data=data,
            columns=columns,
            table_format=table_format,
            truncate=truncate
        )

    headers = 'keys'
    if rotate:
        table_format = 'plain'
        headers = ''

    return (SUCCESS, tabulate.tabulate(data, headers=headers, tablefmt=table_format, floatfmt=''))


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
            if '=' in arg:
                try:
                    k, v = arg[2:].split('=')
                    long_options[k] = int(v)
                except Exception:
                    helptext()
            else:
                long_options[arg[2:]] = None

    csv = 'c' in options or 'csv' in long_options
    dokuwiki = 'd' in options or 'dokuwiki' in long_options
    html = 'H' in options or 'html' in long_options
    markdown = 'm' in options or 'markdown' in long_options
    fancy_grid = 'f' in options or 'fancy' in long_options
    nowrap = 'n' in options or 'no-wrap' in long_options
    quiet = 'q' in options or 'quiet' in long_options
    rotate = 'r' in options or 'rotate' in long_options
    truncate = 't' in options or 'truncate' in long_options
    version_info = 'v' in options or 'version' in long_options
    helpme = 'h' in options or 'help' in long_options

    if markdown:
        tbl_fmt = 'github'
    elif dokuwiki:
        tbl_fmt = 'dokuwiki'
    elif html:
        tbl_fmt = 'html'
    elif fancy_grid:
        tbl_fmt = 'fancy_grid'
    else:
        tbl_fmt = 'simple'

    if not rotate and (markdown or dokuwiki or html or csv):
        nowrap = True

    columns = None
    if 'cols' in long_options:
        columns = long_options['cols']

    if columns is None:
        columns = shutil.get_terminal_size().columns

    if version_info:
        print_error(f'jtbl:   version {__version__}\n')

    if helpme:
        helptext()

    succeeded, json_data = get_json(stdin, columns=columns)
    if not succeeded:
        print_error(json_data, quiet=quiet)

    succeeded, json_data = check_data(json_data, columns=columns)
    if not succeeded:
        print_error(json_data, quiet=quiet)

    # Make and print the tables
    if rotate:
        succeeded, result = make_rotate_table(
            data=json_data,
            truncate=truncate,
            nowrap=nowrap,
            columns=columns,
            rotate=True
        )

        if succeeded:
            print(result)
        else:
            print_error(result, quiet=quiet)

    elif csv:
        succeeded, result = make_csv_table(data=json_data)

        if succeeded:
            print(result)
        else:
            print_error(result, quiet=quiet)

    else:
        succeeded, result = make_table(
            data=json_data,
            truncate=truncate,
            nowrap=nowrap,
            columns=columns,
            table_format=tbl_fmt
        )

        if succeeded:
            print(result)
        else:
            print_error(result, quiet=quiet)


if __name__ == '__main__':
    main()
