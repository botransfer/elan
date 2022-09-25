#!/usr/bin/env bash

# 最初にxx秒のブランクを挿入した動画を作成する
# usage: $0 <original MP4> <seconds>
# 例: test.mp4 -> test_xxsec.mp4 

FFMPEG=../../ffmpeg/bin/ffmpeg

${FFMPEG} -i $1 -vf tpad=start_duration=$2:color=black -af adelay=$2s:all=1 -c:v h264_nvenc ${1%.*}_$2sec.mp4

# NVIDIA のGPU が無い場合、上をコメントアウトして、以下を使う（CPUエンコード）

# ../ffmpeg/bin/ffmpeg -i $1 -vf tpad=start_duration=$2:color=black -af adelay=$2s:all=1 ${1%.*}_$2sec.mp4
