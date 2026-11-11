const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.cwd()+'/portafolio.html');
await p.pdf({path:'portafolio.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await b.close();})();
