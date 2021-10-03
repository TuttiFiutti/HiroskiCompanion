## Usage
```
pip install -r requirements.txt
# turn on hirki and start game
uvicorn main:app --reload
```

## Known issues

- I see `pymem.exception.CouldNotOpenProcess: Could not open process` after updating heroes

    - Updating heroes makes the game launch with administrative privileges.
      Just close the HD Launcher and start HOTA again. Alternatively you can start `python` as admin. 