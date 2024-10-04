#!/bin/bash

# 현재 날짜를 연/월/일로 분리
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")

# 이미지 저장 경로
IMAGE_DIR="/home/pi/GrowthStation/static/images/$YEAR/$MONTH/$DAY"
OUTPUT_DIR="/home/pi/GrowthStation/static/timelapse"

# 타임랩스 출력 파일 경로
OUTPUT_FILE="$OUTPUT_DIR/timelapse_${YEAR}${MONTH}${DAY}.mp4"

# 디렉토리가 없으면 생성
mkdir -p "$OUTPUT_DIR"

# 타임랩스 생성 (ffmpeg를 사용하여 이미지 파일을 영상으로 합침)
ffmpeg -framerate 30 -pattern_type glob -i "$IMAGE_DIR/*.png" -c:v libx264 -pix_fmt yuv420p "$OUTPUT_FILE"

echo "Timelapse created: $OUTPUT_FILE"