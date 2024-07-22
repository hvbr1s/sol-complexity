#### User guide on macOS:
1. In your working folder, create `venv` and activate it.
2. Run `pip install -r requirements.txt` in your venv.
3. Run `npm install -g mermaid.cli`
4. In the root directory, create `.env` file and set a `OPENAI_API_KEY="<your_value>"` variable.
5. In the root directory, create the following empty folders -> `/bin`, `/docs` and `/output`.
6. Add a `.sol` contract to the `/docs` folder.
7. Run `app_gpt.py`.
