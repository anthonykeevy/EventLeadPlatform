# Discover Data Sources Workflow
# Investigate available public data sources for a domain

## Purpose
Research and evaluate available data sources (APIs, databases, web scraping) for collecting real-world data.

## Workflow

### Step 1: Define Scope
<ask>Which domain are you researching data sources for?</ask>
<ask>What geographic regions are relevant? (e.g., Australia, Global)</ask>

### Step 2: Research Public APIs
<action>Investigate available public APIs</action>
- Coverage and data quality
- Free tier limits
- Paid tier costs
- Rate limits and terms of service

### Step 3: Identify Public Databases
<action>Research public databases and registries</action>
- Government databases
- Tourism boards
- Industry registries
- Academic datasets

### Step 4: Evaluate Web Scraping Opportunities
<action>Assess web scraping potential</action>
- Terms of service compliance
- Data quality and freshness
- Maintenance overhead
- Legal considerations

### Step 5: Cost-Benefit Analysis
<action>Compare sources and recommend integration priority</action>

<template-output>
## Data Sources Analysis - {{Domain}}

### Tier 1: Recommended
[High-quality sources with good ROI]

### Tier 2: Supplementary
[Additional sources for completeness]

### Not Recommended
[Sources with issues or poor ROI]

### Strategic Recommendation
[Which approach: API integration, web scraping, manual curation]
</template-output>

