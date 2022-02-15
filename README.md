![Tests](https://github.com/kellyjonbrazil/jtbl/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jtbl.svg)

# jtbl
A simple cli tool to print JSON data as a table in the terminal.

`jtbl` accepts piped JSON data from `stdin` and outputs a text table representation to `stdout`. e.g:
```
$ cat cities.json | jtbl
  LatD    LatM    LatS  NS      LonD    LonM    LonS  EW    City               State
------  ------  ------  ----  ------  ------  ------  ----  -----------------  -------
    41       5      59  N         80      39       0  W     Youngstown         OH
    42      52      48  N         97      23      23  W     Yankton            SD
    46      35      59  N        120      30      36  W     Yakima             WA
    42      16      12  N         71      48       0  W     Worcester          MA
    43      37      48  N         89      46      11  W     Wisconsin Dells    WI
    36       5      59  N         80      15       0  W     Winston-Salem      NC
    49      52      48  N         97       9       0  W     Winnipeg           MB
```

`jtbl` expects a JSON array of JSON objects or [JSON Lines](http://jsonlines.org/).

It can be useful to JSONify command line output with `jc`, filter through a tool like `jq`, and present in `jtbl`:
```
$ jc ifconfig | jq -c '.[] | {name, type, ipv4_addr, ipv4_mask}'| jtbl
name     type            ipv4_addr       ipv4_mask
-------  --------------  --------------  -------------
docker0  Ethernet        172.17.0.1      255.255.0.0
ens33    Ethernet        192.168.71.146  255.255.255.0
lo       Local Loopback  127.0.0.1       255.0.0.0
```

## Installation
You can install `jtbl` via `pip`, via OS Package Repositories, MSI installer for Windows, or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
For the most up-to-date version and the most cross-platform option, use `pip` or `pip3` to download and install `jtbl` directly from [PyPi](https://pypi.org/project/jtbl/):

![Pypi](https://img.shields.io/pypi/v/jtbl.svg)


```bash
pip3 install jtbl
```

### OS Packages

[![Packaging status](https://repology.org/badge/vertical-allrepos/jtbl.svg)](https://repology.org/project/jtbl/versions)

See [Releases](https://github.com/kellyjonbrazil/jtbl/releases) on Github for MSI packages and binaries.

## Usage
Just pipe JSON data to `jtbl`. (e.g. `cat` a JSON file, `jc`, `jq`, `aws` cli, `kubectl`, etc.)
```
$ <JSON Data> | jtbl [OPTIONS]
```
### Options
- `--cols=n` manually configure the terminal width
- `-m` markdown table output (overrides `--cols` and `-t`)
- `-n` no data wrapping if too long for the terminal width (overrides `--cols` and `-t`)
- `-r` rotate the data (each row turns into a table of key/value pairs)
- `-t` truncate data instead of wrapping if too long for the terminal width
- `-v` prints version information
- `-h` prints help information

## Compatible JSON Formats
`jtbl` works best with a shallow array of JSON objects. Each object should have a few elements that will be turned into table columns. Fortunately, this is how many APIs present their data.

**JSON Array Example**
```
[
  {
    "unit": "proc-sys-fs-binfmt_misc.automount",
    "load": "loaded",
    "active": "active",
    "sub": "waiting",
    "description": "Arbitrary Executable File Formats File System Automount Point"
  },
  {
    "unit": "sys-devices-pci0000:00-0000:00:07.1-ata2-host2-target2:0:0-2:0:0:0-block-sr0.device",
    "load": "loaded",
    "active": "active",
    "sub": "plugged",
    "description": "VMware_Virtual_IDE_CDROM_Drive"
  },
  ...
]
```

`jtbl` can also work with [JSON Lines](http://jsonlines.org/) format with similar features.

**JSON Lines Example**
```
{"name": "docker0", type": "Ethernet", "ipv4_addr": "172.17.0.1", "ipv4_mask": "255.255.0.0"}
{"name": "ens33", "type": "Ethernet", "ipv4_addr": "192.168.71.146", "ipv4_mask": "255.255.255.0"}
{"name": "lo", "type": "Local Loopback", "ipv4_addr": "127.0.0.1", "ipv4_mask": "255.0.0.0"}
...
```

## Filtering the JSON Input
If there are too many elements, or the data in the elements are too large, the table may not fit in the terminal screen. In this case you can use a JSON filter like `jq` or `jello` to send `jtbl` only the elements you are interested in:

### `jq` Array Method
The following example uses `jq` to filter and format the filtered elements into a proper JSON array.
```
$ cat /etc/passwd | jc --passwd | jq '[.[] | {username, shell}]'
[
  {
    "username": "root",
    "shell": "/bin/bash"
  },
  {
    "username": "bin",
    "shell": "/sbin/nologin"
  },
  {
    "username": "daemon",
    "shell": "/sbin/nologin"
  },
  ...
]
```
*(Notice the square brackets around the filter)*

### `jq` Slurp Method
The following example uses `jq` to filter and 'slurp' the filtered elements into a proper JSON array.
```
$ cat /etc/passwd | jc --passwd | jq '.[] | {username, shell}' | jq -s
[
  {
    "username": "root",
    "shell": "/bin/bash"
  },
  {
    "username": "bin",
    "shell": "/sbin/nologin"
  },
  {
    "username": "daemon",
    "shell": "/sbin/nologin"
  },
  ...
]
```
*(Notice the `jq -s` at the end)*

### `jq` JSON Lines Method
The following example will send the data in JSON Lines format, which `jtbl` can understand:
```
$ cat /etc/passwd | jc --passwd | jq -c '.[] | {username, shell}'
{"username":"root","shell":"/bin/bash"}
{"username":"bin","shell":"/sbin/nologin"}
{"username":"daemon","shell":"/sbin/nologin"}
...
```
*(Notice the `-c` option being used)*

### `jello` List Comprehension Method
If you prefer python list and dictionary syntax to filter JSON data, you can use `jello`:
```
$ cat /etc/passwd | jc --passwd | jello '[{"username": x.username, "shell": x.shell} for x in _]'
[
  {
    "username": "root",
    "shell": "/bin/bash"
  },
  {
    "username": "bin",
    "shell": "/sbin/nologin"
  },
  {
    "username": "daemon",
    "shell": "/sbin/nologin"
  },
  ...
]
```

When piping any of these to `jtbl` you get the following result:
```
$ cat /etc/passwd | jc --passwd | jello '[{"username": x.username, "shell": x.shell} for x in _]' | jtbl
username         shell
---------------  --------------
root             /bin/bash
bin              /sbin/nologin
daemon           /sbin/nologin
...
```

## Working with Deeper JSON Structures
`jtbl` will happily dump deeply nested JSON structures into a table, but usually this is not what you are looking for.
```
$ jc dig www.cnn.com | jtbl
╒══════════╤══════════╤═══════╤════════════╤═════════════╤══════════════╤══════════════╤══════════════╤══════════════╤════════════╤════════════╤══════════════╤════════════╤════════════╤════════╤══════════════╤══════════════╕
│ opcode   │ status   │    id │ flags      │   query_num │   answer_num │   authority_ │   additional │ opt_pseudo   │ question   │ answer     │   query_time │ server     │ when       │   rcvd │   when_epoch │ when_epoch   │
│          │          │       │            │             │              │          num │         _num │ section      │            │            │              │            │            │        │              │ _utc         │
╞══════════╪══════════╪═══════╪════════════╪═════════════╪══════════════╪══════════════╪══════════════╪══════════════╪════════════╪════════════╪══════════════╪════════════╪════════════╪════════╪══════════════╪══════════════╡
│ QUERY    │ NOERROR  │ 36494 │ ['qr', 'rd │           1 │            4 │            0 │            1 │ {'edns': {   │ {'name': ' │ [{'name':  │           47 │ 2600:1700: │ Wed Dec 22 │    100 │   1640200072 │              │
│          │          │       │ ', 'ra']   │             │              │              │              │ 'version':   │ cnn.com.', │ 'cnn.com.' │              │ bab0:d40:: │  11:07:52  │        │              │              │
│          │          │       │            │             │              │              │              │  0, 'flags   │  'class':  │ , 'class': │              │ 1#53(2600: │ PST 2021   │        │              │              │
│          │          │       │            │             │              │              │              │ ': [], 'ud   │ 'IN', 'typ │  'IN', 'ty │              │ 1700:bab0: │            │        │              │              │
│          │          │       │            │             │              │              │              │ p': 4096}}   │ e': 'A'}   │ pe': 'A',  │              │ d40::1)    │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ 'ttl': 60, │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │  'data': ' │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ 151.101.12 │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ 9.67'}, {' │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ name': 'cn │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ n.com.', ' │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ class': 'I │              │            │            │        │              │              │
│          │          │       │            │             │              │              │              │              │            │ ...        │              │            │            │        │              │              │
╘══════════╧══════════╧═══════╧════════════╧═════════════╧══════════════╧══════════════╧══════════════╧══════════════╧════════════╧════════════╧══════════════╧════════════╧════════════╧════════╧══════════════╧══════════════╛
```

## Diving Deeper into the JSON with `jq` or `jello`:
To get to the data you are interested in you can use a JSON filter like `jq` or `jello` to dive deeper.

Using `jq`:
```
$ jc dig www.cnn.com | jq '.[0].answer'
```
or with `jello`:
```
$ jc dig www.cnn.com | jello '_[0].answer'
```
Both will produce the following output:
```
[
  {
    "name": "www.cnn.com.",
    "class": "IN",
    "type": "CNAME",
    "ttl": 90,
    "data": "turner-tls.map.fastly.net."
  },
  {
    "name": "turner-tls.map.fastly.net.",
    "class": "IN",
    "type": "A",
    "ttl": 20,
    "data": "151.101.1.67"
  }
  ...
]
```

This will produce the following table in `jtbl`
```
$ jc dig www.cnn.com | jello '_[0].answer' | jtbl
name                        class    type      ttl  data
--------------------------  -------  ------  -----  --------------------------
www.cnn.com.                IN       CNAME      11  turner-tls.map.fastly.net.
turner-tls.map.fastly.net.  IN       A          23  151.101.129.67
turner-tls.map.fastly.net.  IN       A          23  151.101.1.67
turner-tls.map.fastly.net.  IN       A          23  151.101.65.67
turner-tls.map.fastly.net.  IN       A          23  151.101.193.67

```

## Column Width
`jtbl` will attempt to shrink columns to a sane size if it detects the output is wider than the terminal width. The `--cols` option will override the automatic terminal width detection.

You can use the `-t` option to truncate the rows instead of wrapping when the terminal width is too small for all of the data.

The `-n` option disables wrapping and overrides the `--cols` and `-t` options.

This can be useful to present a nicely non-wrapped table of infinite width in combination with `less -S`:
```
$ jc ps aux | jtbl -n | less -S
user                  pid        vsz     rss  tt    stat    started    time       command
------------------  -----  ---------  ------  ----  ------  ---------  ---------  ---------------------------------------------------
joeuser             34029    4277364   24800  s000  S+      9:28AM     0:00.27    /usr/local/Cellar/python/3.7.6_1/Frameworks/Python....
joeuser             34030    4283136   17104  s000  S+      9:28AM     0:00.20    /usr/local/Cellar/python/3.7.6_1/Frameworks/Python....
joeuser               481    5728568  189328        S       17Apr20    21:46.52   /Applications/Utilities/Terminal.app/Contents/MacOS...
joeuser             45827    6089084  693768        S       Wed01PM    84:54.87   /Applications/Microsoft Teams.app/Contents/Framewor...
joeuser              1493    9338824  911600        S       17Apr20    143:27.08  /Applications/Microsoft Outlook.app/Contents/MacOS/...
joeuser             45822    5851524  163840        S       Wed01PM    38:48.83   /Applications/Microsoft Teams.app/Contents/MacOS/Te...
```