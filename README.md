# AI Article Writer

App Streamlit de tao bai viet bang AI.

## Input

- `Idea`: y tuong bai viet
- `Max words`: gioi han so chu toi da

## Output

- Mot bai viet hoan chinh dang Markdown

## Cong nghe

- Streamlit
- DeepSeek API
- Model: `deepseek-v4-flash`

## Chay local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Cau hinh API key

Tao file `.streamlit/secrets.toml`:

```toml
DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_MODEL = "deepseek-v4-flash"
```

Co the dung bien moi truong `DEEPSEEK_API_KEY` neu khong muon dung secrets.

## Deploy len Streamlit Community Cloud

1. Day project len GitHub.
2. Vao Streamlit Community Cloud va tao app moi.
3. Chon repo nay, file chay la `app.py`.
4. Them secret:

```toml
DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_MODEL = "deepseek-v4-flash"
```

## Luu y

- App nay yeu cau dung API key DeepSeek hop le.
- Model mac dinh la `deepseek-v4-flash`, nhung co the doi bang `DEEPSEEK_MODEL` trong secrets.
