# Stegapix
A project for posting steganographic puns to Twitter, in Python.

## Requirements
* [conda](http://conda.pydata.org/docs/download.html)
* Python 2.7+/3.5+: Only required for Miniconda installs on Linux, OSX, and possibly Windows - see installation details in above link

## Setup
1. Install the necessary software for your system from the "Requirements" section.
2. Download/clone this repository.
3. Set up the conda environment with the command:  
`conda create --name <env> --file <this file>`
4. Install the requisite pip packages with:  
`pip install -r requirements.txt`
5. In the root directory of your repo, create a file called `settings.ini`. It should be filled out as below, substituting your own API authentication information where indicated:  
  ```
  [GOOGLE]
  API_Key = YOUR_API_KEY_HERE
  cx_ID = YOUR_CX_ID_HERE
  
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
