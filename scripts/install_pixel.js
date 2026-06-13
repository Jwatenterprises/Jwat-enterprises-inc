const fs = require('fs');
const path = require('path');

const pixelID = '7650989745631281169';
const pixelCode = `    <script>
    !function (w, d, t) {
      w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","trackPull","install","instance"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var o="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=o,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var a=d.createElement("script");a.type="text/javascript",a.async=!0,a.src=o+"?sdkid="+e+"&lib="+t;var r=d.getElementsByTagName("script")[0];r.parentNode.insertBefore(a,r)};
      ttq.load('${pixelID}');
      ttq.page();
    }(window, document, 'ttq');
    </script>
`;

function processDir(dir) {
    const items = fs.readdirSync(dir);
    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            processDir(fullPath);
        } else if (item.endsWith('.html')) {
            let content = fs.readFileSync(fullPath, 'utf8');
            if (!content.includes(pixelID)) {
                content = content.replace('</head>', pixelCode + '</head>');
                fs.writeFileSync(fullPath, content);
                console.log(`Installed Pixel in: ${fullPath}`);
            }
        }
    });
}

const baseDir = 'C:\\Users\\Milli\\Documents\\jwat-website-repo';
console.log(`Starting Pixel installation in ${baseDir}...`);
processDir(baseDir);
console.log('Done!');
