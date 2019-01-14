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

## Prune
Not all images will actually be relevant to the query you intended.  There will be some touch work needed to prune the images you do not want.


## 