#compdef jtbl

_jtbl() {
    jtbl_options_describe=(
        '--cols:manually configure the terminal width'
        '-c:CSV table output'
        '--csv:CSV table output'
        '-d:DokuWiki table output'
        '--dokuwiki:DokuWiki table output'
        '-f:fancy table output'
        '--fancy:fancy table output'
        '-h:help'
        '--help:help'
        '-H:HTML table output'
        '--html:HTML table output'
        '-m:markdown table output'
        '--markdown:markdown table output'
        '-n:do not try to wrap if too wide for the terminal'
        '--no-wrap:do not try to wrap if too wide for the terminal'
        "-q:quiet - don't print error messages"
        "--quiet:quiet - don't print error messages"
        '-r:rotate table output'
        '--rotate:rotate table output'
        '-t:truncate data if too wide for the terminal'
        '--truncate:truncate data if too wide for the terminal'
        '-v:version info'
        '--version:version info'
    )

    _describe 'commands' jtbl_options_describe
    return 0
}

_jtbl