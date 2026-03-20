# Story 6.2 Model Comparison

- Generated: 2026-02-27 14:50:52
- Prompt set size: 3
- Models compared: gpt-4o-mini, gpt-4.1-mini, gpt-5-mini, gpt-4.1, gpt-5, gpt-5-pro

## Leaderboard

| Model | First-pass validity | Converged <=3 retries | Fail rate | Avg attempts | Avg retries | P95 latency (ms) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini | 0.0% | 100.0% | 0.0% | 2.00 | 1.00 | 21199 |
| gpt-4.1-mini | 0.0% | 100.0% | 0.0% | 2.00 | 1.00 | 18141 |
| gpt-5-mini | 100.0% | 100.0% | 0.0% | 1.00 | 0.00 | 29968 |
| gpt-4.1 | 0.0% | 100.0% | 0.0% | 2.67 | 1.67 | 19981 |
| gpt-5 | 66.7% | 100.0% | 0.0% | 1.33 | 0.33 | 50937 |
| gpt-5-pro | 0.0% | 0.0% | 100.0% | 0.00 | 0.00 | 60613 |

## Ranked Recommendation

1. `gpt-5-mini` - convergence 100.0%, first-pass 100.0%, fail 0.0%, avg attempts 1.00
2. `gpt-5` - convergence 100.0%, first-pass 66.7%, fail 0.0%, avg attempts 1.33
3. `gpt-4o-mini` - convergence 100.0%, first-pass 0.0%, fail 0.0%, avg attempts 2.00
4. `gpt-4.1-mini` - convergence 100.0%, first-pass 0.0%, fail 0.0%, avg attempts 2.00
5. `gpt-4.1` - convergence 100.0%, first-pass 0.0%, fail 0.0%, avg attempts 2.67
6. `gpt-5-pro` - convergence 0.0%, first-pass 0.0%, fail 100.0%, avg attempts 0.00

## Per-Prompt Results

| Model | Prompt | Status | Attempts | Retries | First-pass valid | Terminal reason | Latency (ms) |
|---|---|---|---:|---:|---|---|---:|
| gpt-4o-mini | Build a contact form with full name, email, phone, and sub... | completed | 2 | 1 | no | validated-success | 16585 |
| gpt-4o-mini | Create an event registration form with attendee name, emai... | completed | 2 | 1 | no | validated-success | 21199 |
| gpt-4o-mini | Generate a lead capture form for webinar signup with first... | completed | 2 | 1 | no | validated-success | 19127 |
| gpt-4.1-mini | Build a contact form with full name, email, phone, and sub... | completed | 2 | 1 | no | validated-success | 9455 |
| gpt-4.1-mini | Create an event registration form with attendee name, emai... | completed | 2 | 1 | no | validated-success | 18141 |
| gpt-4.1-mini | Generate a lead capture form for webinar signup with first... | completed | 2 | 1 | no | validated-success | 13157 |
| gpt-5-mini | Build a contact form with full name, email, phone, and sub... | completed | 1 | 0 | yes | validated-success | 22553 |
| gpt-5-mini | Create an event registration form with attendee name, emai... | completed | 1 | 0 | yes | validated-success | 29968 |
| gpt-5-mini | Generate a lead capture form for webinar signup with first... | completed | 1 | 0 | yes | validated-success | 22981 |
| gpt-4.1 | Build a contact form with full name, email, phone, and sub... | completed | 3 | 2 | no | validated-success | 19981 |
| gpt-4.1 | Create an event registration form with attendee name, emai... | completed | 3 | 2 | no | validated-success | 15393 |
| gpt-4.1 | Generate a lead capture form for webinar signup with first... | completed | 2 | 1 | no | validated-success | 12394 |
| gpt-5 | Build a contact form with full name, email, phone, and sub... | completed | 1 | 0 | yes | validated-success | 43362 |
| gpt-5 | Create an event registration form with attendee name, emai... | completed | 2 | 1 | no | validated-success | 50937 |
| gpt-5 | Generate a lead capture form for webinar signup with first... | completed | 1 | 0 | yes | validated-success | 33311 |
| gpt-5-pro | Build a contact form with full name, email, phone, and sub... | failed | 0 | 0 | no | provider-error | 60579 |
| gpt-5-pro | Create an event registration form with attendee name, emai... | failed | 0 | 0 | no | provider-error | 60573 |
| gpt-5-pro | Generate a lead capture form for webinar signup with first... | failed | 0 | 0 | no | provider-error | 60613 |

- Total execution time: 8.8 minutes
