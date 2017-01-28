if (!($# == 2))
then
  echo "Usage: $0 inFile outFile"
  exit -1
fi
ffmpeg -i $1 -acodec pcm_u8 -ar 44100 -ac 2 $2
echo "finished"
