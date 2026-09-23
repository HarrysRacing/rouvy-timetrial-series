#!/bin/bash
# archive_startlist_logs.sh — daily log archive, keep last 7

LOG_FILE="/home/harry/harrysracing/logs/startlist_results_calc.log"
ARCHIVE_DIR="/home/harry/harrysracing/logs/archive"
KEEP=7

mkdir -p "$ARCHIVE_DIR"

# 1. Archive today's log
if [ -f "$LOG_FILE" ]; then
 STAMP=$(date +"%Y%m%d_%H%M%S")
 mv $LOG_FILE $ARCHIVE_DIR/startlist_results_calc_$STAMP.log"
fi

# 2. Remove the oldest archive once we exceed KEEP
cd "$ARCHIVE_DIR" || exit 1
while [ "$(ls -1 startlist_results_calc_*.log 2>/dev/null | wc -l)" -gt "$KEEP" ]; do
 oldest=$(ls -1 startlist_results_calc_*.log | head -n 1)
 rm -f "$oldest"
done