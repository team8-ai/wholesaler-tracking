# Scraper Script

This script is designed to fetch data from Parmed and Blupax websites and save it into CSV files.

## Instructions for macOS Users

These instructions will guide you through setting up and running the script on your Mac.

### Step 1: Install Python

If you don't already have Python installed on your Mac, follow these steps:

1.  Open the **Terminal** application. You can find it by searching in Spotlight (press `Command + Space` and type "Terminal").
2.  Check if Python 3 is already installed by typing:
    ```bash
    python3 --version
    ```
    If you see a version number (e.g., `Python 3.11`), you can skip the installation step.
3.  If Python 3 is not installed, you can [download](https://www.python.org/ftp/python/3.11.9/python-3.11.9-macos11.pkg) version 3.11 from the official Python website.
4.  Download the macOS 64-bit installer and run it. Follow the on-screen instructions.

### Step 2: Download the Script Files

Make sure you have downloaded all the script files (`main.py`, `parmed.py`, `blupax.py`, `utils.py`, and `requirements.txt`) and placed them in a single folder on your computer.

### Step 3: Install Required Libraries

The script needs a few extra libraries to run. You can install them using a tool called `pip` which comes with Python.

1.  Open **Terminal**.
2.  Navigate to the folder where you saved the script files using the `cd` command. For example, if you saved them in a folder called `scraper` on your Desktop, you would type:
    ```bash
    cd ~/Desktop/scraper
    ```
    (Replace `~/Desktop/scraper` with the actual path to your folder).
3.  Install the required libraries by typing:
    ```bash
    pip3 install -r requirements.txt
    ```

### Step 4: Set up Environment Variables

The `parmed.py` script requires an `ACCESS_TOKEN`. You need to create a file named `.env` in the same folder as your scripts and add your token there.

1.  Open a simple text editor (like TextEdit or VS Code if you have it).
2.  Create a new file.
3.  Type the following line, replacing `YOUR_ACCESS_TOKEN_HERE` with your actual token:
    ```
    PARMED_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
    ```
4.  Save the file as `.env` in the same folder where you saved the script files.

### Step 5: Run the Script

Now you are ready to run the script.

1.  Open **Terminal**.
2.  Navigate to the script folder again using the `cd` command (if you closed the Terminal or changed directory).
3.  Run the main script by typing:
    ```bash
    python3 main.py
    ```

The script will run and print messages in the Terminal indicating its progress. It will create two CSV files in the same folder: `parmed-YYYY-MM-DD.csv` and `blupax-YYYY-MM-DD.csv` (where `YYYY-MM-DD` is the current date) containing the scraped data.

If you encounter any errors, double-check the previous steps, especially the installation of libraries and the `.env` file content.
