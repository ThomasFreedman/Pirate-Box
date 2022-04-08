(()=>{"use strict";var e={36043:(e,t,s)=>{s(58522);const l=s(93150),a=s(72490),n=s(89698),i=s(83487),o=a();o.use(n(l.i18n,l.runtime)),o.route("*",i(l.i18n)),o.mount("#root")},83487:(e,t,s)=>{const l=s(93150),a=s(16566),n=s(4700),{renderTranslatedLinks:i,renderTranslatedSpans:o}=s(78179),{brave:c}=s(82945),{optionsPage:r}=s(22134),p="#ffffff";const g=(e,t)=>a`
    <div class="mt4 mb2 flex flex-column justify-center items-center transition-all ${null===t&&"state-unknown"}">
      ${n({path:"../../../icons",size:128,isIpfsOnline:t})}
      <p class="montserrat mt3 mb0 f2">${e.getMessage("page_landingWelcome_logo_title")}</p>
    </div>
  `,u=(e,t,s)=>a`
    <div class="w-80 flex flex-column justify-center">
      <div class="mb3 flex flex-column justify-center items-center">
        ${a`
    <svg x="0px" y="0px" viewBox="0 0 100 100" width="${130}">
      <path fill="${"#57cbd0"}" d="M52.42 18.81A31.19 31.19 0 1083.6 50a31.22 31.22 0 00-31.18-31.19zm0 59.78A28.59 28.59 0 1181 50a28.62 28.62 0 01-28.58 28.59z"/>
      <path fill="${p}" d="M66.49 35.87a.75.75 0 00-1.06 0L46.6 54.7l-7.2-7.2a.75.75 0 00-1.06 0l-3.92 3.92a.75.75 0 000 1.06l11.65 11.65a.75.75 0 001.06 0l23.28-23.28a.74.74 0 000-1.06zM46.6 62.54L36 52l2.86-2.86 7.2 7.2a.75.75 0 001.06 0L66 37.46l2.86 2.86z"/>
    </svg>
  `}
        <p class="mt0 mb0 f3 tc">${o("page_landingWelcome_welcome_peers",[t],'class="aqua fw6"')}</p>
      </div>
      <div class="mt3 f5 flex justify-center items-center">
        <button class="pv3 ph4 mh2 b navy br2 bn bg-white hover-bg-white-90 pointer" onclick=${s("/")}>${e.getMessage("page_landingWelcome_welcome_statusButton_text")}</button>
        <button class="pv3 ph4 mh2 b navy br2 bn bg-white hover-bg-white-90 pointer" onclick=${s("/files")}>${e.getMessage("page_landingWelcome_welcome_filesButton_text")}</button>
        <button class="pv3 ph4 mh2 b navy br2 bn bg-white hover-bg-white-90 pointer" onclick=${s("/peers")}>${e.getMessage("page_landingWelcome_welcome_peersButton_text")}</button>
      </div>
    </div>
  `,m=(e,t)=>{const s="mv0 white f5 lh-copy",n="aqua hover-white",o=null===t,p=l.runtime.getURL(r);return a`
    <div class="w-80 mt0 flex flex-column transition-all ${o&&"state-unknown"}">
      <div class="mb4 flex flex-column justify-center items-center">
        ${a`
    <svg x="0px" y="0px" viewBox="0 0 100 100" width="${130}">
      <path fill="${"#f39021"}" d="M82.84 71.14L55.06 23a5.84 5.84 0 00-10.12 0L17.16 71.14a5.85 5.85 0 005.06 8.77h55.56a5.85 5.85 0 005.06-8.77zm-30.1-.66h-5.48V65h5.48zm0-10.26h-5.48V38.46h5.48z"/>
    </svg>
  `}
        <p class="mt0 mb0 f3 tc">${e.getMessage("page_landingWelcome_installSteps_notRunning_title")}</p>
      </div>
      ${c?a`
          <p class="mb2 aqua b f4 lh-title">${e.getMessage("page_landingWelcome_installSteps_brave_title")}</p>
          <p class="${s}">${i("page_landingWelcome_installSteps_brave_install",[p],`target="_blank" class="${n}"`)}</p>`:null}
      <p class="mb2 aqua b f4 lh-title">${e.getMessage("page_landingWelcome_installSteps_desktop_title")}</p>
      <p class="${s}">${i("page_landingWelcome_installSteps_desktop_install",["https://github.com/ipfs-shipyard/ipfs-desktop#ipfs-desktop"],`target="_blank" class="${n}"`)}</p>
      <p class="mb2 aqua b f4 lh-title">${e.getMessage("page_landingWelcome_installSteps_cli_title")}</p>
      <p class="${s}">${i("page_landingWelcome_installSteps_cli_install",["https://docs.ipfs.io/how-to/command-line-quick-start/"],`target="_blank" class="${n}"`)}</p>
    </div>
  `},d=e=>{const t="ttu tracked f6 fw4 teal mt0 mb3",s="mt0 mb4 lh-copy",l="link underline-under hover-aqua";return a`
    <div class="w-80 mt4 mb0 navy f5">

      <p class="${t}">${e.getMessage("page_landingWelcome_resources_title_new_ipfs")}</p>
      <ul class="${s}">
        <li>${i("page_landingWelcome_resources_new_ipfs_companion_features",["https://github.com/ipfs-shipyard/ipfs-companion#ipfs-companion-features"],`target="_blank" class="${l}"`)}</li>
        <li>${i("page_landingWelcome_resources_new_ipfs_concepts",["https://docs.ipfs.io/concepts/how-ipfs-works/"],`target="_blank" class="${l}"`)}</li>
        <li>${i("page_landingWelcome_resources_new_ipfs_docs",["https://docs.ipfs.io"],`target="_blank" class="${l}"`)}</li>
      </ul>

      <p class="${t}">${e.getMessage("page_landingWelcome_resources_title_build")}</p>
      <ul class="${s}">
        <li>${i("page_landingWelcome_resources_build_tutorials",["https://docs.ipfs.io/how-to/"],`target="_blank" class="${l}"`)}</li>
        <li>${i("page_landingWelcome_resources_build_examples",["https://awesome.ipfs.io"],`target="_blank" class="${l}"`)}</li>
      </ul>

      <p class="${t}">${e.getMessage("page_landingWelcome_resources_title_get_help")}</p>
      <ul class="${s}">
        <li>${i("page_landingWelcome_resources_get_help",["https://discuss.ipfs.io"],`target="_blank" class="${l}"`)}</li>
      </ul>

      <p class="${t}">${e.getMessage("page_landingWelcome_resources_title_community")}</p>
      <ul class="${s}">
        <li>${i("page_landingWelcome_resources_community_contribute",["https://docs.ipfs.io/community/contribute/ways-to-contribute/"],`target="_blank" class="${l}"`)}</li>
        <li>${i("page_landingWelcome_resources_community_translate",["https://www.transifex.com/ipfs/public/"],`target="_blank" class="${l}"`)}</li>
        <li>${i("page_landingWelcome_resources_community_resources",["https://docs.ipfs.io/community/"],`target="_blank" class="${l}"`)}</li>
    </ul>
    </div>
  `},_=e=>{const t="relative overflow-hidden br2 o-70 glow",s=180,l=()=>a`
    <div class="absolute absolute--fill bg-navy o-70"></div>
  `,n=()=>a`
    <svg class="aspect-ratio--object" x="0px" y="0px" viewBox="-90 -60 ${240} ${s}">
      <g fill="${p}">
        <polygon points="43,30 23,40 23,20" />
      </g>
    </svg>
  `;return a`
    <div class="w-80 flex flex-column flex-row-ns justify-between-ns aqua f5">
      <div class="flex flex-column mr1">
        <p class="ttu tracked f6 fw4 teal mt0 mb3">${e.getMessage("page_landingWelcome_videos_why_ipfs")}</p>
        <a class="${t}" style="height: ${s}px" href="https://www.youtube.com/watch?feature=player_embedded&v=zE_WSLbqqvo" target="_blank">
          <img width="${240}" height="${s}" src="https://ipfs.io/ipfs/QmS4Ae3WBzkaANSPD82Dsax8QuJQpS4TEfaC53FMPkdxMA" alt="${e.getMessage("page_landingWelcome_videos_why_ipfs")}" />
          ${l()}
          ${n()}
        </a>
      </div>

      <div class="flex flex-column">
        <p class="ttu tracked f6 fw4 teal mt0 mb3">${e.getMessage("page_landingWelcome_videos_how_ipfs_works")}</p>
        <a class="${t}" style="height: ${s}px" href="https://www.youtube.com/watch?feature=player_embedded&v=0IGzEYixJHk" target="_blank">
          <img width="${240}" height="${s}" src="https://ipfs.io/ipfs/QmP5uNwDjYZmoLxw8zJeeheSJEnBKYpFn4uuEQQWFYGKvM" alt="${e.getMessage("page_landingWelcome_videos_how_ipfs_works")}" />
          ${l()}
          ${n()}
        </a>
      </div>
    </div>
  `},f=e=>{const t="flex flex-column items-center navy link underline-under hover-aqua";return a`
    <div class="w-80 mv4 navy f6">
      <p class="ttu tracked f6 fw4 teal mt0 mb3">${e.getMessage("page_landingWelcome_projects_title")}</p>

      <div class="flex justify-between-ns">
        <a class="${t}" href="https://multiformats.io/" target="_blank">
          <img width="${80}" src="${"../../../images/multiformats.svg"}" alt="Multiformats Logo">
          <p>Multiformats</p>
        </a>

        <a class="${t}" href="https://ipld.io/" target="_blank">
          <img width="${80}" src="${"../../../images/ipld.svg"}" alt="IPLD Logo">
          <p>IPLD</p>
        </a>

        <a class="${t}" href="https://libp2p.io/" target="_blank">
        <img width="${80}" src="${"../../../images/libp2p.svg"}" alt="libp2p Logo">
          <p>libp2p</p>
        </a>
      </div>
    </div>
  `};e.exports=function(e){return function(t,s){const{isIpfsOnline:l,peerCount:n}=t;return document.title=e.getMessage("page_landingWelcome_title"),a`
      <div class="flex flex-column flex-row-l">
        <div id="left-col" class="min-vh-100 flex flex-column justify-center items-center bg-navy white">
          ${g(e,l)}
          ${l?u(e,n,(e=>()=>s("openWebUi",e))):m(e,l)}
        </div>

        <div id="right-col" class="min-vh-100 w-100 flex flex-column justify-around items-center">
          ${d(e)}
          ${_(e)}
          ${f(e)}
        </div>
      </div>
    `}}},89698:(e,t,s)=>{const l=s(93150);e.exports=function(e,t){return function(e,s){let a;e.isIpfsOnline=null,e.peerCount=null,e.webuiRootUrl=null,s.on("DOMContentLoaded",(async()=>{s.emit("render"),a=t.connect({name:"browser-action-port"}),a.onMessage.addListener((async t=>{if(t.statusUpdate){const l=t.statusUpdate.webuiRootUrl,a=t.statusUpdate.peerCount,n=a>-1;n===e.isIpfsOnline&&a===e.peerCount&&l===e.webuiRootUrl||(e.webuiRootUrl=l,e.isIpfsOnline=n,e.peerCount=a,s.emit("render"))}}))})),s.on("openWebUi",(async(t="/")=>{const s=`${e.webuiRootUrl}#${t}`;try{await l.tabs.create({url:s})}catch(e){console.error(`Unable Open Web UI (${s})`,e)}}))}}},78179:(e,t,s)=>{const l=s(93150);e.exports={renderTranslatedLinks:(e,t,s)=>{const a=/<\d+>(.+?)<\/\d+>/gm,n=/<(\d+)>/gm,i=l.i18n.getMessage(e);let o=i,c=a.exec(i);for(;null!==c;){let e=n.exec(c[0]);for(;null!==e;)o=o.replace(c[0],`<a href="${t[parseInt(e[1])]}" ${s}>${c[1]}</a>`),e=n.exec(i);c=a.exec(i)}const r=document.createElement("template");return r.innerHTML=o,r.content},renderTranslatedSpans:(e,t,s)=>{const a=/<\d+>(.+?)<\/\d+>/gm,n=/<(\d+)>/gm,i=l.i18n.getMessage(e,t);let o=i,c=a.exec(i);for(;null!==c;){let e=n.exec(c[0]);for(;null!==e;)o=o.replace(c[0],`<span ${s}>${c[1]}</span>`),e=n.exec(i);c=a.exec(i)}const r=document.createElement("template");return r.innerHTML=o,r.content}}},58522:(e,t,s)=>{s.r(t)}},t={};function s(l){if(t[l])return t[l].exports;var a=t[l]={exports:{}};return e[l].call(a.exports,a,a.exports,s),a.exports}s.m=e,s.x=e=>{},s.amdO={},s.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),s.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={516:0},t=[[36043,297]],l=e=>{},a=(a,n)=>{for(var i,o,[c,r,p,g]=n,u=0,m=[];u<c.length;u++)o=c[u],s.o(e,o)&&e[o]&&m.push(e[o][0]),e[o]=0;for(i in r)s.o(r,i)&&(s.m[i]=r[i]);for(p&&p(s),a&&a(n);m.length;)m.shift()();return g&&t.push.apply(t,g),l()},n=self.webpackChunkipfs_companion=self.webpackChunkipfs_companion||[];function i(){for(var l,a=0;a<t.length;a++){for(var n=t[a],i=!0,o=1;o<n.length;o++){var c=n[o];0!==e[c]&&(i=!1)}i&&(t.splice(a--,1),l=s(s.s=n[0]))}return 0===t.length&&(s.x(),s.x=e=>{}),l}n.forEach(a.bind(null,0)),n.push=a.bind(null,n.push.bind(n));var o=s.x;s.x=()=>(s.x=o||(e=>{}),(l=i)())})();s.x()})();