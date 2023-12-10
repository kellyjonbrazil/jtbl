_jtbl()
{
    OPTIONS=(--cols -c --csv -d --dokuwiki -f --fancy -h --help -H --html -m --markdown -n --no-wrap -q --quiet -r --rotate -t --truncate -v --version)
    MOD_OPTIONS=(--cols -n --no-wrap -q --quiet -t --truncate)
    LAST_WORD=$(echo "${COMP_WORDS[${#COMP_WORDS[@]}-1]}")

    if [ "${#COMP_WORDS[@]}" != "2" ]; then
        COMPREPLY=($(compgen -W "${MOD_OPTIONS[*]}" -- "$LAST_WORD"))
        return 0
    else
        COMPREPLY=($(compgen -W "${OPTIONS[*]}" -- "$LAST_WORD"))
        return 0
    fi
} &&
complete -F _jtbl jtbl