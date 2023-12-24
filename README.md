# BBC URL to txt

Two sccripts:

- takes bbc radio playlist url and saves the tracks as txt
- takes the txt file and creates a spotify playlist

## Install

`poetry install`

## Usage

```
poetry run python bbc_url_to_txt.py -url {url} --output-filepath {full_path.txt}
```

Example:

```
python bbc_url_to_txt.py -url https://www.bbc.co.uk/sounds/play/m001tj4b --output-filepath playlist.txt
```

# Move playlist to spotify

```commandline
cp .test.env .env
```

Fill in the `.env` file with your spotify credentials

Then, run the

```commandline
poetry run python bbc_to_spotify/main.py --playlist playlist.txt --playlist-name "Gilles Peterson 2023-12-23"
```
