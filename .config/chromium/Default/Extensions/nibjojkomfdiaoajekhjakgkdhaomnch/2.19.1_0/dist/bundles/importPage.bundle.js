(()=>{"use strict";var e={20267:(e,t,o)=>{o(4141);const r=o(93150),i=o(72490),n=o(16566),a=o(4700),s=o(29930),{formatImportDirectory:p}=o(4026),l=o(31303),c=o(75519),d=o(56755);document.title=r.i18n.getMessage("quickImport_page_title");const u=i();async function b(e,t,o){console.log("Processing files",o);const{ipfsCompanion:i}=await r.runtime.getBackgroundPage();try{if(console.log("importing files",o),!o.length)throw new Error("found no valid sources, try selecting a local file instead");const{copyImportResultsToFiles:n,copyShareLink:a,preloadFilesAtPublicGateway:c,openFilesAtGateway:u,openFilesAtWebUI:b}=i.ipfsImportHandler,m=await r.tabs.getCurrent(),g=p(e.importDir),f="external"===i.state.ipfsNodeType,h=[];let y=0;for(const e of o)h.push({path:e.name,content:f?e:e.stream()}),y+=e.size;const v=d(y,{round:2});e.progress=`Importing ${v}... (keep this page open)`,t.emit("render");const I={progress:o=>{const r=(o/y*100).toFixed(0);e.progress=`Importing... (${r}% of ${v})`,t.emit("render")},wrapWithDirectory:!0,pin:!1};let x;x=f?await s.init(r,i.state):i.ipfs;const k=await l(x.addAll(h,I));await n(k,g),e.progress="Completed",t.emit("render"),console.log(`Successfully imported ${o.length} files`),a(k),c(k),!e.openViaWebUI||e.ipfsNodeType.startsWith("embedded")?await u(g):await b(g),await r.tabs.remove(m.id)}catch(o){console.error("Failed to import files to IPFS",o),e.message="Unable to import to IPFS:",e.progress=`${o}`,t.emit("render"),i.notify("notify_importErrorTitle","notify_inlineErrorMsg",`${o.message}`)}}u.use((function(e,t){let o;e.message="",e.peerCount="",e.ipfsNodeType="external",e.expandOptions=!1,e.openViaWebUI=!0,e.userChangedOpenViaWebUI=!1,e.importDir="",e.userChangedImportDir=!1,t.on("DOMContentLoaded",(async()=>{o=r.runtime.connect({name:"browser-action-port"}),o.onMessage.addListener((async o=>{o.statusUpdate&&(console.log("In browser action, received message from background:",o),function({ipfsNodeType:t,peerCount:o,importDir:r,openViaWebUI:i}){e.ipfsNodeType=t,e.peerCount=o,e.userChangedImportDir||(e.importDir=r),e.userChangedOpenViaWebUI||(e.openViaWebUI=i)}(o.statusUpdate),t.emit("render"))}))})),t.on("fileInputChange",(o=>b(e,t,o.target.files))),c(document.body,(o=>b(e,t,o)))})),u.route("*",(function(e,t){const{peerCount:o}=e;return n`
    <div class="montserrat pt5" style="background: linear-gradient(to top, #041727 0%,#043b55 100%); height:100%;">
      <div class="mw8 center pa3 white">
        <header class="flex items-center no-user-select">
  ${a({size:80,path:"../../icons",heartbeat:!1})}
          <div class="pl3">
            <h1 class="f2 fw5 ma0">
              ${r.i18n.getMessage("quickImport_head_peers")}
            </h1>
            <p class="f3 fw2 lh-copy ma0 light-gray">
              ${r.i18n.getMessage("quickImport_subhead_peers",[o])}
            </p>
          </div>
        </header>
        <label for="quickImportInput" class='db relative mt5 hover-inner-shadow pointer' style="border:solid 2px #6ACAD1">
          <input class="db pointer w-100 h-100 top-0 o-0" type="file" id="quickImportInput" multiple onchange=${e=>t("fileInputChange",e)} />
          <div class='dt dim' style='padding-left: 100px; height: 300px'>
            <div class='dtc v-mid'>
              <span class="f3 dim br1 ph4 pv3 dib navy" style="background: #6ACAD1">
                ${r.i18n.getMessage("quickImport_pick_file_button")}
              </span>
              <span class='f3'>
                <emph class='underline pl3 pr2 moon-gray'>
                  ${r.i18n.getMessage("quickImport_or")}
                </emph>
                ${r.i18n.getMessage("quickImport_drop_it_here")}
              </span>
              <p class='f4 db'>${e.message}<span class='code db absolute fr pv2'>${e.progress}</span></p>
            </div>
          </div>
        </label>
        ${function(e,t){const o=o=>{e.expandOptions=!0,t("render")},i=t=>{e.userChangedImportDir=!0,e.importDir=t.target.value},a=t=>{e.userChangedOpenViaWebUI=!0,e.openViaWebUI=t.target.checked},s="embedded"!==e.ipfsNodeType;if(e.expandOptions)return n`
      <div id='quickImportOptions' class='sans-serif mt3 f6 lh-copy light-gray no-user-select'>
        ${s?n`<label for='openViaWebUI' class='flex items-center db relative mt1 pointer'>
          <input id='openViaWebUI' type='checkbox' onchange=${a} checked=${e.openViaWebUI} />
          <span class='mark db flex items-center relative mr2 br2'></span>
          ${r.i18n.getMessage("quickImport_options_openViaWebUI")}
        </label>`:null}
        <label for='importDir' class='flex items-center db relative mt1 pointer'>
          ${r.i18n.getMessage("quickImport_options_importDir")}
          <span class='mark db flex items-center relative mr2 br2'></span>
          <input id='importDir' class='w-40 bg-transparent aqua monospace br1 ba b--aqua pa2' type='text' oninput=${i} value=${e.importDir} />
        </label>
      </div>
    `;return n`
    <button class='mt3 f6 lh-copy link bn bg-transparent moon-gray dib pa0 pointer' style='color: #6ACAD1' onclick=${o}>
      ${r.i18n.getMessage("quickImport_options_show")} »
    </button>
  `}(e,t)}
      </div>
    </div>
  `})),u.mount("#root")},75519:e=>{function t(e,t){t.stopPropagation(),t.preventDefault(),e(Array.prototype.slice.call(t.dataTransfer.files))}function o(e){return e.stopPropagation(),e.preventDefault(),!1}e.exports=function(e,r){e.addEventListener("dragenter",o,!1),e.addEventListener("dragover",o,!1),e.addEventListener("drop",t.bind(void 0,r),!1)}},56755:e=>{!function(t){var o=/^(b|B)$/,r={iec:{bits:["b","Kib","Mib","Gib","Tib","Pib","Eib","Zib","Yib"],bytes:["B","KiB","MiB","GiB","TiB","PiB","EiB","ZiB","YiB"]},jedec:{bits:["b","Kb","Mb","Gb","Tb","Pb","Eb","Zb","Yb"],bytes:["B","KB","MB","GB","TB","PB","EB","ZB","YB"]}},i={iec:["","kibi","mebi","gibi","tebi","pebi","exbi","zebi","yobi"],jedec:["","kilo","mega","giga","tera","peta","exa","zetta","yotta"]};function n(e){var t,n,a,s,p,l,c,d,u,b,m,g,f,h,y,v=1<arguments.length&&void 0!==arguments[1]?arguments[1]:{},I=[],x=0,k=void 0,w=void 0;if(isNaN(e))throw new TypeError("Invalid number");return n=!0===v.bits,m=!0===v.unix,t=v.base||2,b=void 0!==v.round?v.round:m?1:2,l=void 0!==v.locale?v.locale:"",c=v.localeOptions||{},g=void 0!==v.separator?v.separator:"",f=void 0!==v.spacer?v.spacer:m?"":" ",y=v.symbols||{},h=2===t&&v.standard||"jedec",u=v.output||"string",s=!0===v.fullform,p=v.fullforms instanceof Array?v.fullforms:[],k=void 0!==v.exponent?v.exponent:-1,a=2<t?1e3:1024,(d=(w=Number(e))<0)&&(w=-w),(-1===k||isNaN(k))&&(k=Math.floor(Math.log(w)/Math.log(a)))<0&&(k=0),8<k&&(k=8),"exponent"===u?k:(0===w?(I[0]=0,I[1]=m?"":r[h][n?"bits":"bytes"][k]):(x=w/(2===t?Math.pow(2,10*k):Math.pow(1e3,k)),n&&a<=(x*=8)&&k<8&&(x/=a,k++),I[0]=Number(x.toFixed(0<k?b:0)),I[0]===a&&k<8&&void 0===v.exponent&&(I[0]=1,k++),I[1]=10===t&&1===k?n?"kb":"kB":r[h][n?"bits":"bytes"][k],m&&(I[1]="jedec"===h?I[1].charAt(0):0<k?I[1].replace(/B$/,""):I[1],o.test(I[1])&&(I[0]=Math.floor(I[0]),I[1]=""))),d&&(I[0]=-I[0]),I[1]=y[I[1]]||I[1],!0===l?I[0]=I[0].toLocaleString():0<l.length?I[0]=I[0].toLocaleString(l,c):0<g.length&&(I[0]=I[0].toString().replace(".",g)),"array"===u?I:(s&&(I[1]=p[k]?p[k]:i[h][k]+(n?"bit":"byte")+(1===I[0]?"":"s")),"object"===u?{value:I[0],symbol:I[1],exponent:k}:I.join(f)))}n.partial=function(e){return function(t){return n(t,e)}},e.exports=n}(window)},31303:e=>{e.exports=async e=>{const t=[];for await(const o of e)t.push(o);return t}},4141:(e,t,o)=>{o.r(t)}},t={};function o(r){if(t[r])return t[r].exports;var i=t[r]={exports:{}};return e[r].call(i.exports,i,i.exports,o),i.exports}o.m=e,o.x=e=>{},o.amdO={},o.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),o.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={743:0},t=[[20267,297]],r=e=>{},i=(i,n)=>{for(var a,s,[p,l,c,d]=n,u=0,b=[];u<p.length;u++)s=p[u],o.o(e,s)&&e[s]&&b.push(e[s][0]),e[s]=0;for(a in l)o.o(l,a)&&(o.m[a]=l[a]);for(c&&c(o),i&&i(n);b.length;)b.shift()();return d&&t.push.apply(t,d),r()},n=self.webpackChunkipfs_companion=self.webpackChunkipfs_companion||[];function a(){for(var r,i=0;i<t.length;i++){for(var n=t[i],a=!0,s=1;s<n.length;s++){var p=n[s];0!==e[p]&&(a=!1)}a&&(t.splice(i--,1),r=o(o.s=n[0]))}return 0===t.length&&(o.x(),o.x=e=>{}),r}n.forEach(i.bind(null,0)),n.push=i.bind(null,n.push.bind(n));var s=o.x;o.x=()=>(o.x=s||(e=>{}),(r=a)())})();o.x()})();