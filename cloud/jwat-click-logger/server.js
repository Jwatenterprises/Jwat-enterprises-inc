import express from 'express';
import { Firestore, FieldValue } from '@google-cloud/firestore';
import { fileURLToPath } from 'node:url';
import partnerLinks from './partner-links.json' with { type: 'json' };

const app = express();
const port = Number(process.env.PORT || 8080);
const collectionName = process.env.CLICK_COLLECTION || 'affiliate_clicks';
const disableFirestore = process.env.DISABLE_FIRESTORE === '1';
let firestore;

function getFirestore() {
  if (disableFirestore) return null;
  if (!firestore) firestore = new Firestore();
  return firestore;
}

function cleanToken(value, fallback = 'unknown') {
  if (!value || typeof value !== 'string') return fallback;
  const cleaned = value.toLowerCase().replace(/[^a-z0-9._-]/g, '-').slice(0, 80);
  return cleaned || fallback;
}

function cleanText(value, maxLength = 250) {
  if (!value || typeof value !== 'string') return '';
  return value.replace(/[\u0000-\u001f\u007f]/g, '').slice(0, maxLength);
}

function getClientIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (typeof forwarded === 'string' && forwarded.length > 0) {
    return forwarded.split(',')[0].trim();
  }
  return req.socket.remoteAddress || '';
}

export function buildClickEvent(req, partner) {
  return {
    partner,
    campaign: cleanToken(req.query.campaign, 'direct'),
    sourcePage: cleanText(req.query.source || req.query.page || 'unknown', 180),
    referrer: cleanText(req.get('referer'), 300),
    userAgent: cleanText(req.get('user-agent'), 300),
    ipPrefix: cleanText(getClientIp(req).split('.').slice(0, 3).join('.'), 40),
    createdAt: FieldValue.serverTimestamp()
  };
}

app.get('/', (req, res) => {
  res.status(200).json({
    service: 'jwat-click-logger',
    status: 'ok',
    partners: Object.keys(partnerLinks)
  });
});

app.get('/r/:partner', async (req, res) => {
  const partner = cleanToken(req.params.partner);
  const destination = partnerLinks[partner];

  if (!destination) {
    res.status(404).send('Unknown partner link.');
    return;
  }

  const clickEvent = buildClickEvent(req, partner);

  try {
    const db = getFirestore();
    if (db) {
      await db.collection(collectionName).add({
        ...clickEvent,
        partnerLabel: destination.label,
        category: destination.category
      });
    }
  } catch (error) {
    console.error('click_log_write_failed', {
      partner,
      error: error.message
    });
  }

  res.redirect(302, destination.url);
});

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  app.listen(port, () => {
    console.log(`jwat-click-logger listening on ${port}`);
  });
}

export { app, partnerLinks, cleanToken };
