# Expressive profile generator

Adapted from [AlexJamesHQ/AlexJamesHQ](https://github.com/AlexJamesHQ/AlexJamesHQ). The original copyright and MIT license are included in `LICENSE-AlexJamesHQ.txt`.

Edit `profile.json` to change the profile, links, text, and layout configuration. The SVG builder and palette follow the reference design; the avatar is circular and project thumbnails are added at the owner's request.

The workflow `.github/workflows/expressive-profile.yml` refreshes public repository, language, contribution and streak data every six hours and on manual dispatch. If the GitHub API or contribution service is unavailable, the job fails without replacing the previous cards with invented statistics. Language totals count bytes in non-fork public repositories; stars include public forks. Contribution and streak data come from github-contributions-api.jogruber.de and cover the current UTC calendar year.

To regenerate locally from the `expressive` directory, install dependencies with `npm ci`, provide a GitHub token as `GITHUB_TOKEN` to `python3 scripts/update_stats.py`, and run `npm run generate`. Never commit the token.
