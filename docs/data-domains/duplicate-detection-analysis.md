# Duplicate Event Detection - Complexity Analysis

**Author:** Dimitri (Data Domain Architect)  
**Date:** October 13, 2025  
**Context:** User-generated events may create duplicates (e.g., "CES 2025" vs "Consumer Electronics Show 2025")

---

## Problem Statement

When users add events, they may create duplicates:
- **Exact Duplicates:** "CES 2025" vs "CES 2025" (typo, didn't search first)
- **Near Duplicates:** "CES 2025" vs "Consumer Electronics Show 2025" (different names, same event)
- **Variation Duplicates:** "CeBIT Australia" vs "CeBIT Australia 2025" vs "CEBIT Australia 2025"

**Goal:** Detect potential duplicates and prompt user: "Did you mean this existing event?"

---

## Approach 1: Exact String Matching (Trivial Complexity)

### **Algorithm:**
```sql
-- Check if event with same name + date + city exists
SELECT EventID, Name, StartDateTime, City
FROM [Event]
WHERE Name = @NewEventName
  AND StartDateTime = @NewEventStartDateTime
  AND City = @NewEventCity
  AND IsDeleted = 0;
```

### **Complexity:**
- **Development:** 1-2 hours (simple SQL query)
- **Performance:** O(log n) with index (very fast)
- **Accuracy:** Only catches exact duplicates

### **Pros:**
- ✅ Extremely fast
- ✅ Zero false positives
- ✅ Simple to implement

### **Cons:**
- ❌ Misses near-duplicates ("CES 2025" vs "Consumer Electronics Show 2025")
- ❌ Case-sensitive (unless you use COLLATE)

### **Recommendation:** 🎯 **Use as baseline** (MVP must-have)

---

## Approach 2: Fuzzy String Matching (Moderate Complexity)

### **Algorithm: Levenshtein Distance**

Measures "edit distance" between two strings (how many character changes needed to transform one into the other).

```sql
-- T-SQL implementation (simplified)
-- Levenshtein distance between two strings
CREATE FUNCTION dbo.LevenshteinDistance(@s1 NVARCHAR(4000), @s2 NVARCHAR(4000))
RETURNS INT
AS
BEGIN
    -- Implementation: Dynamic programming matrix
    -- Returns: Number of edits (insert, delete, substitute) to transform s1 → s2
    -- Example: "CES 2025" → "CES  2025" (extra space) = distance of 1
END;

-- Find potential duplicates
SELECT EventID, Name, StartDateTime, City,
       dbo.LevenshteinDistance(LOWER(@NewEventName), LOWER(Name)) AS Distance
FROM [Event]
WHERE ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3  -- Within 3 days
  AND City = @NewEventCity
  AND IsDeleted = 0
HAVING Distance <= 5  -- Threshold: 5 character changes
ORDER BY Distance ASC;
```

### **Complexity:**
- **Development:** 1-2 days (write function, tune threshold)
- **Performance:** O(n * m * k) where n = length of string 1, m = length of string 2, k = number of events to compare
  - For 1,000 events: ~100ms per search (acceptable)
  - For 100,000 events: ~10 seconds (too slow, needs optimization)
- **Accuracy:** Catches typos and minor variations

### **Example Matches:**
| New Event Name | Existing Event | Distance | Match? |
|----------------|----------------|----------|--------|
| "CES 2025" | "CES  2025" (extra space) | 1 | ✅ Yes |
| "CeBIT Australia" | "CEBIT Australia" | 1 | ✅ Yes (case difference) |
| "IoT Expo" | "IOT Expo" | 1 | ✅ Yes |
| "CES 2025" | "Consumer Electronics Show 2025" | 28 | ❌ No (too different) |

### **Pros:**
- ✅ Catches typos ("CeBIT" vs "CEBIT")
- ✅ Catches minor variations
- ✅ Well-understood algorithm

### **Cons:**
- ❌ Still misses semantic duplicates ("CES" vs "Consumer Electronics Show")
- ⚠️ Performance degrades with large datasets (needs pre-filtering)
- ⚠️ Requires tuning threshold (too low = false negatives, too high = false positives)

### **Optimization:**
Pre-filter by date and city (reduces search space by 99%):
```sql
-- Only compare events in same city within ±3 days
WHERE City = @NewEventCity
  AND ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3
```

### **Recommendation:** 🎯 **Use for Phase 2** (post-MVP enhancement)

---

## Approach 3: Semantic Similarity (High Complexity)

### **Algorithm: Vector Embeddings + Cosine Similarity**

Convert event names to vectors (embeddings), then measure similarity.

```python
# Using OpenAI Embeddings API or Sentence Transformers
import openai

# Convert event names to vectors
new_event_embedding = openai.Embedding.create(
    input="CES 2025",
    model="text-embedding-ada-002"
)

existing_event_embedding = openai.Embedding.create(
    input="Consumer Electronics Show 2025",
    model="text-embedding-ada-002"
)

# Calculate cosine similarity (0 = completely different, 1 = identical)
from numpy import dot
from numpy.linalg import norm

similarity = dot(new_event_embedding, existing_event_embedding) / (
    norm(new_event_embedding) * norm(existing_event_embedding)
)
# Result: 0.92 (highly similar, probably duplicate)
```

### **Complexity:**
- **Development:** 1-2 weeks (integrate ML model, tune threshold, build pipeline)
- **Performance:** 
  - Embedding generation: 50-200ms per event (API call to OpenAI or local model)
  - Similarity search: O(n) for brute force, O(log n) with vector database (Pinecone, Weaviate)
- **Cost:** $0.0004 per 1,000 tokens (OpenAI) = ~$0.10 per 1,000 event comparisons
- **Accuracy:** Catches semantic duplicates ("CES" vs "Consumer Electronics Show")

### **Example Matches:**
| New Event Name | Existing Event | Similarity | Match? |
|----------------|----------------|------------|--------|
| "CES 2025" | "Consumer Electronics Show 2025" | 0.92 | ✅ Yes! |
| "Tech Summit" | "Technology Conference" | 0.85 | ✅ Yes |
| "Hair Salon Feedback" | "CES 2025" | 0.12 | ❌ No |

### **Pros:**
- ✅ Catches semantic duplicates (different names, same event)
- ✅ Understands abbreviations ("CES" = "Consumer Electronics Show")
- ✅ Language-agnostic (works with non-English event names)

### **Cons:**
- ❌ Expensive (API costs, compute)
- ❌ Complex infrastructure (vector database, embedding pipeline)
- ❌ Requires tuning threshold (what similarity score = duplicate?)
- ⚠️ Overkill for MVP

### **Recommendation:** ⏰ **Phase 3 (future)** - Only if user-generated events become a major pain point

---

## Approach 4: Hybrid (Best of All Worlds)

### **Strategy:**

**Step 1: Pre-filter (Exact + Date + City)**
```sql
-- Fast pre-filter: Same city, within ±3 days
WHERE City = @NewEventCity
  AND ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3
  AND IsDeleted = 0;
-- Reduces search space from 10,000 events to ~50 events
```

**Step 2: Fuzzy Match (Levenshtein)**
```sql
-- Among pre-filtered events, find close matches
SELECT EventID, Name, dbo.LevenshteinDistance(LOWER(@NewEventName), LOWER(Name)) AS Distance
FROM [Event]
WHERE City = @NewEventCity
  AND ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3
  AND IsDeleted = 0
HAVING Distance <= 5
ORDER BY Distance ASC;
```

**Step 3: Manual Review (Admin Flag)**
```sql
-- If no fuzzy match found, flag for admin review
INSERT INTO [Event] (..., Status) VALUES (..., 'Draft'); -- Admin must approve
```

### **Complexity:**
- **Development:** 2-3 days (combine Step 1 + Step 2)
- **Performance:** Fast (pre-filter reduces search space by 99%)
- **Accuracy:** Catches exact + typo duplicates, flags uncertain cases for admin

### **Recommendation:** 🎯 **Use for Phase 2** (best balance of accuracy + simplicity)

---

## Recommended Implementation Roadmap

### **Phase 1 (MVP):** Exact Matching Only
```sql
-- Check exact duplicates (name + date + city)
WHERE Name = @NewEventName
  AND CAST(StartDateTime AS DATE) = CAST(@NewEventStartDateTime AS DATE)
  AND City = @NewEventCity;
```
- **Effort:** 2 hours
- **Catches:** Exact duplicates only
- **UX:** "An event with this name, date, and city already exists. Did you mean: [Event Name]?"

### **Phase 2 (Post-MVP):** Hybrid (Pre-filter + Levenshtein)
```sql
-- Pre-filter by city + date, then fuzzy match
WHERE City = @NewEventCity
  AND ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3
HAVING dbo.LevenshteinDistance(LOWER(@NewEventName), LOWER(Name)) <= 5;
```
- **Effort:** 2-3 days
- **Catches:** Exact + typo duplicates
- **UX:** "Did you mean one of these existing events? [List of 3 similar events]"

### **Phase 3 (Future):** Semantic Similarity (If Needed)
```python
# Only if duplicate events become a major problem
# Use vector embeddings + cosine similarity
```
- **Effort:** 1-2 weeks
- **Catches:** Semantic duplicates ("CES" vs "Consumer Electronics Show")
- **Trigger:** Only implement if analytics show >10% duplicate event creation rate

---

## Complexity Summary

| Approach | Dev Time | Performance | Accuracy | Recommendation |
|----------|----------|-------------|----------|----------------|
| **Exact Match** | 2 hours | ⚡ Instant | ⭐ Low | ✅ MVP |
| **Levenshtein (Fuzzy)** | 2-3 days | ⚡ Fast (with pre-filter) | ⭐⭐⭐ Medium | ✅ Phase 2 |
| **Vector Embeddings** | 1-2 weeks | ⚠️ Slow (API calls) | ⭐⭐⭐⭐⭐ High | ⏰ Phase 3 (if needed) |
| **Hybrid** | 2-3 days | ⚡ Fast | ⭐⭐⭐⭐ High | 🎯 **Recommended** |

---

## Code Example: Levenshtein Distance (T-SQL)

```sql
CREATE FUNCTION dbo.LevenshteinDistance(
    @s1 NVARCHAR(4000),
    @s2 NVARCHAR(4000)
)
RETURNS INT
AS
BEGIN
    DECLARE @len1 INT = LEN(@s1);
    DECLARE @len2 INT = LEN(@s2);
    DECLARE @i INT, @j INT;
    DECLARE @cost INT;
    DECLARE @d TABLE (i INT, j INT, val INT);

    -- Initialize matrix
    SET @i = 0;
    WHILE @i <= @len1
    BEGIN
        INSERT INTO @d VALUES (@i, 0, @i);
        SET @i = @i + 1;
    END;

    SET @j = 0;
    WHILE @j <= @len2
    BEGIN
        INSERT INTO @d VALUES (0, @j, @j);
        SET @j = @j + 1;
    END;

    -- Fill matrix
    SET @i = 1;
    WHILE @i <= @len1
    BEGIN
        SET @j = 1;
        WHILE @j <= @len2
        BEGIN
            IF SUBSTRING(@s1, @i, 1) = SUBSTRING(@s2, @j, 1)
                SET @cost = 0;
            ELSE
                SET @cost = 1;

            INSERT INTO @d VALUES (
                @i, @j,
                (SELECT MIN(val) FROM (
                    SELECT (SELECT val FROM @d WHERE i = @i-1 AND j = @j) + 1 AS val
                    UNION SELECT (SELECT val FROM @d WHERE i = @i AND j = @j-1) + 1
                    UNION SELECT (SELECT val FROM @d WHERE i = @i-1 AND j = @j-1) + @cost
                ) AS mins)
            );
            SET @j = @j + 1;
        END;
        SET @i = @i + 1;
    END;

    RETURN (SELECT val FROM @d WHERE i = @len1 AND j = @len2);
END;
GO

-- Usage Example:
SELECT dbo.LevenshteinDistance('CeBIT Australia', 'CEBIT Australia'); -- Returns: 1
SELECT dbo.LevenshteinDistance('CES 2025', 'Consumer Electronics Show 2025'); -- Returns: 28
```

---

## Frontend UX Flow

### **When User Adds Event:**

1. **User fills out form:**
   - Event Name: "CeBIT Australia 2025"
   - Date: May 15, 2025
   - City: Sydney

2. **On "Save" click:**
   - Backend runs duplicate detection
   - Finds similar event: "CeBIT Australia 2025" (curated)

3. **Show modal:**
   ```
   ┌─────────────────────────────────────────────────────────┐
   │  ⚠️ Possible Duplicate Event Found                       │
   ├─────────────────────────────────────────────────────────┤
   │  We found an existing event that might be the same:     │
   │                                                          │
   │  ✅ CeBIT Australia 2025                                 │
   │     May 15-17, 2025 | ICC Sydney                        │
   │     Trade Show • 12,000 attendees                       │
   │     [Source: ICC Sydney Events]                         │
   │                                                          │
   │                         [Use This Event]  [Add Anyway]  │
   └─────────────────────────────────────────────────────────┘
   ```

4. **User chooses:**
   - "Use This Event" → Select existing event (no duplicate created)
   - "Add Anyway" → Create new event (user knows best)

---

## Conclusion

**For EventLeadPlatform MVP:**
- ✅ **Start with Exact Matching** (2 hours dev time)
- ✅ **Add Fuzzy Matching in Phase 2** (2-3 days dev time)
- ⏰ **Only consider ML/Vector approach if duplicate rate >10%**

**Complexity is manageable!** Levenshtein distance is well-understood and performant with proper pre-filtering.

---

*Dimitri - Data Domain Architect* 🔍

