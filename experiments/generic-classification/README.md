# Pharmaceutical Generic Classification Experiment

This experiment implements an AI-powered classification system to identify whether pharmaceutical products are brand-name or generic drugs. The system analyzes product information and provides detailed insights about generic availability, alternative manufacturers, and classification reasoning.

## Overview

The experiment uses OpenAI's API to intelligently classify pharmaceutical products based on:
- Product descriptions
- NDC (National Drug Code) numbers
- Primary ingredient information
- Route of administration

## Purpose

**Primary Goal**: Automatically classify pharmaceutical products as brand-name or generic drugs to support:
- Cost optimization strategies
- Procurement decision-making
- Generic substitution opportunities
- Market analysis and competitive intelligence

## Data Sources

### Input Data
- **Product Report**: Complete pharmaceutical product dataset (`product-report-full.csv`)
  - Contains product descriptions, NDC codes, ingredients, routes, pricing, and supplier information
  - Full dataset processed up to 1000 records for analysis

### Output Data
- **Classified Report**: AI-enhanced dataset with classification results (`product-report-top-1000-with-predictions.csv`)
  - Original product data plus AI-generated classifications
  - Brand status, generic availability, manufacturer information, and reasoning

## Script Documentation

### predict.py
Main classification script that processes pharmaceutical products through AI analysis.

**Purpose**: Classify products as brand-name or generic and identify alternative options.

**Algorithm**:
1. Load product report data from CSV
2. Initialize new classification columns
3. For each product (up to 1000 records):
   - Extract key product attributes (NDC, ingredient, description, route)
   - Send structured data to OpenAI classification prompt
   - Parse AI response for classification results
   - Store results with error handling
   - Save incremental progress

**Key Features**:
- **Incremental Processing**: Saves results after each classification to prevent data loss
- **Error Handling**: Captures and logs processing errors with fallback values
- **Progress Tracking**: Displays real-time processing status and results
- **Structured Output**: Generates consistent JSON-formatted responses

**AI Classification Output**:
- `brand_status`: Classification as "Brand" or "Generic"
- `generic_alternative_available`: Boolean indicating if generic alternatives exist
- `generic_manufacturers`: List of manufacturers producing generic versions
- `reasoning`: AI explanation for the classification decision

**Usage**:
```bash
python predict.py
```

**Requirements**:
- OpenAI API key in environment variables
- `openai`, `pandas`, `python-dotenv` libraries

## Environment Setup

### Required Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
```

### Python Dependencies
```bash
pip install pandas openai python-dotenv
```

## Workflow

1. **Setup Environment**: Configure OpenAI API key
2. **Data Loading**: Read full product report dataset
3. **AI Classification**: Process each product through OpenAI prompt
4. **Result Storage**: Save classified data with reasoning
5. **Analysis**: Review classification patterns and insights

## AI Prompt Integration

The system uses a specialized OpenAI prompt template:
- **Prompt ID**: `pmpt_686a6cae5a5081939975224e71d812f10848a83d45ec9a02`
- **Version**: 4
- **Input Variables**: NDC, ingredient, product description, administration route
- **Output Format**: Structured JSON with classification fields

## Classification Methodology

### Brand vs Generic Determination
The AI analyzes multiple factors:
- Product naming conventions (brand names vs generic chemical names)
- NDC patterns and manufacturer codes
- Ingredient formulations and strengths
- Market positioning indicators

### Generic Alternative Identification
For brand-name drugs, the system identifies:
- Available generic manufacturers
- Market availability status
- Regulatory approval information
- Cost-saving opportunities

## Output Analysis

The classified dataset enables analysis of:
- **Brand/Generic Distribution**: Market composition insights
- **Cost Optimization Opportunities**: Identify expensive brand drugs with generic alternatives
- **Supplier Diversification**: Map generic manufacturer options
- **Procurement Strategy**: Data-driven generic substitution decisions

## Use Cases

### Healthcare Organizations
- **Formulary Management**: Optimize drug formularies with generic preferences
- **Cost Reduction**: Identify high-impact generic substitution opportunities
- **Budget Planning**: Forecast savings from generic adoption

### Pharmaceutical Procurement
- **Supplier Strategy**: Diversify sources through generic manufacturer identification
- **Contract Negotiation**: Leverage generic alternatives in pricing discussions
- **Market Intelligence**: Track brand vs generic market dynamics

### Research and Analysis
- **Market Studies**: Analyze generic penetration and availability
- **Competitive Intelligence**: Monitor generic manufacturer landscape
- **Policy Research**: Support generic drug policy development

## Performance Metrics

### Processing Statistics
- **Dataset Size**: Full product report (variable size)
- **Analysis Scope**: Top 1000 products processed
- **Success Rate**: Error handling ensures robust classification
- **Processing Time**: Sequential API calls (approximately 1-2 seconds per product)

### Classification Accuracy
- **AI-Powered**: Leverages advanced language models for nuanced analysis
- **Context-Aware**: Considers multiple product attributes simultaneously
- **Reasoning-Based**: Provides explanations for each classification decision

## Limitations

- **API Dependency**: Requires OpenAI API access and quota management
- **Processing Speed**: Sequential API calls limit throughput
- **Cost Considerations**: API usage costs scale with dataset size
- **Data Quality**: Classification accuracy depends on input data completeness

## Future Improvements

### Technical Enhancements
- **Batch Processing**: Implement parallel API calls for faster processing
- **Caching System**: Store and reuse classifications for similar products
- **Confidence Scoring**: Add classification confidence metrics
- **Model Fine-tuning**: Train specialized models on pharmaceutical data

### Analytical Extensions
- **Price Impact Analysis**: Calculate potential savings from generic substitution
- **Market Trend Tracking**: Monitor classification changes over time
- **Regulatory Integration**: Include FDA approval status and timing
- **Therapeutic Equivalence**: Add bioequivalence and therapeutic substitution data

## Integration Opportunities

- **ERP Systems**: Direct integration with procurement and inventory systems
- **Decision Support**: Real-time classification during purchasing decisions
- **Analytics Dashboards**: Visualization of classification insights and trends
- **Compliance Tools**: Support regulatory reporting and audit requirements 