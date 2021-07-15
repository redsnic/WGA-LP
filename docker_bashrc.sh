# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi
eval "$(/root/miniconda/bin/conda shell.bash hook)"

export PERL5LIB=$CONDA_PREFIX/lib/perl5/site_perl/5.22.0/

# use a fancier command line
PS1="\[\e[0;32m\]wgalp\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]>"

echo -e ''
echo -e '░██╗░░░░░░░██╗░██████╗░░█████╗░░░░░░░██╗░░░░░██████╗░\n░██║░░██╗░░██║██╔════╝░██╔══██╗░░░░░░██║░░░░░██╔══██╗\n░╚██╗████╗██╔╝██║░░██╗░███████║█████╗██║░░░░░██████╔╝\n░░████╔═████║░██║░░╚██╗██╔══██║╚════╝██║░░░░░██╔═══╝░\n░░╚██╔╝░╚██╔╝░╚██████╔╝██║░░██║░░░░░░███████╗██║░░░░░\n░░░╚═╝░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝░░░░░░╚══════╝╚═╝░░░░░'
echo -e '\nWelcome to the shell of wgalp, a pipeline for whole genome assembly:'
echo -e "-\tThis shell runs in Ubuntu and has full functionalities, if you need a specific program you can install it as usual, for example with apt (remember that you are root)"
echo -e "-\tThe 'shared' folder contains your data, any file produced in this folder is also available to the host system and vice versa."
echo -e "\tAny other activity has its effects limited to this container only. The storage is persistent, so nothing is lost when this container is stopped."
echo -e "-\tThe core wgalp sources are in the folder '~/git/WGA-LP'"
echo -e "-\tTo use wgalp tools simply enter 'wgalp' to the promt, this will show an help message with an explanation of wgalp functionalities"
echo -e "For any question and/or to report a problem, feel free to open an issue on github or to write me an e-mail"
echo -e "\t\tThe Author and mantainer: Nicolò Rossi <email:olocin.issor@gmail.com> <github:https://github.com/redsnic/WGA-LP>" 
cd /root



