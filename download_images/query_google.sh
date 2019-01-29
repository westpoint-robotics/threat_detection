# https://github.com/hardikvasa/google-images-download
pip install google_images_download --user ## downloads the python script

sudo apt-get install iy chromium-chromedriver # for downloading more than 100 images




googleimagesdownload -k "pistol in hand, pistol firing" -o "pistol_in_hand" -l 500


mkdir -p ~/datasets/googleimages/pistol_in_hand && cd ~/datasets/googleimages/pistol_in_hand
googleimagesdownload -n -nn -k "pistol in hand, pistol firing, pistol shooting" -l 500 -cd /usr/lib/chromium-browser/chromedriver




-n # no sub-directory : download to current location
-nn # no numbering
-cd /usr/lib/chromium-browser/chromedriver # location of chrome driver for downloading more than 100 images
-k "pistol in hand" # search term

