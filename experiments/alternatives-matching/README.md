# Pharmaceutical Alternatives Matching Experiment

This experiment implements an AI-powered system to find alternative pharmaceutical products from wholesaler databases. The system identifies potential cost-saving opportunities by matching generic drugs from a product report with similar products available from ParMed and BluPax wholesalers.

## Overview

The experiment consists of a three-stage pipeline:
1. **Data Fetching** - Extract unique products from wholesaler databases
2. **Preprocessing** - Find potential matches using keyword-based search
3. **AI Prediction** - Use OpenAI to intelligently select the best alternatives

## Data Sources

### Input Data
- **Product Report**: Top 1000 generic drug predictions (`product-report-top-1000-generic-predictions.csv`)
- **ParMed Database**: `wholesaler_tracking.parmed` table (PostgreSQL)
- **BluPax Database**: `wholesaler_tracking.blupax` table (PostgreSQL)

### Generated Data Files
- `unique_parmed_samples.csv` - Unique ParMed products with minimum prices (801 records)
- `unique_blupax_samples.csv` - Unique BluPax products with minimum prices (4,952 records) 
- `product-report-top-1000-preprocessed.csv` - Preprocessed report with potential matches (114 records)
- `product-report-top-1000-alternative-predictions.csv` - Final predictions with AI-selected alternatives

## Scripts

### 1. fetch.py
Extracts unique pharmaceutical products from both wholesaler databases.

**Purpose**: Create deduplicated datasets from raw wholesaler data with minimum pricing information.

**Key Features**:
- Connects to PostgreSQL database using `POSTGRES_CONNECTION_STRING` environment variable
- Groups products by key attributes (description, manufacturer, strength, etc.)
- Calculates minimum price for each unique product combination
- Saves results to CSV files for offline processing

**Usage**:
```bash
python fetch.py
```

**Requirements**: 
- PostgreSQL connection string in environment variables
- `psycopg2` for database connectivity

### 2. preprocess.py
Preprocesses the product report to identify potential alternative matches.

**Purpose**: Find candidate alternatives using keyword-based matching before expensive AI processing.

**Algorithm**:
- Filters product report to generic drugs only
- Extracts primary keywords from product descriptions and ingredient names
- Searches through ParMed and BluPax text representations for keyword matches
- Flags products with potential alternatives and stores match indices

**Key Features**:
- Handles short keywords (≤3 characters) by combining multiple terms
- Creates JSON text representations for efficient searching
- Tracks match counts and indices for downstream processing

**Usage**:
```bash
python preprocess.py
```

### 3. predict.py
Uses OpenAI's API to intelligently select the best alternative from potential matches.

**Purpose**: Apply AI reasoning to select the most appropriate alternative from candidate matches.

**Algorithm**:
- For each product with potential alternatives, constructs a structured prompt
- Sends product details and alternative options to OpenAI
- Receives structured response with selected alternative index and reasoning
- Extracts pricing and description data for selected alternatives

**Key Features**:
- Uses OpenAI prompt template (ID: `pmpt_686e6e307768819395b8d349ed4c12f10341e5bc38652685`)
- Validates AI responses and handles invalid selections
- Saves incremental results during processing
- Provides detailed reasoning for each selection

**Usage**:
```bash
python predict.py
```

**Requirements**:
- OpenAI API key in environment variables
- `openai` Python library

## Environment Setup

### Required Environment Variables
```bash
POSTGRES_CONNECTION_STRING=postgresql://user:password@host:port/database
OPENAI_API_KEY=your_openai_api_key
```

### Python Dependencies
```bash
pip install pandas psycopg2-binary openai python-dotenv
```

## Workflow

1. **Setup Environment**: Configure database connection and OpenAI API key
2. **Fetch Data**: Run `fetch.py` to extract wholesaler data
3. **Preprocess**: Run `preprocess.py` to find potential matches
4. **Predict**: Run `predict.py` to get AI-selected alternatives

## Output Analysis

The final output (`product-report-top-1000-alternative-predictions.csv`) contains:
- Original product information (description, ingredient, supplier, cost)
- Alternative matches from both ParMed and BluPax
- AI reasoning for alternative selection
- Pricing comparison data
- Match confidence indicators

## Use Cases

- **Cost Optimization**: Identify cheaper alternatives for pharmaceutical procurement
- **Supply Chain Diversification**: Find alternative suppliers for critical medications
- **Market Analysis**: Compare pricing across different wholesaler networks
- **Procurement Decision Support**: Provide data-driven alternative recommendations

## Limitations

- Keyword matching may miss semantically similar but textually different products
- AI selection quality depends on prompt engineering and model capabilities
- Database connectivity required for fresh data fetching
- Processing time scales with number of potential matches

## Future Improvements

- Implement semantic similarity search using embeddings
- Add batch processing for larger datasets
- Include additional wholesaler data sources
- Develop confidence scoring for match quality
- Add automated validation of AI selections 