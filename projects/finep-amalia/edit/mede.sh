#!/usr/bin/env bash
# mede.sh <arquivo> <filtro>  -> YAVG/UAVG/VAVG medios de 300 frames a partir de 20s
ffmpeg -v error -ss 20 -i "$1" -vf "$2,signalstats,metadata=print:file=-" -frames:v 300 -f null - 2>/dev/null \
 | awk -F= '/YAVG|UAVG|VAVG/{s[$1]+=$2;n[$1]++} END{printf "Y=%.1f U=%.1f V=%.1f\n", s["lavfi.signalstats.YAVG"]/n["lavfi.signalstats.YAVG"], s["lavfi.signalstats.UAVG"]/n["lavfi.signalstats.UAVG"], s["lavfi.signalstats.VAVG"]/n["lavfi.signalstats.VAVG"]}'
