# Nicehash Mining Stats -> Google Sheets Bot

Collects information about mining rigs from Nicehash API and writes to Google Sheets.

## Usage

1. Create readonly Nicehash API key. Details are here: https://www.nicehash.com/docs/

2. Create `nicehash.json` file and fill in the API key and secret. Refer to `nicehash.example.json`. Multiple rigs and devices supported.

3. Create Google API Service Account for Google Sheets. Refer to https://pygsheets.readthedocs.io/en/stable/authorization.html.

4. Create Google Sheets document and add new service account as a collaborator.

5. Download service account JSON credentials and put then in the `google-sa.json`. Refer to `google-sa.example.json`.

6. Install dependencies.

7. Run `nicehash-mining-stats-bot.py` and/or `nicehash-mining-stats-bot.py`.

- `pipenv run python /app/nicehash-account-stats-bot.py`
- `pipenv run python /app/nicehash-mining-stats-bot.py`

You can setup cron job to make such records periodically.
