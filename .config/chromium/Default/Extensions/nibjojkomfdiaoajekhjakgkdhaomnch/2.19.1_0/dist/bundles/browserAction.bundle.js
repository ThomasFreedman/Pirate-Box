(()=>{"use strict";var e={85266:(e,t,n)=>{const s=n(93150),i=n(11227),a=i("ipfs-companion:context-menus");a.error=i("ipfs-companion:context-menus:error");const o={selection:"selectionText",image:"srcUrl",video:"srcUrl",audio:"srcUrl",link:"linkUrl",page:"pageUrl"};e.exports.findValueForContext=async function(e,t){if(e){if(t){return e[o[t]]}if(e.srcUrl)return e.srcUrl;if(e.linkUrl)return e.linkUrl;if(e.pageUrl)return e.pageUrl}return(await s.tabs.query({active:!0,currentWindow:!0}).then((e=>e[0]))).url};const r="contextMenu_importToIpfs",l="panelCopy_currentIpnsAddress",c="panelCopy_copyRawCid",p="panel_copyCurrentPublicGwUrl";e.exports.contextMenuCopyCidAddress="panelCopy_currentIpfsAddress",e.exports.contextMenuCopyCanonicalAddress=l,e.exports.contextMenuCopyRawCid=c,e.exports.contextMenuCopyAddressAtPublicGw=p,e.exports.contextMenuViewOnGateway="panel_contextMenuViewOnGateway",e.exports.contextMenuCopyPermalink="panel_copyCurrentPermalink";const d=new Set([c,l,r]),u=new Set,g=new Set;e.exports.createContextMenus=function(e,t,n,{onAddFromContext:i,onCopyCanonicalAddress:o,onCopyRawCid:l,onCopyAddressAtPublicGw:w}){try{const e=(e,t,n)=>{s.contextMenus.create({id:e,title:s.i18n.getMessage(e),documentUrlPatterns:["<all_urls>"],contexts:[t]})},t=(e,t,n,a)=>{const o=`${e}_${t}`;return u.add(o),s.contextMenus.create({id:o,parentId:e,title:s.i18n.getMessage(t),contexts:[n],documentUrlPatterns:["<all_urls>"],enabled:!1,onclick:e=>i(e,n,a)})},n=(e,t,n,i)=>{const a=`${e}_${t}`;return g.add(a),d.has(t)&&u.add(a),s.contextMenus.create({id:a,parentId:e,title:s.i18n.getMessage(t),contexts:[n],documentUrlPatterns:["*://*/ipfs/*","*://*/ipns/*","*://*.ipfs.dweb.link/*","*://*.ipns.dweb.link/*","*://*.ipfs.localhost/*","*://*.ipns.localhost/*"],onclick:e=>i(e,n)})},a=(s,i)=>{e(s,i),t(s,r,i,{wrapWithDirectory:!0,pin:!1}),n(s,p,i,w),n(s,c,i,l)};t(null,"contextMenu_importToIpfsSelection","selection",{pin:!1}),a("contextMenu_parentImage","image"),a("contextMenu_parentVideo","video"),a("contextMenu_parentAudio","audio"),a("contextMenu_parentLink","link"),a("contextMenu_parentPage","page")}catch(e){if(e.message.indexOf("createProperties.documentUrlPatterns of contextMenus.create is not supported yet")>-1)return a("context menus disabled - createProperties.documentUrlPatterns of contextMenus.create is not supported yet"),{update:()=>Promise.resolve()};if("browser.contextMenus is undefined"===e.message||void 0===s.contextMenus)return a("context menus disabled - browser.contextMenus is undefined"),{update:()=>Promise.resolve()};throw e}const b=new Set([...u].filter((e=>g.has(e))));let f=!1;return{async update(t){try{if(t){const e=await s.tabs.query({active:!0,currentWindow:!0}).then((e=>e[0]));e&&e.id===t&&(f=n.isIpfsPageActionsContext(e.url))}const i=e().peerCount>=0;for(const e of u)await s.contextMenus.update(e,{enabled:i});for(const e of g)await s.contextMenus.update(e,{enabled:f});for(const e of b)await s.contextMenus.update(e,{enabled:i&&f})}catch(e){a.error("Error updating context menus",e)}}}}},79524:(e,t,n)=>{const s=n(93150),i=n(16566),a=n(18488),o=n(34998),{sameGateway:r}=n(11014),{formatImportDirectory:l}=n(4026),{contextMenuViewOnGateway:c,contextMenuCopyAddressAtPublicGw:p,contextMenuCopyPermalink:d,contextMenuCopyRawCid:u,contextMenuCopyCanonicalAddress:g,contextMenuCopyCidAddress:w}=n(85266),b=s.i18n.getMessage("panelCopy_notReadyHint");function f({active:e,redirect:t,isRedirectContext:n,pubGwURLString:o,gwURLString:f,currentTab:v,currentFqdn:m,currentDnslinkFqdn:x,currentTabIntegrationsOptOut:h,currentTabContentPath:y=b,currentTabImmutablePath:C=b,currentTabCid:M=b,currentTabPublicUrl:$=b,currentTabPermalink:A=b,ipfsNodeType:k,isIpfsContext:T,isIpfsOnline:P,isApiAvailable:O,onToggleSiteIntegrations:I,onViewOnGateway:U,onCopy:_,importDir:S,onFilesCpImport:R}){const G=e&&P&&O&&M,V=e&&P&&O&&!k.startsWith("embedded"),z=y.startsWith("/ipns/");return i`
    <div class='fade-in pv1'>
  ${(()=>{if(n)return i`
  ${a({text:s.i18n.getMessage("panel_activeTabSiteIntegrationsToggle",m),title:s.i18n.getMessage("panel_activeTabSiteIntegrationsToggleTooltip",m),style:"truncate",disabled:!e,switchValue:e&&!h,onClick:I})}
      `})()}
  ${(()=>{if(T)return i`<div>
  ${(e=>{if(!e)return!1;const{url:t}=e;return!(t.startsWith("ip")||r(t,f)||r(t,o))})(v)?a({text:s.i18n.getMessage(c),onClick:()=>U(c)}):null}
  ${a({text:s.i18n.getMessage(p),title:s.i18n.getMessage("panel_copyCurrentPublicGwUrlTooltip"),helperText:$,onClick:()=>_(p)})}
  ${z?a({text:s.i18n.getMessage(d),title:s.i18n.getMessage("panel_copyCurrentPermalinkTooltip"),helperText:A,onClick:()=>_(d)}):""}
  ${z?a({text:s.i18n.getMessage(g),title:s.i18n.getMessage("panelCopy_currentIpnsAddressTooltip"),helperText:y,onClick:()=>_(g)}):""}
  ${a({text:s.i18n.getMessage(w),title:s.i18n.getMessage("panelCopy_currentIpfsAddressTooltip"),helperText:C,onClick:()=>_(w)})}
  ${a({text:s.i18n.getMessage(u),title:s.i18n.getMessage("panelCopy_copyRawCidTooltip"),helperText:M,disabled:!G,onClick:()=>_(u)})}
  ${a({text:s.i18n.getMessage("panel_importCurrentIpfsAddress"),title:s.i18n.getMessage("panel_importCurrentIpfsAddressTooltip"),helperText:l(S),disabled:!V,onClick:R})}
  </div>
    `})()}
    </div>
  `}e.exports.contextActions=f,e.exports.activeTabActions=function(e){if(e.isRedirectContext||e.isIpfsContext)return i`
      <div class="mb1">
      ${o("panel_activeTabSectionHeader")}
      <div class="fade-in pv0">
        ${f(e)}      </div>
      </div>
  `}},26842:(e,t,n)=>{const s=n(93150),i=n(16566);function a({label:e,labelLegend:t,value:n,check:a,itemClass:o="",valueClass:r=""}){const l=s.i18n.getMessage("panel_statusOffline");return e=e?s.i18n.getMessage(e):null,t=t?s.i18n.getMessage(t):e,i`
      <div class="flex mb1 ${a?"":"o-60"} ${o}" title="${t}">
        <span class="w-40 f7 ttu no-user-select">${e}</span>
        <span class="w-60 f7 tr monospace truncate force-select-all ${r}" title="${n=n||0===n?n:l}">${n}</span>
      </div>
    `}e.exports=function({ipfsApiUrl:e,gatewayAddress:t,gatewayVersion:n,swarmPeers:s,ipfsNodeType:o}){const r=e&&"embedded"===o?"js-ipfs":e;return i`
    <ul class="fade-in list mv0 pt2 ph3 white">
    ${a({label:"panel_statusSwarmPeers",labelLegend:"panel_statusSwarmPeersTitle",value:s,check:s})}
    ${a({label:"panel_statusGatewayAddress",labelLegend:"panel_statusGatewayAddressTitle",value:t,check:t})}
    ${a({label:"panel_statusApiAddress",labelLegend:"panel_statusApiAddressTitle",value:r,check:n})}
    </ul>
  `}},6670:(e,t,n)=>{const s=n(16566),i=n(4700),a=n(42106),o=n(99669),r=n(80834),l=n(64974),c=n(26842);e.exports=function(e){const{ipfsNodeType:t,active:n,onToggleActive:p,onOpenPrefs:d,onOpenReleaseNotes:u,isIpfsOnline:g,onOpenWelcomePage:w,newVersion:b}=e;return s`
    <div>
      <div class="pt3 pr3 pb2 pl3 no-user-select flex justify-between items-center">
        <div class="inline-flex items-center">
        <div
          onclick=${w}
          class="transition-all pointer ${n?"":"o-40"}"
          style="${n?"":"filter: blur( .15em )"}">
  ${i({size:54,path:"../../../icons",ipfsNodeType:t,isIpfsOnline:n&&g})}
        </div>
          <div class="flex flex-column ml2 white ${n?"":"o-40"}">
            <div>
              <h1 class="inter fw6 f2 ttu ma0 pa0">
                IPFS
              </h1>
            </div>
            <span class="${n?"":"o-0"}">${l(e)}</span>
          </div>
        </div>
        <div class="tr ma0 pb1">
          ${b?a({newVersion:b,active:n,title:"panel_headerNewVersionTitle",action:u}):null}
          ${o({active:n,title:"panel_headerActiveToggleTitle",action:p})}
          ${r({active:n,title:"panel_openPreferences",action:d})}
        </div>
      </div>
      <div class="pb1 ${n?"":"o-40"}">
        ${c(e)}
      </div>
    </div>
  `}},98888:(e,t,n)=>{const s=n(16566),i=n(93150);e.exports=function({svg:e,title:t,active:n,action:a,className:o}){return s`
    <button class="header-icon pa0 ma0 dib bn bg-transparent transition-all ${o} ${a?"pointer":null} ${n?"aqua":"gray"}"
      style="outline:none;"
      title="${i.i18n.getMessage(t)||t}"
      onclick=${a}>
      ${e}
    </button>
  `}},16950:(e,t,n)=>{n(39127);const s=n(72490),i=n(18091),a=n(29307),o=s();o.use(a),o.route("*",i),o.mount("#root")},64974:(e,t,n)=>{const s=n(93150),i=n(16566);e.exports=function({gatewayVersion:e}){return i`
  ${function({label:e,labelLegend:t,title:n,value:a,check:o,valueClass:r=""}){const l=s.i18n.getMessage("panel_statusOffline");return e=e?s.i18n.getMessage(e):null,t=t?s.i18n.getMessage(t):e,i`
      <div title="${t}" class="ma0 pa0" style="line-height: 0.25">
        <span class="f7 tr monospace force-select-all ${r}" title="${n}">${(a=a||0===a?a:l).substring(0,13)}</span>
      </div>
    `}({label:"panel_statusGatewayVersion",title:s.i18n.getMessage("panel_statusGatewayVersionTitle"),value:e,check:e})}
  `}},34998:(e,t,n)=>{const s=n(93150),i=n(16566);e.exports=function(e){return i`
    <div class="no-select w-100 outline-0--focus tl ph3 pt2 mt1 pb1 o-40 f6">
      ${s.i18n.getMessage(e)}
    </div>
  `}},18488:(e,t,n)=>{const s=n(16566),i=n(34451);e.exports=function({icon:e,text:t,helperText:n,title:a,disabled:o,style:r,onClick:l,switchValue:c}){let p="black button-reset db w-100 bg-white b--none outline-0--focus pt2 ph3 f6 tl";return p+=o?" o-40":" pointer bg-near-white--hover",r&&(p+=` ${r}`),o&&(a=""),s`

    <button class="${p}"
            onclick=${o?null:l}  title="${a||""}" ${o?"disabled":""}>
      <div class="flex flex-row items-center justify-between"><div class="truncate">${t}</div>${i({checked:c,disabled:o,style:"fr ml2"})}</div>
      <div class="f7 o-40 w-80 truncate mv1">${n}</div>
    </button>
  `}},80834:(e,t,n)=>{const s=n(16566),i=n(98888);e.exports=function({active:e,title:t,action:n,size:a="1.8rem"}){const o=s`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 86 86"
        class="fill-current-color"
        style="width:${a}; height:${a}">
        <path d="M74.05 50.23c-.07-3.58 1.86-5.85 5.11-7.1-.2-2-2.48-7.45-3.63-8.76-3.11 1.46-6.06 1.23-8.54-1.22s-2.72-5.46-1.26-8.64a29.24 29.24 0 0 0-8.8-3.63c-1.06 3.08-3.12 5-6.35 5.25-3.82.29-6.29-1.69-7.61-5.22a30.11 30.11 0 0 0-8.77 3.67c1.5 3.16 1.3 6.1-1.15 8.6s-5.45 2.76-8.64 1.29a29.33 29.33 0 0 0-3.58 8.79C24 44.43 25.94 46.62 26 50s-1.82 5.84-5.1 7.12a29.21 29.21 0 0 0 3.68 8.71c3.09-1.38 6-1.15 8.42 1.22s2.79 5.33 1.41 8.49a29.72 29.72 0 0 0 8.76 3.57 1.46 1.46 0 0 0 .11-.21 7.19 7.19 0 0 1 13.53-.16c.13.33.28.32.55.25a29.64 29.64 0 0 0 8-3.3 4 4 0 0 0 .37-.25c-1.27-2.86-1.15-5.57.88-7.94 2.44-2.84 5.5-3.26 8.91-1.8a29.23 29.23 0 0 0 3.65-8.7c-3.17-1.22-5.05-3.38-5.12-6.77zM50 59.54a8.57 8.57 0 1 1 8.59-8.31A8.58 8.58 0 0 1 50 59.54z"/>
      </svg>
    `;return i({svg:o,title:t,active:e,action:n})}},18091:(e,t,n)=>{const s=n(16566),i=n(6670),{activeTabActions:a}=n(79524),o=n(10603);e.exports=function(e,t){const n=Object.assign({onToggleActive:()=>t("toggleActive"),onOpenPrefs:()=>t("openPrefs"),onOpenReleaseNotes:()=>t("openReleaseNotes"),onOpenWelcomePage:()=>t("openWelcomePage")},e),r=Object.assign({onViewOnGateway:()=>t("viewOnGateway"),onToggleSiteIntegrations:()=>t("toggleSiteIntegrations"),onCopy:e=>t("copy",e),onFilesCpImport:()=>t("filesCpImport")},e),l=Object.assign({onQuickImport:()=>t("quickImport"),onOpenWebUi:()=>t("openWebUi","/"),onToggleGlobalRedirect:()=>t("toggleGlobalRedirect")},e);return s`
    <div class="sans-serif" style="text-rendering: optimizeLegibility;">
      <div class="ba bw1 b--white ipfs-gradient-0">
        ${i(n)}
        ${o(l)}
      </div>
      ${a(r)}
    </div>
  `}},99669:(e,t,n)=>{const s=n(16566),i=n(98888);e.exports=function({active:e,title:t,action:n,size:a="1.8rem"}){const o=s`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 86 86"
        class="fill-current-color mr1"
        style="width:${a}; height:${a}">
        <path d="M50 20.11A29.89 29.89 0 1 0 79.89 50 29.89 29.89 0 0 0 50 20.11zm-3.22 17a3.22 3.22 0 0 1 6.44 0v6.43a3.22 3.22 0 0 1-6.44 0zM50 66.08a16.14 16.14 0 0 1-11.41-27.49 3.28 3.28 0 0 1 1.76-.65 2.48 2.48 0 0 1 2.42 2.41 2.58 2.58 0 0 1-.77 1.77A10.81 10.81 0 0 0 38.59 50a11.25 11.25 0 0 0 22.5 0 10.93 10.93 0 0 0-3.21-7.88 3.37 3.37 0 0 1-.65-1.77 2.48 2.48 0 0 1 2.42-2.41 2.16 2.16 0 0 1 1.76.65A16.14 16.14 0 0 1 50 66.08z"/>
      </svg>
    `;return i({svg:o,title:t,active:e,action:n})}},29307:(e,t,n)=>{const s=n(93150),i=n(24981),{browserActionFilesCpImportCurrentTab:a}=n(4026),{ipfsContentPath:o}=n(11014),{welcomePage:r,optionsPage:l}=n(22134),{contextMenuViewOnGateway:c,contextMenuCopyAddressAtPublicGw:p,contextMenuCopyPermalink:d,contextMenuCopyRawCid:u,contextMenuCopyCanonicalAddress:g,contextMenuCopyCidAddress:w}=n(85266);e.exports=(e,t)=>{let n;Object.assign(e,{active:!0,redirect:!0,isIpfsContext:!1,isRedirectContext:!1,ipfsNodeType:"external",isIpfsOnline:!1,ipfsApiUrl:null,publicGatewayUrl:null,publicSubdomainGatewayUrl:null,gatewayAddress:null,swarmPeers:null,gatewayVersion:null,isApiAvailable:!1,currentTab:null,currentFqdn:null,currentDnslinkFqdn:null,enabledOn:[],disabledOn:[]}),t.on("DOMContentLoaded",(async()=>{t.emit("render"),n=s.runtime.connect({name:"browser-action-port"}),n.onMessage.addListener((async n=>{if(n.statusUpdate){const i=n.statusUpdate;console.log("In browser action, received message from background:",n),await async function(t){t?(Object.assign(e,t),e.active&&t.redirect&&"embedded"!==t.ipfsNodeType?e.gatewayAddress=t.gwURLString:e.gatewayAddress=t.pubGwURLString,e.isApiAvailable=e.active&&!!await s.runtime.getBackgroundPage()&&!s.extension.inIncognitoContext,e.swarmPeers=e.active&&-1!==t.peerCount?t.peerCount:null,e.isIpfsOnline=e.active&&t.peerCount>-1,e.gatewayVersion=e.active&&t.gatewayVersion?t.gatewayVersion:null,e.ipfsApiUrl=e.active?t.apiURLString:null):(e.ipfsNodeType="external",e.swarmPeers=null,e.isIpfsOnline=!1,e.gatewayVersion=null,e.isIpfsContext=!1,e.isRedirectContext=!1)}(i),t.emit("render")}})),setTimeout((()=>{document.body.style.height=window.innerHeight+1+"px",setTimeout((()=>document.body.style.removeProperty("height")),50)}),100)})),t.on("viewOnGateway",(async()=>{n.postMessage({event:c}),window.close()})),t.on("copy",(function(e){switch(e){case g:n.postMessage({event:g});break;case w:n.postMessage({event:w});break;case u:n.postMessage({event:u});break;case p:n.postMessage({event:p});break;case d:n.postMessage({event:d})}window.close()})),t.on("filesCpImport",(()=>{n.postMessage({event:a}),window.close()})),t.on("quickImport",(()=>{s.tabs.create({url:s.runtime.getURL("dist/popup/quick-import.html")}),window.close()})),t.on("openWelcomePage",(async()=>{try{await s.tabs.create({url:r}),window.close()}catch(e){console.error(`Unable Open WelcomePage (${r})`,e)}})),t.on("openWebUi",(async(t="/")=>{const n=`${e.webuiRootUrl}#${t}`;try{await s.tabs.create({url:n}),window.close()}catch(e){console.error(`Unable Open Web UI (${n})`,e)}})),t.on("openReleaseNotes",(async()=>{const{version:e}=s.runtime.getManifest(),t=2===e.match(/\./g).length;let n;try{t?(n=`https://github.com/ipfs-shipyard/ipfs-companion/releases/tag/v${e}`,await s.storage.local.set({dismissedUpdate:e})):n="https://github.com/ipfs-shipyard/ipfs-companion/issues/964",await s.tabs.create({url:n}),window.close()}catch(e){console.error(`Unable to open release notes (${n})`,e)}})),t.on("openPrefs",(()=>{s.runtime.openOptionsPage().then((()=>window.close())).catch((e=>{console.error("runtime.openOptionsPage() failed, opening options page in tab instead.",e),s.tabs.create({url:s.runtime.getURL(l)})}))})),t.on("toggleGlobalRedirect",(async()=>{const n=e.redirect;e.redirect=!n,e.gatewayAddress=e.redirect?e.gwURLString:e.pubGwURLString,t.emit("render");try{await s.storage.local.set({useCustomGateway:!n})}catch(s){console.error(`Unable to update redirect state due to ${s}`),e.redirect=n,t.emit("render")}})),t.on("toggleSiteIntegrations",(async()=>{const n=e.currentTabIntegrationsOptOut;e.currentTabIntegrationsOptOut=!n,t.emit("render");try{let{enabledOn:t,disabledOn:a,currentTab:r,currentDnslinkFqdn:l,currentFqdn:c}=e;const p=l||c;n?(a=a.filter((e=>e!==p)),t.push(p)):(t=t.filter((e=>e!==p)),a.push(p)),await s.storage.local.set({disabledOn:a,enabledOn:t});const d=o(r.url,{keepURIParams:!0});if(l&&i.ipnsPath(d)){const e=d.replace(/^.*\/ipns\//,"http://");await s.tabs.update(r.id,{url:e})}else await s.tabs.reload(r.id)}catch(e){console.error(`Unable to update integrations state due to ${e}`),t.emit("render")}})),t.on("toggleActive",(async()=>{const n=e.active;e.active=!n,e.active||(e.gatewayAddress=e.pubGwURLString,e.ipfsApiUrl=null,e.gatewayVersion=null,e.swarmPeers=null,e.isIpfsOnline=!1);try{await s.storage.local.set({active:e.active})}catch(t){console.error(`Unable to update global Active flag due to ${t}`),e.active=n}t.emit("render")}))}},12735:(e,t,n)=>{const s=n(16566);e.exports=function({iconD:e,iconSize:t,text:n,title:i,disabled:a,style:o,onClick:r}){let l="header-icon fade-in w-50 ba bw1 snow b--snow bg-transparent f7 ph1 pv0 br4 ma1 flex justify-center items-center truncate";return l+=a?" o-60":" pointer",o&&(l+=` ${o}`),a&&(i=""),s`

    <div class="${l}" onclick=${a?null:r}  title="${i||""}" ${a?"disabled":""}>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="mr1" width="${t}" height="${t}"><path fill="currentColor" d="${e}"/></svg>
      <div class="flex flex-row items-center justify-between"><div class="truncate">${n}</div></div>
    </div>
  `}},10603:(e,t,n)=>{const s=n(93150),i=n(16566),a=n(12735);e.exports=function({active:e,ipfsNodeType:t,isIpfsOnline:n,isApiAvailable:o,onQuickImport:r,onOpenWebUi:l}){const c=e&&n&&o,p=e&&n&&"embedded"!==t;return i`
    <div class="flex pb2 ph2 justify-between">
  ${a({text:s.i18n.getMessage("panel_quickImport"),title:s.i18n.getMessage("panel_quickImportTooltip"),disabled:!c,onClick:r,iconSize:20,iconD:"M71.13 28.87a29.88 29.88 0 100 42.26 29.86 29.86 0 000-42.26zm-18.39 37.6h-5.48V52.74H33.53v-5.48h13.73V33.53h5.48v13.73h13.73v5.48H52.74z"})}
  ${a({text:s.i18n.getMessage("panel_openWebui"),title:s.i18n.getMessage("panel_openWebuiTooltip"),disabled:!p,onClick:l,iconSize:18,iconD:"M69.69 20.57c-.51-.51-1.06-1-1.62-1.47l-.16-.1c-.56-.46-1.15-.9-1.76-1.32l-.5-.35c-.25-.17-.52-.32-.79-.48A28.27 28.27 0 0050 12.23h-.69a28.33 28.33 0 00-27.52 28.36c0 13.54 19.06 37.68 26 46a3.21 3.21 0 005 0c6.82-8.32 25.46-32.25 25.46-45.84a28.13 28.13 0 00-8.56-20.18zM51.07 49.51a9.12 9.12 0 119.13-9.12 9.12 9.12 0 01-9.13 9.12z"})}
    </div>
  `}},42106:(e,t,n)=>{const s=n(16566),i=n(98888);e.exports=function({newVersion:e,active:t,title:n,action:a,className:o,size:r="1.8rem"}){let l=s`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 86 86"
        class="fill-yellow-muted mr1"
        style="width:${r}; height:${r}">
        <path xmlns="http://www.w3.org/2000/svg" d="M71.13 28.87a29.88 29.88 0 100 42.26 29.86 29.86 0 000-42.26zm-18.39 37.6h-5.48V44.71h5.48zm0-26.53h-5.48v-5.49h5.48z"/>
      </svg>
    `;return e.match(/\./g).length>2&&(l=s`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 86 86"
          class="fill-red-muted mr1"
          style="width:${r}; height:${r}">
          <path d="M82.84 71.14L55.06 23a5.84 5.84 0 00-10.12 0L17.16 71.14a5.85 5.85 0 005.06 8.77h55.56a5.85 5.85 0 005.06-8.77zm-30.1-.66h-5.48V65h5.48zm0-10.26h-5.48V38.46h5.48z"/>
      </svg>
    `,n="Beta channel is deprecated, please switch to regular releases",o=`${o} blink`),i({svg:l,title:n,active:t,action:a,className:o})}},39127:(e,t,n)=>{n.r(t)}},t={};function n(s){if(t[s])return t[s].exports;var i=t[s]={exports:{}};return e[s].call(i.exports,i,i.exports,n),i.exports}n.m=e,n.x=e=>{},n.amdO={},n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),n.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={666:0},t=[[16950,297]],s=e=>{},i=(i,a)=>{for(var o,r,[l,c,p,d]=a,u=0,g=[];u<l.length;u++)r=l[u],n.o(e,r)&&e[r]&&g.push(e[r][0]),e[r]=0;for(o in c)n.o(c,o)&&(n.m[o]=c[o]);for(p&&p(n),i&&i(a);g.length;)g.shift()();return d&&t.push.apply(t,d),s()},a=self.webpackChunkipfs_companion=self.webpackChunkipfs_companion||[];function o(){for(var s,i=0;i<t.length;i++){for(var a=t[i],o=!0,r=1;r<a.length;r++){var l=a[r];0!==e[l]&&(o=!1)}o&&(t.splice(i--,1),s=n(n.s=a[0]))}return 0===t.length&&(n.x(),n.x=e=>{}),s}a.forEach(i.bind(null,0)),a.push=i.bind(null,a.push.bind(a));var r=n.x;n.x=()=>(n.x=r||(e=>{}),(s=o)())})();n.x()})();