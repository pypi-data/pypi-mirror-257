#!/bin/bash
# ---------------------------------------------------------
.f() { printf "\e[%sm" "$(tr -s ' ' \; <<<"$*")"; }
.fsudo() { .f 38 2 248 184 137 ; }
.r() { .f 0 ; }
__call() { __fmtcmd "$@" ; "$@" ; }
__scall() { __fmtcmd sudo "$@" ; sudo "$@" ; }
__fmtcmd() {
  local cmd="$1" fcmd=$(.f 94)
  shift
  if [[ $cmd == sudo ]] ; then
    cmd+=" $1" ; fcmd=$(.fsudo)
    shift
  fi
  printf "${fcmd}$(.f 1)>$(.r) ${fcmd}%s$(.r) $(.f 34)%s$(.r)\n" "$cmd" "$*"
}
# ---------------------------------------------------------

__main() {
  local source_path="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
  local dest_path="/usr/share/applications"
  local file=default-browser.desktop
  __scall cp -u "$source_path/$file" "$dest_path/$file"
  __scall sed "$dest_path/$file" -i -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g"
}

__main "$@"
