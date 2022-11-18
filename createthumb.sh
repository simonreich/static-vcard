for i in `ls -1`; do echo $i; convert $i -quality 80 -resize 1920 $i; convert $i -resize 600 ../thumbnails/$i;done
