# Analyze Domain Workflow
# Dimitri's primary command: Complete domain analysis

## Workflow Steps

### Step 1: Understand the Domain
<ask>Which domain would you like me to analyze? (e.g., Event, Lead, Submission, Company, Form)</ask>

<ask>What's the business context? Tell me how users will interact with this domain:</ask>
- What problems does it solve?
- What are the edge cases? (e.g., "formal events vs hair salon scenario")
- Any specific competitors to research?

### Step 2: Industry Research (Phase 1)
<action>Research industry data patterns for {{domain}}</action>

I'm investigating:
- ✓ Competitor platforms (how do leaders structure this data?)
- ✓ Industry standards (what fields are common across the market?)
- ✓ Real-world examples (finding 50-100 actual instances)
- ✓ Edge cases and variations (formal vs informal scenarios)

**Research Sources:**
- Leading platforms: [researching...]
- Industry documentation: [analyzing...]
- Public examples: [collecting...]

<template-output>
## {{Domain}} - Industry Research Findings

### Competitors Analyzed
1. **[Platform 1]**
   - Schema approach: [findings]
   - Key fields: [list]
   - Strengths: [observations]

2. **[Platform 2]**
   - Schema approach: [findings]
   - Key fields: [list]
   - Strengths: [observations]

### Common Patterns Discovered
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

### Edge Cases Identified
- [Edge case 1]
- [Edge case 2]

### Real-World Examples Collected
- [100 examples with details]
</template-output>

### Step 3: Data Source Intelligence (Phase 2)
<action>Discover available public data sources for {{domain}}</action>

I'm evaluating:
- ✓ Public APIs (coverage, quality, cost)
- ✓ Public databases (government, tourism, industry registries)
- ✓ Web scraping opportunities (respectful, terms-compliant)
- ✓ Legal and terms of service considerations

<template-output>
## {{Domain}} - Data Source Intelligence

### Tier 1: Recommended Sources
1. **[Source Name]**
   - Coverage: [scope]
   - Quality: [assessment]
   - Access: [free tier / paid / scraping]
   - Cost: [pricing details]
   - Legal: [terms of service analysis]
   - Recommendation: [strategic assessment]

### Tier 2: Supplementary Sources
[Additional sources...]

### Not Recommended
[Sources with issues...]

### Strategic Recommendation
[Curated database vs user-generated vs hybrid approach]
</template-output>

### Step 4: Schema Design (Phase 3)
<action>Design normalized database schema for {{domain}}</action>

Based on my research, I'm proposing:
- ✓ Primary table structure
- ✓ Industry-standard fields discovered
- ✓ Flexibility for formal + informal scenarios
- ✓ Optional relationships (where appropriate)
- ✓ Indexes and constraints (performance + data integrity)

<template-output>
## {{Domain}} - Schema Proposal

### Primary Table: {{Domain}}
```sql
CREATE TABLE {{Domain}} (
    -- Primary Key (PascalCase, [TableName]ID pattern)
    {{Domain}}ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Keys (discovered from research)
    [Fields based on industry analysis...]
    
    -- Core Fields (industry-standard fields)
    [Fields from competitive analysis...]
    
    -- Optional Fields (for flexibility)
    [Fields for edge cases...]
    
    -- Audit Trail (standard for all tables)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- Constraints
    CONSTRAINT FK_{{Domain}}_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT CK_{{Domain}}_Dates CHECK (CreatedDate <= ISNULL(UpdatedDate, '9999-12-31'))
);

-- Indexes (based on expected queries)
CREATE INDEX IX_{{Domain}}_[Field] ON {{Domain}}([Field]);
```

### Related Tables
[Any junction or dependent tables...]

### ERD
[ASCII or description of relationships]

### Design Rationale
**Formal vs Informal Scenarios:**
[How schema handles both structured and unstructured cases]

**Flexibility:**
[Optional relationships, nullable fields, extensibility]

**Industry Alignment:**
[How this matches/exceeds competitor schemas]
</template-output>

### Step 5: Generate Seed Data (Phase 4)
<action>Generate test and production seed data from research</action>

Creating two separate data sets:

**Test Data (Development/Testing):**
- Verbose, varied examples
- Edge cases (hair salon, cancelled events, etc.)
- Clearly labeled as TEST DATA

**Production Data (Launch Seed):**
- Clean, verified real examples
- Source attribution included
- Ready for production deployment

<template-output>
## {{Domain}} - Seed Data Generated

### Test Data
**File:** `database/seeds/test/{{domain}}_test_data.sql`

**Contents:**
- 50 varied examples
- Edge cases: [list unusual scenarios]
- Clearly marked: `-- TEST DATA - DO NOT USE IN PRODUCTION`

