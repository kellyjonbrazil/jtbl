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

It can be useful to JSONify command line output with `jc`, filter through `jq`, and present in `jtbl`:
```
$ jc ifconfig | jq -c '.[] | {name, type, ipv4_addr, ipv4_mask}'| jtbl 
name     type            ipv4_addr       ipv4_mask
-------  --------------  --------------  -------------
docker0  Ethernet        172.17.0.1      255.255.0.0
ens33    Ethernet        192.168.71.146  255.255.255.0
lo       Local Loopback  127.0.0.1       255.0.0.0
```

## Installation
```
pip3 install --upgrade jtbl
```
## Usage
Just pipe JSON data to `jtbl`. (e.g. `cat` a JSON file, `jc`, `jq`, `aws` cli, `kubectl`, etc.)
```
$ <JSON Data> | jtbl [OPTIONS]
```
### Options
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
If there are too many elements, or the data in the elements are too large, the table may not fit in the terminal screen. In this case you can use a JSON filter like `jq` to send `jtbl` only the elements you are interested in:

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

When piping any of these to `jtbl` you get the following result:
```
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
+-------+----------+----------+--------------+-------------+--------------+-----------------+------------------+--------------+--------------+--------------+----------+--------------+--------+
|    id | opcode   | status   | flags        |   query_num |   answer_num |   authority_num |   additional_num | question     | answer       |   query_time |   server | when         |   rcvd |
+=======+==========+==========+==============+=============+==============+=================+==================+==============+==============+==============+==========+==============+========+
| 28791 | QUERY    | NOERROR  | ['qr', 'rd', |           1 |            5 |               0 |                1 | {'name': 'ww | [{'name': 'w |           32 |     2600 | Fri Mar 06 1 |    143 |
|       |          |          |  'ra']       |             |              |                 |                  | w.cnn.com.', | ww.cnn.com.' |              |          | 7:15:25 PST  |        |
|       |          |          |              |             |              |                 |                  |  'class': 'I | , 'class': ' |              |          | 2020         |        |
|       |          |          |              |             |              |                 |                  | N', 'type':  | IN', 'type': |              |          |              |        |
|       |          |          |              |             |              |                 |                  | 'A'}         |  'CNAME', 't |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | tl': 251, 'd |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | ata': 'turne |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | r-tls.map.fa |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | stly.net.'}, |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              |  {'name': 't |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | urner-tls.ma |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | p.fastly.net |              |          |              |        |
|       |          |          |              |             |              |                 |                  |              | ...          |              |          |              |        |
+-------+----------+----------+--------------+-------------+--------------+-----------------+------------------+--------------+--------------+--------------+----------+--------------+--------+
```

## Diving Deeper into the JSON with `jq`
To get to the data you are interested in you can use a JSON filter like `jq` do dive deeper.
```
$ jc dig www.cnn.com | jq '.[].answer' 
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
name                        class    type      ttl  data
--------------------------  -------  ------  -----  --------------------------
www.cnn.com.                IN       CNAME      11  turner-tls.map.fastly.net.
turner-tls.map.fastly.net.  IN       A          23  151.101.129.67
turner-tls.map.fastly.net.  IN       A          23  151.101.1.67
turner-tls.map.fastly.net.  IN       A          23  151.101.65.67
turner-tls.map.fastly.net.  IN       A          23  151.101.193.67

```

## Column Width
`jtbl` will attempt to shrink columns to a sane size if it detects the output is wider than the terminal width. You can use the `-t` option to truncate the rows instead of wrapping when the terminal width is too small for all of the data.