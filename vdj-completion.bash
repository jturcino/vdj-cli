

_vdj () {
    COMPREPLY=()
    local prev cur
    cur=${COMP_WORDS[COMP_CWORD]}

    local commands="apps files jobs login metadata monitors notifications profiles projects postits systems"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "$commands" -- $cur) )
    elif [ $COMP_CWORD -eq 2 ]; then
        prev=${COMP_WORDS[COMP_CWORD-1]}

        case "$prev" in
            app|apps) COMPREPLY=( $(compgen -W "addupdate clone disable enable erase history ls pems publish rm search" -- $cur) ) ;;
            file|files) COMPREPLY=( $(compgen -W "cp download history import index ls mv pems publish rename rm upload" -- $cur) ) ;;
            job|jobs) COMPREPLY=( $(compgen -W "history ls output pems resubmit rm run search status submit template" -- $cur) ) ;;
            metadata) COMPREPLY=( $(compgen -W "addupdate ls pems schema rm" -- $cur) ) ;;
            monitor|monitors) COMPREPLY=( $(compgen -W "addupdate checks ls rm" -- $cur) ) ;;
            notification|notifications) COMPREPLY=( $(compgen -W "addupdate ls rm search" -- $cur) ) ;;
            project|projects) COMPREPLY=( $(compgen -W "create ls rm" -- $cur) ) ;;
            postit|postits) COMPREPLY=( $(compgen -W "create ls rm" -- $cur) ) ;;
            system|systems|s) COMPREPLY=( $(compgen -W "addupdate clone disable enable history ls publish queues rm roles search setdefault unsetdefault" -- $cur) ) ;; 
        esac

    elif [ $COMP_CWORD -gt 2 ]; then
        prev=${COMP_WORDS[COMP_CWORD-1]}

        case "$prev" in
            -p) local IFS=$'\n'; COMPREPLY=($(compgen -W "$(vdj-projects-list.py | awk '{$NF=""; print "\x27" $0 }' | sed "s/ $/\x27/" | sed "s/ /\\ /g" )" -- $cur)) ;;
        esac
    fi

    return 0
}

complete  -F _vdj vdj
