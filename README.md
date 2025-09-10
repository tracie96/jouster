# Jouster LLM Knowledge Extractor

A FastAPI-based service that extracts structured data and summaries from unstructured text using OpenAI's GPT-3.5-turbo model.

## Features

- **Text Analysis**: Generate 1-2 sentence summaries and extract structured metadata
- **Keyword Extraction**: Custom implementation to find the 3 most frequent nouns
- **Structured Data**: Extract title, topics, sentiment, and keywords
- **Cloud Database**: Supabase PostgreSQL for scalable data storage
- **Search**: Find analyses by topic or keyword
- **Robust Error Handling**: Graceful handling of empty input and LLM API failures
- **Cloud Ready**: Full Supabase integration with PostgreSQL
- **Minimal UI**: Focused on robust API design for easy integration and testing

## Setup Instructions

### Prerequisites

- Python 3.8+
- OpenAI API key
- And Supabase account

### Installation

1. **Clone and navigate to the project directory:**
   ```bash
   cd /Users/mac/Desktop/projects/jouster
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=your_actual_api_key_here
   # SUPABASE_URL=your_supabase_project_url
   # SUPABASE_KEY=your_supabase_anon_key
   # SUPABASE_DB_PASSWORD=your_database_password
   ```

4. **Set up Supabase database:**
   - Go to your Supabase project dashboard
   - Navigate to SQL Editor
   - Run the SQL commands from `supabase_schema.sql`

5. **Run the application:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

6. **View API documentation:**
   - Interactive docs: `http://localhost:8000/docs`

### Testing

Run the test script to verify functionality:

```bash
python test_api.py
```

## API Endpoints

### `POST /analyze`
Analyze text and extract structured data.

**Request:**
```json
{
  "text": "Your text to analyze here..."
}
```

**Response:**
```json
{
  "id": 1,
  "summary": "1-2 sentence summary",
  "title": "Extracted title or null",
  "topics": ["topic1", "topic2", "topic3"],
  "sentiment": "positive|neutral|negative",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "created_at": "2024-01-01T12:00:00"
}
```

### `GET /search?topic=xyz`
Search for analyses containing a specific topic or keyword.

### `GET /analyses`
Get all stored analyses.

### `GET /health`
Health check endpoint.


## Design Choices

**Architecture**: I chose FastAPI for its excellent automatic API documentation, built-in validation with Pydantic, and async support. The modular structure separates concerns: database models, LLM service, keyword extraction, and API endpoints are in separate files for maintainability.

**Database**: Supabase PostgreSQL provides a scalable, cloud-native database with JSONB support for efficient storage and querying of structured data. The database includes proper indexing, and real-time capabilities.

**LLM Integration**: OpenAI's GPT-3.5-turbo provides reliable text analysis with structured JSON output. The service includes proper error handling for API failures and validates responses before processing.

**Keyword Extraction**: I implemented a custom noun extraction algorithm using NLTK instead of relying on the LLM, as specified in the requirements. This approach is more deterministic and doesn't consume additional API tokens.

## Trade-offs Made

**Time Constraints**: Due to the 90-minute timebox, I focused on core functionality over advanced features. I created minimal UI approach due to the time

**Error Handling**: While I implemented the required edge cases (empty input, LLM failures), more comprehensive error handling and retry logic could be added for production use.

**Testing**: I created a basic test script but didn't implement formal unit tests due to time constraints. The test script covers the main API endpoints and edge cases.

**Security**: The current implementation doesn't include authentication or rate limiting, which would be necessary for production deployment.

## Project Structure

```
jouster/
├── main.py                # Endpoints section
├── supabase_service.py    # Supabase client service
├── models.py              
├── llm_service.py         # OpenAI integration and text analysis
├── keyword_extractor.py  
├── test_api.py           # Test script for API endpoints
├── test_unit.py          # Unit tests
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    
├── Makefile              # Development automation
├── .gitignore          
├── supabase_schema.sql  # Supabase database schema
└── README.md            
```

## You can also quick start with Make

```bash
make setup
source venv/bin/activate
make install

make run

make test

make clean
```

## Docker Deployment

```bash
make docker-run

docker build -t jouster-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here jouster-api
```

## Example Usage

```bash
python main.py

curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Artificial Intelligence is transforming industries worldwide."}'

curl "http://localhost:8000/search?topic=AI"
```
