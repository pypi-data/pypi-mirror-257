# TheCatAPI Python SDK

Python wrapper for making secure requests to TheCatAPI

## Getting started
- Create an account on [TheCatAPI.com](https://thecatapi.com/)
- An API Key will be sent to you via mail

### Installation

`pip install thecatapi-sdk`

```py
from thecatapi import TheCatAPI

# create an instance
catapi = TheCatApi("API_KEY HERE")
```

## Sample request
```py
# List of images
catapi.images.get_images(limit=10)

-------------------------

# Get image by image ID 
catapi.images.get_image('2bbSbBC-v')

-------------------------

# list votes
catapi.votes.get_votes()
```
> [Read full documentation here](./docs)


# Contribution & Issues
- Simply fork the repo, make changes and make a pull request
- You can open an issue for support or suggestions


## Author
[Adavize Hassan](https://linked.com/in/adavize-hassan)

## Ackowledgements
- [TheCatAPI.com](https://thecatapi.com/)