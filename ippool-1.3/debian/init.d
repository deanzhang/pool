#! /bin/sh -e

### BEGIN INIT INFO
# Provides:          ippoold
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Required-Start:    2 3 4 5
# Required-Stop:     0 1 6
# Short-Description: Start ippool daemon
# Description:       Start ippool daemon
### END INIT INFO

DAEMON=/usr/sbin/ippoold
NAME=ippoold
MODULE=pppol2tp

# Check for daemon presence
test -x $DAEMON || exit 0

# Get lsb functions
. /lib/lsb/init-functions
. /etc/default/rcS

case "$1" in
  start)
    log_begin_msg "Starting ippoold..."
    start-stop-daemon --start --quiet --exec $DAEMON
    log_end_msg $?
    ;;
  stop)
    log_begin_msg "Stopping ippoold..."
    start-stop-daemon --stop --quiet --oknodo --retry 2 --exec $DAEMON
    if [ -f /var/run/ippoold.pid ] ; then
        rm -rf /var/run/ippoold.pid >/dev/null
    fi
    log_end_msg $?
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  reload|force-reload) 
    log_begin_msg "Reloading ippoold..."
    start-stop-daemon --stop --signal 1 --exec $DAEMON
    log_end_msg $?
    ;;
  *)
    log_success_msg "Usage: /etc/init.d/ippoold {start|stop|restart|reload|force-reload}"
    exit 1
esac

exit 0

