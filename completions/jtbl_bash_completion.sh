_jtbl()
{
    OPTIONS=(--cols -c --csv -d --dokuwiki -f --fancy -h --help -H --html -m --markdown -n --no-wrap -q --quiet -r --rotate -t --truncate -v --version)
    MOD_OPTIONS=(--cols -n --no-wrap -q --quiet -t --truncate)

    if [ "${#COMP_WORDS[@]}" != "2" ]; then
        COMPREPLY=($(compgen -W "${MOD_OPTIONS[*]}" -- "${COMP_WORDS[${#COMP_WORDS[@]}-1]}"))
        return 0
    else
        COMPREPLY=($(compgen -W "${OPTIONS[*]}" -- "${COMP_WORDS[${#COMP_WORDS[@]}-1]}"))
        return 0
    fi
} &&
complete -F _jtbl jtbl