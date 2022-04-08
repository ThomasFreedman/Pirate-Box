(()=>{"use strict";var e={75570:(e,t,s)=>{const{brave:i}=s(82945);e.exports.createRuntimeChecks=async function(e){const{name:t,version:s}=await function(e){return e&&e.runtime&&e.runtime.getBrowserInfo?e.runtime.getBrowserInfo():Promise.resolve({})}(e),n=t&&(t.includes("Firefox")||t.includes("Fennec")),o=!!(e&&e.protocol&&e.protocol.registerStringProtocol),a=await function(e){return e&&e.runtime&&e.runtime.getPlatformInfo?e.runtime.getPlatformInfo():Promise.resolve()}(e),l=!!a&&"android"===a.os;return Object.freeze({browser:e,brave:i,isFirefox:n,isAndroid:l,requiresXHRCORSfix:!!(n&&s&&s.startsWith("68")),hasNativeProtocolHandler:o})}},59390:(e,t,s)=>{const i=s(93150),n=s(16566),{guiURLString:o}=s(1906),{braveNodeType:a}=s(82945),l=s(34451);e.exports=function({ipfsNodeType:e,ipfsApiUrl:t,ipfsApiPollMs:s,automaticMode:d,onOptionChange:r}){const p=r("ipfsApiUrl",(e=>o(e,{useLocalhostName:!1}))),c=r("ipfsApiPollMs"),g=r("automaticMode"),f="external"===e,b=e===a?"brave":"";return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_api")}</h2>
        <div class="flex-row-ns pb0-ns">
          <label for="ipfsApiUrl">
            <dl>
              <dt>${i.i18n.getMessage("option_ipfsApiUrl_title")}</dt>
              <dd>${i.i18n.getMessage("option_ipfsApiUrl_description")}</dd>
            </dl>
          </label>
          <input
            class="bg-white navy self-center-ns ${b}"
            id="ipfsApiUrl"
            type="url"
            inputmode="url"
            required
            pattern="^https?://[^/]+/?$"
            spellcheck="false"
            title="${i.i18n.getMessage(f?"option_hint_url":"option_hint_readonly")}"
            onchange=${p}
            ${f?"":"disabled"}
            value=${t} />
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="ipfsApiPollMs">
            <dl>
              <dt>${i.i18n.getMessage("option_ipfsApiPollMs_title")}</dt>
              <dd>${i.i18n.getMessage("option_ipfsApiPollMs_description")}</dd>
            </dl>
          </label>
          <input
            class="bg-white navy self-center-ns"
            id="ipfsApiPollMs"
            type="number"
            inputmode="numeric"
            min="1000"
            max="60000"
            step="1000"
            required
            onchange=${c}
            value=${s} />
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="automaticMode">
            <dl>
              <dt>${i.i18n.getMessage("option_automaticMode_title")}</dt>
              <dd>${i.i18n.getMessage("option_automaticMode_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${l({id:"automaticMode",checked:d,onchange:g})}</div>
        </div>
      </fieldset>
    </form>
  `}},99068:(e,t,s)=>{const i=s(93150),n=s(16566),o=s(34451);e.exports=function({dnslinkPolicy:e,dnslinkDataPreload:t,dnslinkRedirect:s,onOptionChange:a}){const l=a("dnslinkPolicy"),d=a("dnslinkRedirect"),r=a("dnslinkDataPreload");return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_dnslink")}</h2>
        <div class="flex-row-ns pb0-ns">
          <label for="dnslinkPolicy">
            <dl>
              <dt>${i.i18n.getMessage("option_dnslinkPolicy_title")}</dt>
              <dd>
                ${i.i18n.getMessage("option_dnslinkPolicy_description")}
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/dnslink-companion/" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <select id="dnslinkPolicy" name='dnslinkPolicy' class="self-center-ns bg-white navy" onchange=${l}>
            <option
              value='false'
              selected=${"false"===String(e)}>
              ${i.i18n.getMessage("option_dnslinkPolicy_disabled")}
            </option>
            <option
              value='best-effort'
              selected=${"best-effort"===e}>
              ${i.i18n.getMessage("option_dnslinkPolicy_bestEffort")}
            </option>
            <option
              value='enabled'
              selected=${"enabled"===e}>
              ${i.i18n.getMessage("option_dnslinkPolicy_enabled")}
            </option>
          </select>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="dnslinkDataPreload">
            <dl>
              <dt>${i.i18n.getMessage("option_dnslinkDataPreload_title")}</dt>
              <dd>${i.i18n.getMessage("option_dnslinkDataPreload_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"dnslinkDataPreload",checked:t,disabled:s,onchange:r})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="dnslinkRedirect">
            <dl>
              <dt>${i.i18n.getMessage("option_dnslinkRedirect_title")}</dt>
              <dd>
                ${i.i18n.getMessage("option_dnslinkRedirect_description")}
                ${s?n`<p class="red i">${i.i18n.getMessage("option_dnslinkRedirect_warning")}</p>`:null}
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/address-ipfs-on-web/#subdomain-gateway" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"dnslinkRedirect",checked:s,onchange:d})}</div>
        </div>
      </fieldset>
    </form>
  `}},8082:(e,t,s)=>{const i=s(93150),n=s(16566),o=s(34451);e.exports=function({useLatestWebUI:e,displayNotifications:t,displayReleaseNotes:s,catchUnhandledProtocols:a,linkify:l,recoverFailedHttpRequests:d,detectIpfsPathHeader:r,ipfsProxy:p,logNamespaces:c,onOptionChange:g}){const f=g("displayNotifications"),b=g("displayReleaseNotes"),u=g("useLatestWebUI"),h=g("catchUnhandledProtocols"),_=g("linkify"),m=g("recoverFailedHttpRequests"),v=g("detectIpfsPathHeader"),$=g("ipfsProxy");return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_experiments")}</h2>
        <div class="mb2">${i.i18n.getMessage("option_experiments_warning")}</div>
        <div class="flex-row-ns pb0-ns">
          <label for="useLatestWebUI">
            <dl>
              <dt>${i.i18n.getMessage("option_useLatestWebUI_title")}</dt>
              <dd>${i.i18n.getMessage("option_useLatestWebUI_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"useLatestWebUI",checked:e,onchange:u})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="displayNotifications">
            <dl>
              <dt>${i.i18n.getMessage("option_displayNotifications_title")}</dt>
              <dd>${i.i18n.getMessage("option_displayNotifications_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"displayNotifications",checked:t,onchange:f})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="displayReleaseNotes">
            <dl>
              <dt>${i.i18n.getMessage("option_displayReleaseNotes_title")}</dt>
              <dd>${i.i18n.getMessage("option_displayReleaseNotes_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"displayReleaseNotes",checked:s,onchange:b})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="catchUnhandledProtocols">
            <dl>
              <dt>${i.i18n.getMessage("option_catchUnhandledProtocols_title")}</dt>
              <dd>${i.i18n.getMessage("option_catchUnhandledProtocols_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"catchUnhandledProtocols",checked:a,onchange:h})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="recoverFailedHttpRequests">
            <dl>
              <dt>${i.i18n.getMessage("option_recoverFailedHttpRequests_title")}</dt>
              <dd>${i.i18n.getMessage("option_recoverFailedHttpRequests_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"recoverFailedHttpRequests",checked:d,onchange:m})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="linkify">
            <dl>
              <dt>${i.i18n.getMessage("option_linkify_title")}</dt>
              <dd>${i.i18n.getMessage("option_linkify_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"linkify",checked:l,onchange:_})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="detectIpfsPathHeader">
            <dl>
              <dt>${i.i18n.getMessage("option_detectIpfsPathHeader_title")}</dt>
              <dd>${i.i18n.getMessage("option_detectIpfsPathHeader_description")}
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/companion-x-ipfs-path-header/" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"detectIpfsPathHeader",checked:r,onchange:v})}</div>
        </div>
        <div class="flex-row-ns pb0-ns o-50">
          <label for="ipfsProxy">
            <dl>
              <dt>${i.i18n.getMessage("option_ipfsProxy_title")}</dt>
              <dd>
                Disabled until move to JavaScript API with async await and async iterables
                <!-- TODO: https://github.com/ipfs-shipyard/ipfs-companion/pull/777
                ${i.i18n.getMessage("option_ipfsProxy_description")}
                <p>${p?n`
                    <a class="link underline hover-aqua" href="${i.runtime.getURL("dist/pages/proxy-acl/index.html")}" target="_blank">
                      ${i.i18n.getMessage("option_ipfsProxy_link_manage_permissions")}
                    </a>`:n`<del>${i.i18n.getMessage("option_ipfsProxy_link_manage_permissions")}</del>`}
                </p>
                -->
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/companion-window-ipfs/" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"ipfsProxy",checked:p,disabled:!0,onchange:$})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="logNamespaces">
            <dl>
              <dt>${i.i18n.getMessage("option_logNamespaces_title")}</dt>
              <dd>${i.i18n.getMessage("option_logNamespaces_description")}</dd>
            </dl>
          </label>
          <input
            class="bg-white navy self-center-ns"
            id="logNamespaces"
            type="text"
            required
            onchange=${g("logNamespaces")}
            value=${c} />
        </div>
      </fieldset>
    </form>
  `}},75732:(e,t,s)=>{const i=s(93150),n=s(16566),o=s(34451);e.exports=function({importDir:e,openViaWebUI:t,preloadAtPublicGateway:s,onOptionChange:a}){const l=a("importDir"),d=a("openViaWebUI"),r=a("preloadAtPublicGateway");return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_fileImport")}</h2>
        <div class="flex-row-ns pb0-ns">
          <label for="importDir">
            <dl>
              <dt>${i.i18n.getMessage("option_importDir_title")}</dt>
              <dd>
                ${i.i18n.getMessage("option_importDir_description")}
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/concepts/file-systems/#mutable-file-system-mfs" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <input
            class="bg-white navy self-center-ns"
            id="importDir"
            type="text"
            pattern="^\/(.*)"
            required
            onchange=${l}
            value=${e} />
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="openViaWebUI">
            <dl>
              <dt>${i.i18n.getMessage("option_openViaWebUI_title")}</dt>
              <dd>${i.i18n.getMessage("option_openViaWebUI_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"openViaWebUI",checked:t,onchange:d})}</div>
        </div>
        <div class="flex-row-ns pb0-ns">
          <label for="preloadAtPublicGateway">
            <dl>
              <dt>${i.i18n.getMessage("option_preloadAtPublicGateway_title")}</dt>
              <dd>${i.i18n.getMessage("option_preloadAtPublicGateway_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns">${o({id:"preloadAtPublicGateway",checked:s,onchange:r})}</div>
        </div>
      </fieldset>
    </form>
  `}},51419:(e,t,s)=>{const i=s(93150),n=s(16566),o=s(34451),{guiURLString:a,hostTextToArray:l,hostArrayToText:d}=s(1906),{braveNodeType:r}=s(82945),p=/^https:\/\/|^http:\/\/localhost|^http:\/\/127.0.0.1|^http:\/\/\[::1\]/;e.exports=function({ipfsNodeType:e,customGatewayUrl:t,useCustomGateway:s,useSubdomains:c,disabledOn:g,enabledOn:f,publicGatewayUrl:b,publicSubdomainGatewayUrl:u,onOptionChange:h}){const _=h("customGatewayUrl",(e=>a(e,{useLocalhostName:c}))),m=h("useCustomGateway"),v=h("useSubdomains"),$=h("publicGatewayUrl",a),y=h("publicSubdomainGatewayUrl",a),w=h("disabledOn",l),M=h("enabledOn",l),k=!p.test(t),x="embedded"!==e,P="external"===e,N=e===r?"brave":"";return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_gateways")}</h2>
          <div class="flex-row-ns pb0-ns">
            <label for="publicGatewayUrl">
              <dl>
                <dt>${i.i18n.getMessage("option_publicGatewayUrl_title")}</dt>
                <dd>${i.i18n.getMessage("option_publicGatewayUrl_description")}</dd>
              </dl>
            </label>
            <input
              class="bg-white navy self-center-ns"
              id="publicGatewayUrl"
              type="url"
              inputmode="url"
              required
              pattern="^https?://[^/]+/?$"
              spellcheck="false"
              title="${i.i18n.getMessage("option_hint_url")}"
              onchange=${$}
              value=${b} />
          </div>
          <div class="flex-row-ns pb0-ns">
            <label for="publicSubdomainGatewayUrl">
              <dl>
                <dt>${i.i18n.getMessage("option_publicSubdomainGatewayUrl_title")}</dt>
                <dd>
                  ${i.i18n.getMessage("option_publicSubdomainGatewayUrl_description")}
                  <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/address-ipfs-on-web/#subdomain-gateway" target="_blank">
                    ${i.i18n.getMessage("option_legend_readMore")}
                  </a></p>
                </dd>
              </dl>
            </label>
            <input
              class="bg-white navy self-center-ns"
              id="publicSubdomainGatewayUrl"
              type="url"
              inputmode="url"
              required
              pattern="^https?://[^/]+/?$"
              spellcheck="false"
              title="${i.i18n.getMessage("option_hint_url")}"
              onchange=${y}
              value=${u} />
          </div>
          ${x?n`<div class="flex-row-ns pb0-ns">
              <label for="customGatewayUrl">
                <dl>
                  <dt>${i.i18n.getMessage("option_customGatewayUrl_title")}</dt>
                  <dd>${i.i18n.getMessage("option_customGatewayUrl_description")}
                    ${k?n`<p class="red i">${i.i18n.getMessage("option_customGatewayUrl_warning")}</p>`:null}
                  </dd>
                </dl>
              </label>
              <input
                class="bg-white navy self-center-ns ${N}"
                id="customGatewayUrl"
                type="url"
                inputmode="url"
                required
                pattern="^https?://[^/]+/?$"
                spellcheck="false"
                title="${i.i18n.getMessage(P?"option_hint_url":"option_hint_readonly")}"
                onchange=${_}
                ${P?"":"disabled"}
                value=${t} />
            </div>`:null}
          ${x?n`<div class="flex-row-ns pb0-ns">
              <label for="useCustomGateway">
                <dl>
                  <dt>${i.i18n.getMessage("option_useCustomGateway_title")}</dt>
                  <dd>${i.i18n.getMessage("option_useCustomGateway_description")}</dd>
                </dl>
              </label>
              <div class="self-center-ns">${o({id:"useCustomGateway",checked:s,onchange:m})}</div>
            </div>`:null}
          ${x?n`<div class="flex-row-ns pb0-ns">
              <label for="useSubdomains">
                <dl>
                  <dt>${i.i18n.getMessage("option_useSubdomains_title")}</dt>
                  <dd>
                    ${i.i18n.getMessage("option_useSubdomains_description")}
                    <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/address-ipfs-on-web/#subdomain-gateway" target="_blank">
                      ${i.i18n.getMessage("option_legend_readMore")}
                    </a></p>
                  </dd>
                </dl>
              </label>
              <div class="self-center-ns">${o({id:"useSubdomains",checked:c,onchange:v})}</div>
            </div>`:null}
          ${x?n`<div class="flex-row-ns pb0-ns">
              <label for="disabledOn">
                <dl>
                  <dt>${i.i18n.getMessage("option_disabledOn_title")}</dt>
                  <dd>${i.i18n.getMessage("option_disabledOn_description")}</dd>
                </dl>
              </label>
              <textarea
                class="bg-white navy self-center-ns"
                id="disabledOn"
                spellcheck="false"
                onchange=${w}
                rows="${Math.min(g.length+1,10)}"
                >${d(g)}</textarea>
            </div>
            <div class="flex-row-ns pb0-ns">
              <label for="enabledOn">
                <dl>
                  <dt>${i.i18n.getMessage("option_enabledOn_title")}</dt>
                  <dd>${i.i18n.getMessage("option_enabledOn_description")}</dd>
                </dl>
              </label>
              <textarea
                class="bg-white navy self-center-ns"
                id="enabledOn"
                spellcheck="false"
                onchange=${M}
                rows="${Math.min(f.length+1,10)}"
                >${d(f)}</textarea>
            </div>`:null}

      </fieldset>
    </form>
  `}},64746:(e,t,s)=>{const i=s(93150),n=s(16566),o=s(34451);e.exports=function({active:e,onOptionChange:t}){const s=t("active");return n`
    <form class="db b mb3 bg-aqua-muted charcoal">
      <label for="active" class="dib pa3 flex items-center pointer ${e?"":"charcoal bg-gray-muted br2"}">
        ${o({id:"active",checked:e,onchange:s,style:"mr3"})}
        ${i.i18n.getMessage("panel_headerActiveToggleTitle")}
      </label>
    </form>
  `}},61510:(e,t,s)=>{const i=s(93150),n=s(16566),{braveNodeType:o}=s(82945);e.exports=function({ipfsNodeType:e,ipfsNodeConfig:t,onOptionChange:s,withNodeFromBrave:a}){const l=s("ipfsNodeType"),d=s("ipfsNodeConfig"),r=e===o?"brave":"";return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_nodeType")}</h2>
        <div class="flex-row-ns pb0-ns">
          <label for="ipfsNodeType">
            <dl>
              <dt>${i.i18n.getMessage("option_ipfsNodeType_title")}</dt>
              <dd>
                <p>${i.i18n.getMessage("option_ipfsNodeType_external_description")}</p>
                ${a?n`<p>${i.i18n.getMessage("option_ipfsNodeType_brave_description")}</p>`:null}
                <p>${i.i18n.getMessage("option_ipfsNodeType_embedded_description")}</p>
                <p><a class="link underline hover-aqua" href="https://docs.ipfs.io/how-to/companion-node-types/" target="_blank">
                  ${i.i18n.getMessage("option_legend_readMore")}
                </a></p>
              </dd>
            </dl>
          </label>
          <select id="ipfsNodeType" name='ipfsNodeType' class="self-center-ns bg-white navy ${r}" onchange=${l}>
            <option
              value='external'
              selected=${"external"===e}>
              ${i.i18n.getMessage("option_ipfsNodeType_external")}
            </option>
            ${a?n`<option
                  value='external:brave'
                  selected=${"external:brave"===e}>
                  ${i.i18n.getMessage("option_ipfsNodeType_brave")}
                </option>`:null}
            <option
              value='embedded'
              selected=${"embedded"===e}>
              ${i.i18n.getMessage("option_ipfsNodeType_embedded")} (${i.i18n.getMessage("option_experimental")})
            </option>
          </select>
        </div>
        ${e.startsWith("embedded")?n`<div class="flex-row-ns pb0-ns">
            <label for="ipfsNodeConfig">
              <dl>
                <dt>${i.i18n.getMessage("option_ipfsNodeConfig_title")}</dt>
                <dd>${i.i18n.getMessage("option_ipfsNodeConfig_description")}</dd>
              </dl>
            </label>
            <textarea
              class="bg-white navy self-center-ns"
              spellcheck="false"
              id="ipfsNodeConfig"
              rows="${Math.min((t.match(/\n/g)||[]).length+1,30)}"
              onchange=${d}>${t}</textarea>
          </div>`:null}
      </fieldset>
    </form>
  `}},69422:(e,t,s)=>{const i=s(93150),n=s(16566);e.exports=function({onOptionsReset:e}){return n`
    <form>
      <fieldset class="mb3 pa1 pa4-ns pa3 bg-snow-muted charcoal">
        <h2 class="ttu tracked f6 fw4 teal mt0-ns mb3-ns mb1 mt2 ">${i.i18n.getMessage("option_header_reset")}</h2>
        <div class="flex-row-ns pb0-ns">
          <label for="resetAllOptions">
            <dl>
              <dt>${i.i18n.getMessage("option_resetAllOptions_title")}</dt>
              <dd>${i.i18n.getMessage("option_resetAllOptions_description")}</dd>
            </dl>
          </label>
          <div class="self-center-ns"><button id="resetAllOptions" class="Button transition-all sans-serif v-mid fw5 nowrap lh-copy bn br1 pa2 pointer focus-outline white bg-red white" onclick=${e}>${i.i18n.getMessage("option_resetAllOptions_title")}</button></div>
        </div>
      </fieldset>
    </form>
  `}},93462:(e,t,s)=>{s(39503);const{i18n:i}=s(93150),n=s(72490),o=s(62086),a=s(56036),l=n();l.use(a),l.route("*",o),l.mount("#root"),document.getElementById("header-text").innerText=i.getMessage("option_page_header"),document.title=i.getMessage("option_page_title")},62086:(e,t,s)=>{const i=s(16566),n=s(64746),o=s(61510),a=s(75732),l=s(99068),d=s(51419),r=s(59390),p=s(8082),c=s(69422);e.exports=function(e,t){const s=(e,s)=>i=>{i.preventDefault();const n="checkbox"===i.target.type?i.target.checked:i.target.value;if(!i.target.reportValidity())return console.warn(`[ipfs-companion] Invalid value for ${e}: ${n}`);t("optionChange",{key:e,value:s?s(n):n}),s&&t("render")};return e.options.active?i`
    <div class="sans-serif">
  ${n({active:e.options.active,onOptionChange:s})}
  ${o({ipfsNodeType:e.options.ipfsNodeType,ipfsNodeConfig:e.options.ipfsNodeConfig,withNodeFromBrave:e.withNodeFromBrave,onOptionChange:s})}
  ${e.options.ipfsNodeType.startsWith("external")?r({ipfsNodeType:e.options.ipfsNodeType,ipfsApiUrl:e.options.ipfsApiUrl,ipfsApiPollMs:e.options.ipfsApiPollMs,automaticMode:e.options.automaticMode,onOptionChange:s}):null}
  ${d({ipfsNodeType:e.options.ipfsNodeType,customGatewayUrl:e.options.customGatewayUrl,useCustomGateway:e.options.useCustomGateway,useSubdomains:e.options.useSubdomains,publicGatewayUrl:e.options.publicGatewayUrl,publicSubdomainGatewayUrl:e.options.publicSubdomainGatewayUrl,disabledOn:e.options.disabledOn,enabledOn:e.options.enabledOn,onOptionChange:s})}
  ${a({importDir:e.options.importDir,openViaWebUI:e.options.openViaWebUI,preloadAtPublicGateway:e.options.preloadAtPublicGateway,onOptionChange:s})}
  ${l({dnslinkPolicy:e.options.dnslinkPolicy,dnslinkDataPreload:e.options.dnslinkDataPreload,dnslinkRedirect:e.options.dnslinkRedirect,onOptionChange:s})}
  ${p({useLatestWebUI:e.options.useLatestWebUI,displayNotifications:e.options.displayNotifications,displayReleaseNotes:e.options.displayReleaseNotes,catchUnhandledProtocols:e.options.catchUnhandledProtocols,linkify:e.options.linkify,recoverFailedHttpRequests:e.options.recoverFailedHttpRequests,detectIpfsPathHeader:e.options.detectIpfsPathHeader,ipfsProxy:e.options.ipfsProxy,logNamespaces:e.options.logNamespaces,onOptionChange:s})}
  ${c({onOptionsReset:e=>{e.preventDefault(),t("optionsReset")}})}
    </div>
  `:i`
    <div class="sans-serif">
  ${n({active:e.options.active,onOptionChange:s})}
    </div>
    `}},56036:(e,t,s)=>{const i=s(93150),{optionDefaults:n}=s(1906),{createRuntimeChecks:o}=s(75570);e.exports=(e,t)=>{e.options=n;const s=async()=>{const s=await o(i);e.withNodeFromBrave=s.brave&&await s.brave.getIPFSEnabled(),e.options=await async function(){const e=await i.storage.local.get();return Object.keys(n).reduce(((t,s)=>(t[s]=null==e[s]?n[s]:e[s],t)),{})}(),t.emit("render")};t.on("DOMContentLoaded",(async()=>{s(),i.storage.onChanged.addListener(s)})),t.on("optionChange",(({key:e,value:t})=>i.storage.local.set({[e]:t}))),t.on("optionsReset",(()=>i.storage.local.set(n)))}},39503:(e,t,s)=>{s.r(t)}},t={};function s(i){if(t[i])return t[i].exports;var n=t[i]={exports:{}};return e[i].call(n.exports,n,n.exports,s),n.exports}s.m=e,s.x=e=>{},s.amdO={},s.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),s.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e={407:0},t=[[93462,297]],i=e=>{},n=(n,o)=>{for(var a,l,[d,r,p,c]=o,g=0,f=[];g<d.length;g++)l=d[g],s.o(e,l)&&e[l]&&f.push(e[l][0]),e[l]=0;for(a in r)s.o(r,a)&&(s.m[a]=r[a]);for(p&&p(s),n&&n(o);f.length;)f.shift()();return c&&t.push.apply(t,c),i()},o=self.webpackChunkipfs_companion=self.webpackChunkipfs_companion||[];function a(){for(var i,n=0;n<t.length;n++){for(var o=t[n],a=!0,l=1;l<o.length;l++){var d=o[l];0!==e[d]&&(a=!1)}a&&(t.splice(n--,1),i=s(s.s=o[0]))}return 0===t.length&&(s.x(),s.x=e=>{}),i}o.forEach(n.bind(null,0)),o.push=n.bind(null,o.push.bind(o));var l=s.x;s.x=()=>(s.x=l||(e=>{}),(i=a)())})();s.x()})();