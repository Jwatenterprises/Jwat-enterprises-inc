# JWAT Affiliate Click Logger

Cost-safe Google Cloud prototype for tracking outbound JWAT partner CTA clicks before redirecting visitors to the approved affiliate destination.

## Purpose

JWAT's current business model is partner-led affiliate lead generation. This logger helps answer:

- Which pages drive partner clicks?
- Which partner lanes are getting attention?
- Which campaign/source labels are worth repeating?
- Are blog CTAs, email CTAs, or homepage CTAs performing better?

## Flow

```text
Visitor clicks JWAT CTA
  -> Cloud Run /r/:partner endpoint
  -> event written to Firestore
  -> visitor redirects to partner affiliate link
```

## Current Partner Slugs

- `rok-financial`
- `gohighlevel`
- `upfirst`
- `nav`
- `tax-services`

Example tracked link:

```text
https://SERVICE_URL/r/rok-financial?source=blog-working-capital-vs-line-of-credit&campaign=rok-nurture-june
```

## Cost Guardrails

Before any deploy:

1. Use one isolated project, suggested name: `jwat-free-tier-lab`.
2. Create budget alerts at `$1`, `$5`, `$10`, and `80%` of the intended monthly cap.
3. Deploy in `us-central1`.
4. Keep Cloud Run `min-instances=0`.
5. Keep Cloud Run `max-instances=1` for the pilot.
6. Keep CPU/memory small: `--cpu=1 --memory=256Mi`.
7. Do not attach this service to paid AI, VPC connectors, Pub/Sub, Cloud Scheduler, or BigQuery during the pilot.
8. Do not replace live JWAT links until the test redirect works and Firestore receives events.

Expected pilot cost: `$0/month` if traffic stays inside Free Tier. Treat operating risk as `$0-$5/month` with alerts.

## Local Run

Install dependencies:

```bash
npm install
```

Run without Firestore writes:

```bash
$env:DISABLE_FIRESTORE='1'
npm start
```

Open:

```text
http://localhost:8080/r/rok-financial?source=local-test&campaign=pilot
```

## Google Cloud Setup

Create project and enable APIs:

```bash
gcloud projects create jwat-free-tier-lab
gcloud config set project jwat-free-tier-lab
gcloud services enable run.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

Create Firestore database:

```bash
gcloud firestore databases create --location=nam5
```

Deploy:

```bash
gcloud run deploy jwat-click-logger `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --min-instances 0 `
  --max-instances 1 `
  --cpu 1 `
  --memory 256Mi `
  --set-env-vars CLICK_COLLECTION=affiliate_clicks
```

## Test After Deploy

Replace `SERVICE_URL` with the Cloud Run URL:

```text
SERVICE_URL/r/rok-financial?source=deploy-test&campaign=pilot
SERVICE_URL/r/gohighlevel?source=deploy-test&campaign=pilot
SERVICE_URL/r/upfirst?source=deploy-test&campaign=pilot
```

Verify:

- Browser redirects to the partner page.
- Firestore collection `affiliate_clicks` receives one document per click.
- No unknown partner slug redirects.
- Cloud Run metrics show low request count and no errors.

## Live JWAT Link Replacement Pattern

Only after the deployed test passes, replace direct partner links with tracked links.

Example:

```html
<a href="https://SERVICE_URL/r/rok-financial?source=blog-working-capital-vs-line-of-credit&campaign=rok-funding" target="_blank" rel="sponsored noopener">Explore Funding</a>
```

Keep `rel="sponsored noopener"` on affiliate links.

## Reporting

Start with Firestore console review. Add BigQuery only after JWAT has enough click volume to justify reporting.

Useful fields stored:

- `partner`
- `partnerLabel`
- `category`
- `campaign`
- `sourcePage`
- `referrer`
- `userAgent`
- `ipPrefix`
- `createdAt`

## Approval Gate

Do not deploy, create Google Cloud resources, or change live JWAT links until Wayne approves the cloud setup step.
