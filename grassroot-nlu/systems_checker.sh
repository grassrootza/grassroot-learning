#! /bin/bash

case "$(pidof flask | wc -w)" in

0)  echo "Restarting sello:"
    bash activate_me.sh
    ;;
1)  echo "sello already running"
    ;;
esac