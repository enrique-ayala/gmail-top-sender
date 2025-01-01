# Gmail Top Senders

This script fetches emails from Gmail API and calculates the top senders by storage usage.

## Setup

1. **Clone the repository**
3. **Set up Google API credentials:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Enable the Gmail API for your project.
    - Create OAuth 2.0 credentials and download the [credentials.json](https://support.google.com/cloud/answer/6158849?hl=en) file.
    - Place the `credentials.json`) file in the root directory of this project.
2. **Prerequisites**

    Ensure you have `uv` installed. If not, [install](https://docs.astral.sh/uv/getting-started/installation/) it using:

    ```sh
    pip install uv
    ```

## Usage

1. **Run the script:**

    ```sh
    uv run gmail-top-senders.py
    ```

2. **Authenticate:**

    The first time you run the script, it will open a browser window for you to authenticate with your Google account and grant the necessary permissions.

3. **View results:**

    The script will fetch your emails and display the top senders by storage usage.

