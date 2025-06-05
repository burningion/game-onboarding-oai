# Gamified Onboarding for OpenAI Agents Hackathon NYC

# Repo structure

This repo uses `uv` for dependencies. You can do a `uv sync`, and you should have all of the Python dependencies to run the repo.

There's a React frontend that lives in `frontend/`, and you can just do an `npm start` to get that running too.

Images, etc. get put in `assets/`.

We use Doppler to manage secrets. To install:

```
brew install gnupg
brew install dopplerhq/cli/doppler
doppler login
```

Followed by a:

```
doppler run -- uv run main.py 
```
