// JWAT Enterprises Inc — Centralized Tracking
// GA4 + TikTok Pixel + Meta Pixel + Custom Event Tracking
// Installed across all pages via <script src="/scripts/tracking.js"></script>

(function() {
  'use strict';

  var GA4_ID = 'G-W8W4W8LPNC';
  var TIKTOK_PIXEL_ID = '7650989745631281169';
  var META_PIXEL_ID = '1358094426455242';

  // ── GA4 ──
  var gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
  document.head.appendChild(gaScript);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA4_ID, {
    send_page_view: true,
    cookie_flags: 'SameSite=None;Secure'
  });

  // ── TikTok Pixel ──
  !function(w, d, t) {
    w.TiktokAnalyticsObject = t;
    var ttq = w[t] = w[t] || [];
    ttq.methods = ["page","track","identify","instances","debug","on","off","once","ready","alias","group","trackPull","install","instance"];
    ttq.setAndDefer = function(t, e) { t[e] = function() { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
    for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
    ttq.instance = function(t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; };
    ttq.load = function(e, n) {
      var o = "https://analytics.tiktok.com/i18n/pixel/events.js";
      ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = o;
      ttq._t = ttq._t || {}; ttq._t[e] = +new Date;
      ttq._o = ttq._o || {}; ttq._o[e] = n || {};
      var a = d.createElement("script"); a.type = "text/javascript"; a.async = true;
      a.src = o + "?sdkid=" + e + "&lib=" + t;
      var r = d.getElementsByTagName("script")[0]; r.parentNode.insertBefore(a, r);
    };
    ttq.load(TIKTOK_PIXEL_ID);
    ttq.page();
  }(window, document, 'ttq');

  // ── Meta Pixel (activates when META_PIXEL_ID is set) ──
  if (META_PIXEL_ID) {
    !function(f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function() { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = true; n.version = '2.0';
      n.queue = [];
      t = b.createElement(e); t.async = true; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID);
    fbq('track', 'PageView');
  }

  // ── UTM Capture ──
  // Store UTM params in sessionStorage so they persist across page navigations
  var params = new URLSearchParams(window.location.search);
  var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  utmKeys.forEach(function(key) {
    var val = params.get(key);
    if (val) sessionStorage.setItem(key, val);
  });

  function getUtm() {
    var utm = {};
    utmKeys.forEach(function(key) {
      var val = sessionStorage.getItem(key);
      if (val) utm[key] = val;
    });
    return utm;
  }

  // ── Affiliate Link Detection ──
  var PARTNER_DOMAINS = {
    'mypartner.io': 'ROK Financial',
    'go.mypartner.io': 'ROK Financial',
    'nav.bfrb4.net': 'Nav',
    'nav.nkwcmr.net': 'Nav',
    'nav.com': 'Nav',
    'gohighlevel.com': 'GoHighLevel',
    'affiliate.gohighlevel.com': 'GoHighLevel',
    'upfirst.ai': 'Upfirst',
    'jotform.com': 'Tax Services'
  };

  function identifyPartner(href) {
    if (!href) return null;
    try {
      var url = new URL(href, window.location.origin);
      var host = url.hostname.replace('www.', '');
      for (var domain in PARTNER_DOMAINS) {
        if (host === domain || host.endsWith('.' + domain)) {
          return PARTNER_DOMAINS[domain];
        }
      }
    } catch (e) {}
    return null;
  }

  function getPageName() {
    var path = window.location.pathname;
    if (path === '/' || path === '/index.html') return 'homepage';
    return path.replace(/^\//, '').replace(/\.html$/, '').replace(/\//g, '_');
  }

  // ── Event Tracking Functions ──
  function trackEvent(eventName, params) {
    var utm = getUtm();
    var merged = Object.assign({}, params || {}, utm, { page_location: getPageName() });

    // GA4
    if (window.gtag) gtag('event', eventName, merged);

    // TikTok
    if (window.ttq) {
      if (eventName === 'affiliate_click') {
        ttq.track('ClickButton', { content_name: merged.partner || 'unknown' });
      }
    }

    // Meta
    if (window.fbq && META_PIXEL_ID) {
      if (eventName === 'affiliate_click') {
        fbq('trackCustom', 'AffiliateClick', { partner: merged.partner });
      }
    }
  }

  // ── Auto-attach Affiliate Click Tracking ──
  function attachAffiliateTracking() {
    var links = document.querySelectorAll('a[href]');
    links.forEach(function(link) {
      var partner = identifyPartner(link.href);
      if (partner) {
        link.addEventListener('click', function() {
          trackEvent('affiliate_click', {
            partner: partner,
            link_url: link.href,
            link_text: (link.textContent || '').trim().substring(0, 100)
          });
        });
        link.setAttribute('data-jwat-partner', partner);
      }
    });
  }

  // ── CTA Click Tracking ──
  function attachCTATracking() {
    var ctas = document.querySelectorAll('.nav-cta, .cta-button, [class*="cta"], .partner-btn, .hero-cta, button[type="submit"]');
    ctas.forEach(function(el) {
      el.addEventListener('click', function() {
        trackEvent('cta_click', {
          cta_text: (el.textContent || '').trim().substring(0, 100),
          cta_class: el.className
        });
      });
    });
  }

  // ── Cassidy Chatbot Tracking ──
  function attachCassidyTracking() {
    var bubble = document.getElementById('cassidy-bubble');
    if (bubble) {
      bubble.addEventListener('click', function() {
        trackEvent('cassidy_open', { action: 'chatbot_opened' });
      });
    }
  }

  // ── Scroll Depth Tracking ──
  function attachScrollTracking() {
    var milestones = [25, 50, 75, 90];
    var fired = {};
    window.addEventListener('scroll', function() {
      var scrollPct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
      milestones.forEach(function(m) {
        if (scrollPct >= m && !fired[m]) {
          fired[m] = true;
          trackEvent('scroll_depth', { depth_percent: m });
        }
      });
    }, { passive: true });
  }

  // ── Blog-Specific Tracking ──
  function attachBlogTracking() {
    if (window.location.pathname.indexOf('/blog/') === -1) return;
    var title = document.title.split(' — ')[0] || document.title;
    trackEvent('blog_view', { blog_title: title.substring(0, 150) });

    // Track time on blog (30s, 60s, 120s)
    var intervals = [30, 60, 120];
    intervals.forEach(function(sec) {
      setTimeout(function() {
        trackEvent('blog_engaged', { blog_title: title.substring(0, 150), seconds: sec });
      }, sec * 1000);
    });
  }

  // ── Initialize on DOM Ready ──
  function init() {
    attachAffiliateTracking();
    attachCTATracking();
    attachCassidyTracking();
    attachScrollTracking();
    attachBlogTracking();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose for manual use
  window.jwatTrack = trackEvent;

})();
