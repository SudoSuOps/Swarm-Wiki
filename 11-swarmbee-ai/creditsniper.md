# CreditSniper

Litigation-grade credit dispute intelligence platform.

**Domain**: `https://creditsniper.xyz`
**Repo**: `~/Desktop/creditsniper-xyz/` (GitHub: `SudoSuOps/creditsniper-xyz`)
**Platform**: Cloudflare Pages + R2

## Architecture

```
creditsniper.xyz (Cloudflare Pages)
  ├── Landing page (index.html)
  ├── /api/contact -> Rocket.Chat webhook
  └── /api/download -> Stripe verify -> R2 zip delivery

R2 bucket: creditsniper-vault
  └── products/*.zip (5 tiers)

External:
  ├── Stripe (payment processing)
  ├── Rocket.Chat (chat.swarmandbee.com)
  └── SwarmRouter letter_sender skill (PostGrid physical mail)
```

## Product Catalog (5 Tiers)

| Product | Price | Contents | R2 File |
|---------|-------|----------|---------|
| Sample Pack | $0.99 | 5 platinum credit law QA pairs | Credit_Sample_Pack.zip |
| Dispute Letter Pack | $9.99 | Dispute letter templates + examples | Dispute_Letter_Pack.zip |
| Full Credit Vault | $49.99 | Complete credit dispute intelligence library | Full_Credit_Vault.zip |
| Pro Monthly | $29.99/mo | Recurring vault access | Full_Credit_Vault.zip |
| Enterprise Annual | $199.99/yr | Annual subscription | Full_Credit_Vault.zip |

## Focus Areas

- FCRA violations (§611, §623)
- FDCPA violations
- Charge-off disputes
- Bureau response analysis
- Section 623 direct disputes
- Section 611 reinvestigation demands
- CoVe-verified legal training data (235B model verification)

## Payment Flow

```
User clicks "Buy" -> Stripe Checkout
  -> Payment completes
  -> Redirect to /api/download?session_id=xxx&product=slug
  -> Function verifies Stripe session (payment_status="paid")
  -> Enforces product_slug from session metadata (prevents slug swapping)
  -> Streams zip from R2 creditsniper-vault
```

## Letters Integration (PostGrid)

The `letter_sender` skill in SwarmRouter generates and sends physical credit dispute letters via PostGrid API.

**Letter type**: `credit_dispute`
- Cites FCRA §623 or §611
- Identifies specific account
- Demands action (reinvestigation, deletion, correction)
- Professional one-page format
- Sends via PostGrid ($1.50/letter, standard or certified mail)

See [letter_sender skill](../07-skills/cre-skills.md) for full details.

## Status

Early access — invite only. Products available but not publicly promoted yet.

## Codebase

| File | Purpose |
|------|---------|
| `wrangler.toml` | Cloudflare Pages config, R2 binding |
| `index.html` | Landing page (34KB) |
| `functions/api/contact.js` | Contact form -> Rocket.Chat |
| `functions/api/download.js` | Stripe verify + R2 delivery |
| `privacy.html` | Privacy policy |
| `terms.html` | Terms of service |