### Production Seed Data
**File:** `database/seeds/production/{{domain}}_production_seed.sql`

**Contents:**
- 50 verified real examples
- Sources: [Eventbrite API (30), ICC Sydney (10), Tourism NSW (10)]
- Attribution included in comments
- Ready for production import

### Data Governance
✓ Test and production data COMPLETELY SEPARATE
✓ Clear labeling in file headers
✓ Source attribution for production data
✓ Never pollute production with test data
</template-output>

### Step 6: Strategic Recommendations (Phase 5)
<action>Analyze trade-offs and recommend strategic approach</action>

Based on my research, here are the strategic options:

<template-output>
## {{Domain}} - Strategic Recommendations

### Option A: Curated Database
**Approach:** You maintain a database of {{domain}} records; users select from your list

**Pros:**
- [Benefits from research]

**Cons:**
- [Limitations from analysis]

**Example:** [Competitor who does this]

### Option B: User-Generated Only
**Approach:** Users create all {{domain}} records manually

**Pros:**
- [Benefits]

**Cons:**
- [Limitations]

**Example:** [Competitor who does this]

### Option C: Hybrid (RECOMMENDED)
**Approach:** Curated database + user additions

**Pros:**
- [Benefits of both approaches]

**Cons:**
- [Managed complexity]

**Example:** [Competitor who does this successfully]

### My Recommendation
Based on competitive analysis and your platform needs:
[Strategic recommendation with rationale]

### Implementation Approach
[Phased rollout suggestion]
</template-output>

### Step 7: Dashboard Metrics Recommendation
<action>Recommend KPIs for UX Expert based on industry standards</action>

<template-output>
## {{Domain}} - Dashboard Metrics Recommendations

### For UX Expert (Dashboard Design)
Based on what users expect to see (learned from competitors):

**Key Metrics:**
1. [Metric 1] - "Users expect this because [industry pattern]"
2. [Metric 2] - "Competitors show this prominently"
3. [Metric 3] - "Strategic differentiation opportunity"

**Visualization Suggestions:**
- [Chart type] for [metric] (industry standard approach)
- [Chart type] for [metric] (competitive analysis)

**User Expectations:**
[What the market has taught users to expect]
</template-output>

### Step 8: Product Enhancement Suggestions
<action>Suggest features to Product Manager based on competitive gaps</action>

<template-output>
## {{Domain}} - Product Enhancement Suggestions

### For Product Manager (Roadmap Planning)

**Competitive Parity (Must-Have):**
1. [Feature] - "All competitors have this; table stakes"
2. [Feature] - "Industry standard expectation"

**Competitive Advantage (Differentiators):**
1. [Feature] - "Opportunity: Only 1 competitor does this well"
2. [Feature] - "Gap: No competitor does this; we could lead"

**Emerging Trends (Future-Proofing):**
1. [Feature] - "20% of market moving toward this"
2. [Feature] - "Early adopter opportunity"

**Prioritization:**
[Recommendations based on market adoption vs effort]
</template-output>

### Step 9: Export Complete Findings
<action>Generate comprehensive analysis report</action>

I've created:
- ✓ Domain analysis document: `docs/data-domains/{{domain}}-analysis.md`
- ✓ Schema proposal SQL: `database/schemas/{{domain}}-schema.sql`
- ✓ Test seed data: `database/seeds/test/{{domain}}_test.sql`
- ✓ Production seed data: `database/seeds/production/{{domain}}_production.sql`
- ✓ Data dictionary: `docs/data-domains/{{domain}}-dictionary.md`

<template-output>
## Analysis Complete! 🎉

### Deliverables Created:
1. **Industry Research** - Competitive analysis and data patterns
2. **Data Source Intelligence** - Available APIs, costs, recommendations
3. **Schema Proposal** - Normalized database design (validated against Solomon's standards)
4. **Seed Data** - Test (50 examples) + Production (50 verified)
5. **Strategic Recommendations** - Curated vs user-generated approach
6. **Dashboard Metrics** - For UX Expert
7. **Product Enhancements** - For Product Manager

### Next Steps:
1. **Review schema proposal** with team
2. **Validate with Solomon** (Database Migration Validator)
3. **Share metrics** with UX Expert for dashboard design
4. **Share enhancements** with Product Manager for roadmap
5. **Import seed data** when ready for testing/production

### Questions or Refinements?
I can dive deeper into any section, compare additional competitors, or adjust the schema based on your feedback!
</template-output>

---

**Workflow Complete!** Dimitri has performed comprehensive domain analysis with strategic intelligence and practical deliverables.

