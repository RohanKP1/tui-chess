# TUI Chess

A simple text-based chess interface you can play in the terminal.

## Features
- Coordinate-labeled board with Unicode chess pieces (ASCII fallback prepared)
- Basic move validation for all pieces (no castling, check rules, or en passant yet)
- Clean CLI with input validation

## Run

```bash
python main.py
```

At startup, select a mode:

- `1` Human vs Human
- `2` Human (White) vs LLM (Black)
- `3` LLM (White) vs Human (Black)
- `4` LLM vs LLM

Enter moves as coordinates (e.g., `E2 E4`):

```
E2 E4
G8 F6
```

Type `exit` to quit.

## Notes
- This engine validates piece movement and captures but does not implement check, checkmate, castling, promotion, or en passant.
- Unicode rendering works in most terminals. If your terminal shows squares incorrectly, consider changing font.

## LLM configuration (optional)
To enable the LLM agent via Azure OpenAI, set the following environment variables before running:

```bash
set AZURE_OPENAI_API_VERSION=<your_api_version>
set AZURE_OPENAI_DEPLOYMENT=<your_deployment_name>
set AZURE_OPENAI_ENDPOINT=https://<your-endpoint>
set AZURE_OPENAI_API_KEY=<your_key>
```

or put these variables in .env file at source location.

If these are not set or libraries are unavailable, the agent falls back to random legal moves.