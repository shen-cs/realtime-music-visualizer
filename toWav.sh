if (!($# == 2))
then
  echo "Usage: $0 outFile.wav inFile.mp3"
  exit -1
fi
mpg123 $1 $2
echo "finished"
