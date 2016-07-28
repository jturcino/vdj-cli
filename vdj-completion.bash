

_vdj () {
    COMPREPLY=()
    local prev cur
    cur=${COMP_WORDS[COMP_CWORD]}

    local commands="apps files jobs login metadata postits projects systems"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "$commands" -- $cur) )
    elif [ $COMP_CWORD -eq 2 ]; then
        prev=${COMP_WORDS[COMP_CWORD-1]}

#        case "$prev" in
#            project|projects|p) COMPREPLY=( $(compgen -W "create ls delete" -- $cur) ) ;;
#            list|ls) COMPREPLY=( $(compgen -W "-p" -- $cur) ) ;;
#            *) ;;


        case "$prev" in
            apps) COMPREPLY=( $(compgen -W "addupdate clone rm ls pems publish search" -- $cur) ) ;;
            files) COMPREPLY=( $(compgen -W "cp download history import mv pems rename rm upload" -- $cur) ) ;;
            jobs) COMPREPLY=( $(compgen -W "history ls pems rm status submit" -- $cur) ) ;;
            project|projects|p) COMPREPLY=( $(compgen -W "create ls rm" -- $cur) ) ;;

            
        esac
    fi

    return 0
}

complete  -F _vdj vdj
