# Letter Sender Skill

AI-generated physical mail via PostGrid API. Generates professional letters and optionally sends them as real mail.

**File**: `swarmrouter/worker/src/skills/letter_sender.js`

## 8 Letter Types

| Type | Purpose | Key Content |
|------|---------|-------------|
| `broker_outreach` | Introducing capital markets services | Reference specific property, lead with value |
| `maturity_alert` | Loan maturity + rate shock warnings | Specific numbers (rate shock, equity gap) |
| `rate_update` | Market rate intelligence | Current rates, trend analysis |
| `offer_letter` | LOI / expression of interest | Terms, price, conditions |
| `credit_dispute` | FCRA/FDCPA dispute letters (CreditSniper) | Cite §623 or §611, identify account, demand action |
| `owner_inquiry` | Property information requests | Specific property, purpose of inquiry |
| `1031_notification` | Exchange deadline communications | Timeline, replacement property |
| `follow_up` | Previous conversation follow-ups | Reference prior discussion, next steps |

## Two Modes

| Mode | Behavior |
|------|----------|
| `draft` | AI generates letter, returns for review (no PostGrid call) |
| `send` | AI generates + sends via PostGrid (real physical mail) |

## PostGrid Integration

**API**: `https://api.postgrid.com/print-mail/v1/letters`
**Auth**: `x-api-key` header
**Cost**: ~$1.50/letter (standard mail)

**Options**:
- Color: true/false
- Double-sided: true/false
- Extra service: standard / certified / registered

## Output Schema

```json
{
  "skill": "letter_sender",
  "mode": "draft|send",
  "letter_type": "broker_outreach|maturity_alert|...",
  "sender": {
    "name": "...", "company": "...",
    "address_line1": "...", "city": "...", "state": "...", "zip": "..."
  },
  "recipient": { "..." },
  "letter": {
    "subject_line": "...",
    "date": "March 9, 2026",
    "salutation": "Dear ...",
    "body_text": "...",
    "closing": "Sincerely,",
    "word_count": 250
  },
  "html_content": "<div>...</div>",
  "postgrid_options": {
    "color": false,
    "double_sided": false,
    "extra_service": "standard"
  },
  "campaign": {
    "name": "...",
    "batch_size": 1,
    "estimated_cost_per_letter": 1.50
  }
}
```

## Example

```
User: "Send a maturity alert to borrower at 1200 Main St, Dallas TX 75201.
       $15M CMBS loan at 3.2% matures in 6 months."

AI generates:
  - 3-5 paragraphs with specific numbers (rate shock, equity gap)
  - HTML formatted for PostGrid rendering
  - Sender/recipient addresses parsed
  - PostGrid options (standard mail)

sendViaPostGrid() returns:
  - postgrid_id, status, tracking URL, expected delivery date
```

## Credit Dispute Example

```
User: "Draft a Section 623 dispute letter for a wrongly reported
       charge-off on account #4532-XXXX-1234 with Capital One."

AI generates:
  - Cites FCRA §623 direct furnisher dispute
  - Identifies account, dates, amounts
  - Demands investigation within 30 days
  - Professional one-page format
```
