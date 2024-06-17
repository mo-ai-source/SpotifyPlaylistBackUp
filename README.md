# SpotifyPlaylistBackUp
A tool to backup Spotify playlists using the Spotify Web API
# Spotify Playlist Backup

A tool to backup your Spotify playlists using the Spotify Web API. This project allows you to authenticate with your Spotify account, fetch your playlists, and export them as CSV files.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Authenticate with your Spotify account using the Authorization Code Flow
- Fetch your public and private playlists
- Export playlists as CSV files
- User-friendly web interface to input playlist IDs and initiate the backup process

## Prerequisites

Before running the Spotify Playlist Backup tool, ensure you have the following:

- Python 3.x installed on your machine
- A Spotify Developer account and a registered application

## Installation

1. Clone the repository:


## Usage

1. Run the Flask application:

```
python app.py

```




2. Open your web browser and navigate to `http://localhost:5000`.

3. Click on the "Login with Spotify" button to authenticate with your Spotify account.

4. Once authenticated, you will be redirected to the main page where you can input a playlist ID and click the "Backup" button to initiate the backup process.

5. The playlist will be fetched, and a CSV file containing the playlist data will be downloaded automatically.

## Configuration

Before running the application, make sure to update the following configuration variables in the `app.py` file:

- `CLIENT_ID`: Replace with your Spotify application's client ID.
- `CLIENT_SECRET`: Replace with your Spotify application's client secret.
- `REDIRECT_URI`: Update with the redirect URI registered in your Spotify application settings.

## Contributing

Contributions to the Spotify Playlist Backup project are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, please open an issue or submit a pull request.

When contributing to this project, please follow the existing code style and guidelines.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.

---

If you have any questions or need further assistance, tweet me at @mo_y5f
