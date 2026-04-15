# Form AI first-shot tuning — review completeness

Use before closing a **block** or archiving an experiment.

## Per iteration (within a block)

- [ ] **Single change**: Addendum or scoring/code change documents exactly one intentional delta
- [ ] **Hypothesis written before run**: Which indicator(s) should move and why
- [ ] **Expected recorded**: Direction (up/down) for numeric indicators
- [ ] **CLI / evidence**: Command line or API payload captured; `changelog.jsonl` row or pasted metrics
- [ ] **Actual filled**: L, G, C, coll, bnd, valid after run
- [ ] **Delta vs previous row**: Numeric or qualitative
- [ ] **Outcome vs expected**: Match / partial / surprise — if surprise, note rerun or variance

## End of block (every 5 iterations)

- [ ] **Block summary** section updated (aggregate + interpretation)
- [ ] **Indicator registry** updated if splits/additions agreed
- [ ] **Checkpoint log** entry: human reviewed with agent; next block hypotheses listed
- [ ] **Explicit stop**: No new runs until checkpoint approved

## Archival

- [ ] Final addendum files committed or linked
- [ ] `experiment_id` and `user_prompt` hash noted for reproduction
