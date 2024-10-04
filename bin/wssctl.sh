#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(dirname $(dirname "$(readlink -f "$0")"))"

start_process() {
    pid=$(get_process_pid)
    if [ -n "$pid" ]; then
        echo "Process exist already."
        echo "Process exist already." >> log/wss_server.log
    else
        mkdir -p "$SCRIPT_DIR/log"  # Ensure the log directory exists
        #@chmod g+w "$SCRIPT_DIR/log"
        nohup python "$SCRIPT_DIR/wss_server.py" >> "$SCRIPT_DIR/log/wss_server.log" 2>> "$SCRIPT_DIR/log/wss_server.err" &
        echo "Process started."
        echo "Process started." >> log/wss_server.log
        #chmod g+w "$SCRIPT_DIR/log/wss_server".*
    fi
}

get_process_pid() {
    pgrep -f "wss_server.py"
}

stop_process() {
    pid=$(get_process_pid)
    if [ -n "$pid" ]; then
        echo "wss_server.py process id [$pid]" >> log/wss_server.log
        kill -9 $pid
        echo "Terminated process with PID: $pid"
        echo "Terminated process with PID: $pid" >> log/wss_server.log
    else
        echo "No such process found."
        echo "No such process found." >> log/wss_server.log
    fi
}

restart_process() {
    stop_process
    start_process
    echo "Process restarted."
    echo "Process restarted." >> log/wss_server.log
}

check_status() {
    pid=$(get_process_pid)
    if [ -n "$pid" ]; then
        echo "Process is running with PID: $pid"
        echo "Process is running with PID: $pid">> log/wss_server.log
    else
        echo "Process is not running."
        echo "Process is not running.">> log/wss_server.log
    fi
}

if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|stop|restart|status}"
    echo "Usage: $0 {start|stop|restart|status}">> log/wss_server.log
    exit 1
fi

action=$1

case $action in
    start)
        start_process
        ;;
    stop)
        stop_process
        ;;
    restart)
        restart_process
        ;;
    status)
        check_status
        ;;
    *)
        echo "Invalid action."
        ;;
esac
