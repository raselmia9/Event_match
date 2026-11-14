# Event_match - Live Sports Data Auto-Updater

This repository automatically fetches sports data from the upstream source, converts it into the custom target format, and updates every 15 minutes via GitHub Actions.

## Raw JSON URL
You can access the live converted JSON directly:
`https://raw.githubusercontent.com/raselmia9/Event_match/main/matches.json`

## Features
- **Auto Update**: GitHub Actions workflow (`.github/workflows/update.yml`) runs every 15 minutes.
- **Manual Trigger**: Can also be triggered manually from the "Actions" tab.
- **Custom Formatting**: Automatically maps match time, team titles, team flags, category titles, and combines stream links with headers.
