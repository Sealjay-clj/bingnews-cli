# Bing News Search API - CLI

This CLI is written in Python to provide an interactive prompt to search for interesting articles that could be used to post to Twitter, or for resarch purposes.

The aim is to demonstrate the use of the Bing News Search API - for more information, [please read the related blog post](https://sealjay.com/bing-news-search-cli/).

## Software Installation

1. Create a Python virtualenv, activate it, and install dependencies:

   - on windows, you may need to use `python` command where there are references to the `python3` command,
   - on macos/linux, you may need to run sudo apt-get install python3-venv first.)

   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   $ pip3 install -r requirements-dev.txt
   ```

   - if you are using a distribution of conda, you may want to create a new conda environment, rather than use venv `conda create --name bingnews python=3.8 -y`, and then `conda activate bingnews`, and  `pip3 install -r requirements-dev.txt`.

2. Complete other settings from the .env template.

## Dependencies
You'll need to have an Azure Subscription with a [Bing Search API](https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/bing-api-comparison) deployment, with a [SKU](https://www.microsoft.com/en-us/bing/apis/pricing) that allows usage of the Bing News Search Features.