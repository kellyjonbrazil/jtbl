_jtbl()
{
    OPTIONS=(--cols -c --csv -d --dokuwiki -f --fancy -h --help -H --html -m --markdown -n --no-wrap -q --quiet -r --rotate -t --truncate -v --version)
    MOD_OPTIONS=(--cols -n --no-wrap -q --quiet -t --truncate)

    COMPREPLY=()
    _get_comp_words_by_ref cur prev words cword

    if [ "${#words[@]}" != "2" ]; then
        COMPREPLY=($(compgen -W "${MOD_OPTIONS[*]}" -- "${cur}"))
        return 0
    else
        COMPREPLY=($(compgen -W "${OPTIONS[*]}" -- "${cur}"))
        return 0
    fi
} &&
complete -F _jtbl jtbl