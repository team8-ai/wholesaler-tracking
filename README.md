# Wholesaler Price Tracker

This project contains a set of Python scripts to scrape product and pricing data from wholesaler websites, specifically ParMed and BluPax. The data is saved to CSV files for further analysis.

## Project Structure

The repository is organized as follows:

```
.
├── scripts/
│   └── analyze.py
├── src/
│   ├── scrapers/
│   │   ├── parmed_scraper.py
│   │   └── blupax_scraper.py
│   ├── utils/
│   │   ├── browser.py
│   │   └── core.py
│   └── main.py
├── .env.sample
├── Dockerfile
├── requirements.txt
└── render.yaml
```

-   `src/`: Contains the main application source code.
    -   `main.py`: The entry point for running the scrapers.
    -   `scrapers/`: Contains the scraper logic for each wholesaler.
    -   `utils/`: Contains shared utility functions for browser automation and HTTP requests.
-   `scripts/`: Contains additional scripts, for example for data analysis.
-   `Dockerfile`: For building and running the application in a Docker container.
-   `render.yaml`: Configuration for deploying the application as a cron job on [Render](https://render.com/).
-   `requirements.txt`: A list of the Python packages required to run the script.
-   `.env.sample`: An example file for environment variables.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

-   Python 3.11 or later
-   Access to a proxy service (the code is configured for Oxylabs)
-   An OpenAI API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/wholesaler-tracking.git
    cd wholesaler-tracking
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**
    The scraper uses Playwright for browser automation. You need to install the necessary browser binaries.
    ```bash
    playwright install --with-deps chromium
    ```

### Environment Variables

The script requires several environment variables to be set. Create a `.env` file in the root of the project by copying the `.env.sample` file:

```bash
cp .env.sample .env
```

Then, edit the `.env` file with your credentials:

```
# .env

# Credentials for ParMed
PARMED_USERNAME="your-parmed-username"
PARMED_PASSWORD="your-parmed-password"

# Session ID for BluPax
BLUPAX_SESSION_ID="your-blupax-session-id"

# OpenAI API Key
OPENAI_API_KEY="your-openai-api-key"

# Proxy credentials (e.g., Oxylabs)
OX_USERNAME="your-proxy-username"
OX_PASSWORD="your-proxy-password"
OX_PROXY_SERVER_ADDRESS="your-proxy-address"
```

## Usage

### Running the Scraper

To run the scrapers, execute the `main.py` script from the project root:

```bash
python -m src.main
```

The script will launch the scrapers for ParMed and BluPax, and upon completion, you will find the output CSV files in a `data/raw/` directory. This directory will be created if it doesn't exist and is not tracked by Git.

### Running with Docker

You can also run the application using Docker.

1.  **Build the Docker image:**
    ```bash
    docker build -t wholesaler-scraper .
    ```

2.  **Run the Docker container:**
    Make sure to pass the environment variables from your `.env` file to the container.
    ```bash
    docker run --rm --env-file .env wholesaler-scraper
    ```

## Deployment

This project includes a `render.yaml` file for easy deployment to [Render](https://render.com/) as a cron job. The service is configured to run daily, executing the scraper and storing the data.

To deploy, create a new "Cron Job" service on Render and point it to your repository. Render will automatically detect and use the `render.yaml` file. You will need to configure the required environment variables in the Render dashboard.

## Data Analysis

The `scripts/analyze.py` script provides an example of how to process the raw data. It reads the daily CSV files from a local `data/raw/` directory, calculates price changes over time, and saves the results into `data/processed/parmed_deltas.csv` and `data/processed/blupax_delta.csv`.

To use it, you may need to adjust the hardcoded dates in the script and run it as a Python script.
