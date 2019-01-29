# Google Image Downloader
Source code is here: https://github.com/hardikvasa/google-images-download

	pip install google_images_download --user ## downloads the python script

## If you want to download more than 100 images at a time
	
	sudo apt-get install -y chromium-chromedriver 

## Using the image downloader

	mkdir -p ~/datasets/googleimages/pistol_in_hand && cd ~/datasets/googleimages/pistol_in_hand
	googleimagesdownload -n -nn -k "pistol in hand, pistol firing, pistol shooting" -l 500 -cd /usr/lib/chromium-browser/chromedriver


	-n # no sub-directory : download to current location
	-nn # no numbering
	-cd /usr/lib/chromium-browser/chromedriver # location of chrome driver for downloading more than 100 images
	-k "pistol in hand" # search term


# Download images from bing/azure
This section is mostly a rehash of [this page](https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/)
	
## Set up azure account

To get started, head to the [Bing Image Search API page](https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api)

![Open Project](https://github.com/westpoint-robotics/threat_detection/blob/master/git_ref/get_api_key.jpg)

![Open Project](https://github.com/westpoint-robotics/threat_detection/blob/master/git_ref/api_keys.jpg)

After you have created your account and found your api keys run these commands: (replace [API_Key1] and [API_Key2] with your own keys)

	echo "export AZURE_KEY_1=[API_Key1]" >> ~/.bashrc
	echo "export AZURE_KEY_2=[API_Key2]" >> ~/.bashrc

## Usage
	
	cd ~/threat_detection/azure
	mkdir -p ~/datasets/automatic_rifle &&  python dl_query.py --api $AZURE_KEY_1 --query "automatic rifle" --output ~/datasets/automatic_rifle

# Pruning
Not all images will actually be relevant to the query you intended.  There will be some touch work needed to prune the images you do not want.











