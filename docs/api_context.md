# API Documentation & Context for Agents

## 1. X API v2 (Data Extraction)

**Base URL**: `https://api.x.com/2`
**Authentication**: Bearer Token (OAuth 2.0)

### Endpoints

#### User Likes
**GET** `/2/users/:id/liked_tweets`
- **Purpose**: Fetch tweets liked by a specific user.
- **Parameters**: `max_results` (10-100), `pagination_token`, `tweet.fields` (e.g., `created_at,author_id`).
- **Response**:
  ```json
  {
    "data": [
      { "id": "123", "text": "Tweet text..." }
    ],
    "meta": { "next_token": "..." }
  }
  ```

#### User Reposts (Timeline)
**GET** `/2/users/:id/tweets`
- **Purpose**: Fetch a user's timeline to identify reposts.
- **Parameters**: `exclude=replies`, `max_results`.
- **Note**: To find reposts, filter results where `referenced_tweets.type == "retweeted"`.

#### User Lookup
**GET** `/2/users/by/username/:username`
- **Purpose**: Resolve handle to User ID.
- **Response**: `{ "data": { "id": "...", "username": "..." } }`

---

## 2. Grok API (xAI SDK)

**Package**: `xai_sdk`
**Authentication**: `XAI_API_KEY` env var.

### Usage Pattern

```python
from xai_sdk import Client
from xai_sdk.chat import user, system

client = Client()
chat = client.chat.create(model="grok-beta")

chat.append(system("You are a helpful assistant."))
chat.append(user("Analyze this data..."))

response = chat.sample()
print(response.content)
```

### Models
- `grok-beta`: Standard model.
- `grok-vision-beta`: Multimodal capabilities.

---

## 3. X Ads API (Boilerplate)

**Base URL**: `https://ads-api.x.com/12`
**Authentication**: OAuth 1.0a (User Context)

### Key Endpoints (Stubbed)

#### List Accounts
**GET** `/12/accounts`
- **Purpose**: Get Ad Account IDs accessible to the user.

#### Create Tweet (Dark Post)
**POST** `/12/accounts/:account_id/tweets`
- **Purpose**: Create a "nullcast" tweet for ads.

#### Create Line Item
**POST** `/12/accounts/:account_id/line_items`
- **Purpose**: Set up targeting and bid strategy.



