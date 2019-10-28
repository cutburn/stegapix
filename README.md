# Stegapix
A project for posting steganographic puns to Twitter, in Python.

## Detail
This is a small project that is built to showcase an implementation I did a while back of LSB image steganography, using Python and PIL. The word "steganography" describes techniques for obscuring a message by concealing it within an innocuous medium, and LSB steganography in particular refers to some process of storing hidden data in the Least Significant Bits of a digital image. Since the least significant bits contribute the least to the color of a pixel, one can replace or mingle them with other information in a way that is not apparent to the eye.

I wanted to show this off with a little enigmatic whimsy, so I decided to write up something to automatically post images to a Twitter account via a cron job, and made a Twitter account [@PicturesOfSnow](https://twitter.com/PicturesOfSnow) that hid images of Snow the rapper (made semi-famous by his 1993 single "Informer") inside images of "snow" (as defined by whatever Google Image spits out for that search term). Of course because I don't curate what the Google Custom Search Engine returns (and because there's another rapper who goes by the handle "Snow" now) the results aren't always perfect, but I had fun making it, and maybe somebody out there has been waiting for the technology to come along that allows them to make a @PicturesOfKittens that covertly embeds images of puppies inside, with minimal configuration effort.

For more on steganography and a brief description of LSB steganography, which I took my idea for implementation from, there's a nice Wikipedia article about it [here](https://en.wikipedia.org/wiki/Steganography).

## Requirements
* [conda](http://conda.pydata.org/docs/download.html)
* Python 2.7+/3.5+: Only required for Miniconda installs on Linux, OSX, and possibly Windows - see installation details in above link
* A Google Custom Search API key and cx ID (See https://cse.google.com/cse/all) and Custom Search Engine with image search enabled
* A Twitter API key, API secret, access token key and access token secret
* An Imgur client ID and client secret

## Setup
1. Install the necessary software for your system from the "Requirements" section.
2. Download/clone this repository.
3. Set up the conda environment with the command:  
  `conda create --name <env> --file <this file>`
4. Install the requisite pip packages with:  
  `pip install -r requirements.txt`
5. In the root directory of your repo, create a file called `settings.ini`. It should be filled out as below, substituting your own API authentication information where indicated:  
  ```ini
  [GENERAL]
  message_search_term = # a search term, e.g. "cute puppies" (without quotes)
  veil_search_term = # another search term, e.g. "adorable kittens" (again, without quotes)
  
  [GOOGLE]
  API_Key = YOUR_API_KEY_HERE
  cx_ID = YOUR_CX_ID_HERE
  skip_traversed_result_indices = 1 # Optional flag; if you wish to start from search index 1 with every invocation you can omit this line
  
  [TWITTER]
  API_Key = YOUR_API_KEY_HERE
  API_Secret = YOUR_API_SECRET_HERE
  Access_Token_Key = YOUR_ACCESS_TOKEN_HERE
  Access_Token_Secret = YOUR_ACCESS_TOKEN_SECRET_HERE
  
  [IMGUR]
  Client_ID = YOUR_CLIENT_ID_HERE
  Client_Secret = YOUR_CLIENT_SECRET_HERE
  ```
6. That's it!

## Usage
1. Activate your conda environment with  
  `source activate <env>` (or `activate <env>` on Windows)
2. Post an image to your configured Twitter account by invoking  
  `./main.py`
