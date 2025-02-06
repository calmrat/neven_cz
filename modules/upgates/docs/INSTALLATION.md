
# 🚀 Upgatescz API - Version 2.2.0 Documentation

## 📥 Installation & Setup

### 1️⃣ Download & Extract
```bash
unzip upgatescz_api_v2.2.0_full.zip
cd upgatescz_api
```

### 2️⃣ Configure Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

### 3️⃣ Install Dependencies
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install --system
```

### 4️⃣ Set Up Configuration
Edit `upgates/config/config.toml` and update API keys:
```toml
[upgates]
api_url = "https://api.upgates.cz/v2"
api_key = "your-api-key-here"
sync_interval_minutes = 30

[openai]
enabled = true
api_key = "your-openai-key-here"
default_model = "gpt-4o-mini"
```

### 5️⃣ Running the CLI
```bash
python -m upgates.cli --help
```

#### Run a Full Sync
```bash
python -m upgates.cli sync_all
```

#### Translate Product Descriptions (After Syncing)
```bash
python -m upgates.cli translate_descriptions --lang en --product-ids 12345,67890
```

### 6️⃣ Running in Docker (Optional)
```bash
docker-compose up --build -d
```

### 7️⃣ Running Tests
```bash
pytest upgates/tests/
```

## 🎯 Summary of Commands
| **Action** | **Command** |
|-----------|------------|
| Full Sync | `python -m upgates.cli sync_all` |
| Translate Descriptions | `python -m upgates.cli translate_descriptions --lang en` |
| Start Webhooks | `python -m upgates.cli start_webhook` |
| Run in Docker | `docker-compose up --build -d` |
| Run Tests | `pytest upgates/tests/` |

🚀 **Upgatescz API is now fully installed and ready for use!**
