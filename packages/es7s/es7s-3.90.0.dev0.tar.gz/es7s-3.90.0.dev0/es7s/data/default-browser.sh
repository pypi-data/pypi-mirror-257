#!/bin/bash
# --------------------
# INSTALL
#   ./applications/install.sh
#   sudo xdg-settings set default-web-browser default-browser.desktop
#
# USAGE
#   Update Exec for a specified application as follows.
#   BEFORE:  Exec=<APPNAME> %u
#    AFTER:  Exec=env DEFAULT_BROWSER=firefox <APPNAME> %u
#

if [ "$DEFAULT_BROWSER" == "" ]
then
  DEFAULT_BROWSER=google-chrome
fi

$DEFAULT_BROWSER "$@"
