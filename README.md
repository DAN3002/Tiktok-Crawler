# Tiktok Crawler
This is a simple Tiktok crawler that can be used to download videos from Tiktok. It uses the Tiktok API to get the video URL and then downloads the video using the requests library. It can download video from multiple hashtags or download by sound.

## Prerequisites
- Python 3.11

## Installation
To install the required libraries, run the following command:
```bash
# Create a virtual environment and install the required libraries
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Install playwright
playwright install
```

Then add the following environment variables to your `.env` file:
```
MS_TOKEN=<your "ms_token" value from your tiktok cookie>
```

## Usage
Before running the script, makesure to update `configs.py` with the tiktok hashtags you want to download videos from and time range.

To run the script, simply run the following command:
```bash
python main.py
```
## Some issues
1. If you get the following error:
```
playwright._impl._errors.Error: Page.evaluate: ReferenceError: opts is not defined
```
=> Makesure to use Python 3.11 and re-run the installation steps.

2. If you get the following error:
```
ImportError: No module named '_ctypes' when using Value from module multiprocessing
```

=> Install the following package:
```bash
sudo apt-get install libffi-dev
pyenv uninstall 3.11.9
pyenv install 3.11
`

