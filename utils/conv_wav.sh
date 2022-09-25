#FFMPEG_BIN=../../ffmpeg/bin/ffmpeg
export FFMPEG_BIN=ffmpeg
export FFMPEG=${FFMPEG_BIN} -hide_banner -loglevel error

for f in *.wav; do
    ${FFMPEG} -i $f -ac 1 -ar 16000 -acodec pcm_s16le -af "pan=mono|FC=FR" -f wav ${f%.wav}_mono16k.wav
done

for f in *.MP4; do
    ${FFMPEG} -i $f -vn -ac 1 -ar 16000 -acodec pcm_s16le -af "pan=mono|FC=FR" -f wav ${f%.MP4}_mp4_mono16k.wav
done
