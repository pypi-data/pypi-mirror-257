"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9041],{60972:(e,t,a)=>{a.d(t,{Z:()=>c});var n=a(67294),l=a(61988),o=a(34858),i=a(29487),r=a(11965);const s=(0,o.z)(),d=s?s.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c=({errorMessage:e,showDbInstallInstructions:t})=>(0,r.tZ)(i.Z,{closable:!1,css:e=>(e=>r.iv`
  border: 1px solid ${e.colors.warning.light1};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;
  color: ${e.colors.warning.dark2};

  .ant-alert-message {
    margin: 0;
  }

  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),type:"error",showIcon:!0,message:e,description:t?(0,r.tZ)(n.Fragment,null,(0,r.tZ)("br",null),(0,l.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: "),(0,r.tZ)("a",{href:d,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},(0,l.t)("here")),"."):""})},49576:(e,t,a)=>{a.d(t,{Z:()=>h});var n=a(67294),l=a(51995),o=a(70707),i=a(11965);const r=l.iK.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,l.iK)(o.Z.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,l.iK)(o.Z.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,l.iK)(o.Z.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,u=l.iK.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,p=l.iK.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,h=(0,n.forwardRef)((({indeterminate:e,id:t,checked:a,onChange:l,title:o="",labelText:h=""},m)=>{const g=(0,n.useRef)(),v=m||g;return(0,n.useEffect)((()=>{v.current.indeterminate=e}),[v,e]),(0,i.tZ)(n.Fragment,null,(0,i.tZ)(p,null,e&&(0,i.tZ)(s,null),!e&&a&&(0,i.tZ)(c,null),!e&&!a&&(0,i.tZ)(d,null),(0,i.tZ)(u,{name:t,id:t,type:"checkbox",ref:v,checked:a,onChange:l})),(0,i.tZ)(r,{title:o,htmlFor:t},h))}))},1315:(e,t,a)=>{a.d(t,{Us:()=>ot,Gr:()=>it,ZP:()=>dt});var n=a(78718),l=a.n(n),o=a(41609),i=a.n(o),r=a(75049),s=a(51995),d=a(61988),c=a(93185),u=a(67294),p=a(16550),h=a(61337),m=a(71262),g=a(4715),v=a(29487),b=a(74069),y=a(35932),f=a(70707);function Z(){return Z=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(e[n]=a[n])}return e},Z.apply(this,arguments)}const x={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},_=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"];function w(e,t){for(;e&&t--;)e=e.previousElementSibling;return e}const C={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},S=Object.keys(C);class $ extends u.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas.parentNode.removeChild(this.canvas)}setState(e,t){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,t)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(x).forEach((t=>{e.style[t]=x[t]})),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);_.forEach((t=>{this.canvas.style[t]=e[t]}))}reflow(e){const t=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(t){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${t}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map((e=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("");const a=this.putEllipsis(this.calcIndexes()),n=a>-1,l={clamped:n,text:n?this.units.slice(0,a).join(""):e.text};this.setState(l,e.onReflow.bind(this,l))}calcIndexes(){const e=[0];let t=this.canvas.firstElementChild;if(!t)return e;let a=0,n=1,l=t.offsetTop;for(;(t=t.nextElementSibling)&&(t.offsetTop>l&&(n++,e.push(a),l=t.offsetTop),a++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const t=e[this.maxLine],a=this.units.slice(0,t),n=this.canvas.children[t].offsetTop;this.canvas.innerHTML=a.map(((e,t)=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const l=this.canvas.lastElementChild;let o=w(l,2);for(;o&&(l.offsetTop>n||l.offsetHeight>o.offsetHeight||l.offsetTop>o.offsetTop);)this.canvas.removeChild(o),o=w(l,2),a.pop();return a.length}isClamped(){return this.clamped}render(){const{text:e,clamped:t}=this.state,a=this.props,{component:n,ellipsis:l,trimRight:o,className:i}=a,r=function(e,t){if(null==e)return{};var a,n,l={},o=Object.keys(e);for(n=0;n<o.length;n++)a=o[n],t.indexOf(a)>=0||(l[a]=e[a]);return l}(a,["component","ellipsis","trimRight","className"]);return u.createElement(n,Z({className:`LinesEllipsis ${t?"LinesEllipsis--clamped":""} ${i}`,ref:e=>this.target=e},function(e,t){if(!e||"object"!=typeof e)return e;const a={};return Object.keys(e).forEach((n=>{t.indexOf(n)>-1||(a[n]=e[n])})),a}(r,S)),t&&o?e.replace(/[\s\uFEFF\xA0]+$/,""):e,u.createElement("wbr",null),t&&u.createElement("span",{className:"LinesEllipsis-ellipsis"},l))}}$.defaultProps=C;const k=$;var N=a(11965);const E=(0,s.iK)(y.Z)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,U=s.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,T=s.iK.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,M=s.iK.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`,A=(0,s.iK)((({icon:e,altText:t,buttonText:a,...n})=>(0,N.tZ)(E,n,(0,N.tZ)(U,null,e&&(0,N.tZ)("img",{src:e,alt:t}),!e&&(0,N.tZ)(f.Z.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})),(0,N.tZ)(M,null,(0,N.tZ)(T,null,(0,N.tZ)(k,{text:a,maxLine:"2",basedOn:"words",trimRight:!0}))))))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`;var P,D,L=a(8272),q=a(14114),O=a(12353),I=a(72875),F=a(60972),R=a(34858),z=a(18451),H=a(38703);!function(e){e.SqlalchemyUri="sqlalchemy_form",e.DynamicForm="dynamic_form"}(P||(P={})),function(e){e.GSheet="gsheets",e.Snowflake="snowflake"}(D||(D={}));var K=a(94184),j=a.n(K),B=a(49576),J=a(43700),Q=a(94670);const V=N.iv`
  margin-bottom: 0;
`,W=s.iK.header`
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  .subheader-text {
    line-height: ${({theme:e})=>4.25*e.gridUnit}px;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,G=N.iv`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,X=N.iv`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,Y=e=>N.iv`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,ee=e=>N.iv`
  padding-left: ${2*e.gridUnit}px;
`,te=e=>N.iv`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,ae=e=>N.iv`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,ne=e=>N.iv`
  border: 1px solid ${e.colors.info.base};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;

  .ant-alert-message {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.m}px;
    font-weight: ${e.typography.weights.bold};
  }

  .ant-alert-description {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.m}px;
    line-height: ${5*e.gridUnit}px;

    a {
      text-decoration: underline;
    }

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,le=s.iK.div`
  ${({theme:e})=>N.iv`
    margin: 0 ${4*e.gridUnit}px -${4*e.gridUnit}px;
  `}
`,oe=e=>N.iv`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    text-align: left;
  }
`,ie=e=>N.iv`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 480px;
  }
`,re=e=>N.iv`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
    margin-bottom: 0;
  }
`,se=s.iK.div`
  ${({theme:e})=>N.iv`
    margin-bottom: ${6*e.gridUnit}px;
    &.mb-0 {
      margin-bottom: 0;
    }
    &.mb-8 {
      margin-bottom: ${2*e.gridUnit}px;
    }

    .control-label {
      color: ${e.colors.grayscale.dark1};
      font-size: ${e.typography.sizes.s}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    &.extra-container {
      padding-top: ${2*e.gridUnit}px;
    }

    .input-container {
      display: flex;
      align-items: top;

      label {
        display: flex;
        margin-left: ${2*e.gridUnit}px;
        margin-top: ${.75*e.gridUnit}px;
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
      }

      i {
        margin: 0 ${e.gridUnit}px;
      }
    }

    input,
    textarea {
      flex: 1 1 auto;
    }

    textarea {
      height: 160px;
      resize: none;
    }

    input::placeholder,
    textarea::placeholder {
      color: ${e.colors.grayscale.light1};
    }

    textarea,
    input[type='text'],
    input[type='number'] {
      padding: ${1.5*e.gridUnit}px ${2*e.gridUnit}px;
      border-style: none;
      border: 1px solid ${e.colors.grayscale.light2};
      border-radius: ${e.gridUnit}px;

      &[name='name'] {
        flex: 0 1 auto;
        width: 40%;
      }
    }
    &.expandable {
      height: 0;
      overflow: hidden;
      transition: height 0.25s;
      margin-left: ${8*e.gridUnit}px;
      margin-bottom: 0;
      padding: 0;
      .control-label {
        margin-bottom: 0;
      }
      &.open {
        height: ${108}px;
        padding-right: ${5*e.gridUnit}px;
      }
    }
  `}
`,de=(0,s.iK)(Q.Ad)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,ce=s.iK.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${261}px;
      &.ctas-open {
        height: ${363}px;
      }
    }
  }
`,ue=s.iK.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,pe=e=>N.iv`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,he=e=>N.iv`
  font-size: ${3.5*e.gridUnit}px;
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,me=s.iK.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0px;
  }
`,ge=(s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  text-transform: uppercase;
`),ve=s.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,be=s.iK.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    text-transform: uppercase;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none !important;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,ye=s.iK.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>e.typography.sizes.l}px;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    text-transform: uppercase;
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,fe=(0,s.iK)(y.Z)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,Ze=s.iK.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
  height: auto;
`,xe=s.iK.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,_e=s.iK.div`
  .ant-progress-inner {
    display: none;
  }

  .ant-upload-list-item-card-actions {
    display: none;
  }
`,we=({db:e,onInputChange:t,onTextChange:a,onEditorChange:n,onExtraInputChange:l,onExtraEditorChange:o,extraExtension:i})=>{var r,s,c,u;const p=!(null==e||!e.expose_in_sqllab),h=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas),m=null==e||null==(r=e.engine_information)?void 0:r.supports_file_upload,g=JSON.parse((null==e?void 0:e.extra)||"{}",((e,t)=>"engine_params"===e&&"object"==typeof t?JSON.stringify(t):t)),v=null==i?void 0:i.component,b=null==i?void 0:i.logo,y=null==i?void 0:i.description;return(0,N.tZ)(J.Z,{expandIconPosition:"right",accordion:!0,css:e=>(e=>N.iv`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e)},(0,N.tZ)(J.Z.Panel,{header:(0,N.tZ)("div",null,(0,N.tZ)("h4",null,(0,d.t)("SQL Lab")),(0,N.tZ)("p",{className:"helper"},(0,d.t)("Adjust how this database will interact with SQL Lab."))),key:"1"},(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:t,labelText:(0,d.t)("Expose database in SQL Lab")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Allow this database to be queried in SQL Lab")})),(0,N.tZ)(ce,{className:j()("expandable",{open:p,"ctas-open":h})},(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:t,labelText:(0,d.t)("Allow CREATE TABLE AS")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Allow creation of new tables based on queries")}))),(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:t,labelText:(0,d.t)("Allow CREATE VIEW AS")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Allow creation of new views based on queries")})),(0,N.tZ)(se,{className:j()("expandable",{open:h})},(0,N.tZ)("div",{className:"control-label"},(0,d.t)("CTAS & CVAS SCHEMA")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"text",name:"force_ctas_schema",placeholder:(0,d.t)("Create or select schema..."),onChange:t,value:(null==e?void 0:e.force_ctas_schema)||""})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")))),(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:t,labelText:(0,d.t)("Allow DML")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")}))),(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==g||!g.cost_estimate_enabled),onChange:l,labelText:(0,d.t)("Enable query cost estimation")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("For Bigquery, Presto and Postgres, shows a button to compute cost before running a query.")}))),(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!(null==g||!g.allows_virtual_table_explore),onChange:l,labelText:(0,d.t)("Allow this database to be explored")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("When enabled, users are able to visualize SQL Lab results in Explore.")}))),(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"disable_data_preview",indeterminate:!1,checked:!(null==g||!g.disable_data_preview),onChange:l,labelText:(0,d.t)("Disable SQL Lab data preview queries")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Disable data preview when fetching table metadata in SQL Lab.  Useful to avoid browser performance issues when using  databases with very wide tables.")}))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"expand_rows",indeterminate:!1,checked:!(null==g||null==(s=g.schema_options)||!s.expand_rows),onChange:l,labelText:(0,d.t)("Enable row expansion in schemas")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("For Trino, describe full schemas of nested ROW types, expanding them with dotted paths")})))))),(0,N.tZ)(J.Z.Panel,{header:(0,N.tZ)("div",null,(0,N.tZ)("h4",null,(0,d.t)("Performance")),(0,N.tZ)("p",{className:"helper"},(0,d.t)("Adjust performance settings of this database."))),key:"2"},(0,N.tZ)(se,{className:"mb-8"},(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Chart cache timeout")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:t})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires, and -1 bypasses the cache. Note this defaults to the global timeout if undefined."))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Schema cache timeout")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"number",name:"schema_cache_timeout",value:(null==g||null==(c=g.metadata_cache_timeout)?void 0:c.schema_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires."))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Table cache timeout")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"number",name:"table_cache_timeout",value:(null==g||null==(u=g.metadata_cache_timeout)?void 0:u.table_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. "))),(0,N.tZ)(se,{css:(0,N.iv)({no_margin_bottom:V},"","")},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allow_run_async",indeterminate:!1,checked:!(null==e||!e.allow_run_async),onChange:t,labelText:(0,d.t)("Asynchronous query execution")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}))),(0,N.tZ)(se,{css:(0,N.iv)({no_margin_bottom:V},"","")},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==g||!g.cancel_query_on_windows_unload),onChange:l,labelText:(0,d.t)("Cancel query on window unload event")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})))),(0,N.tZ)(J.Z.Panel,{header:(0,N.tZ)("div",null,(0,N.tZ)("h4",null,(0,d.t)("Security")),(0,N.tZ)("p",{className:"helper"},(0,d.t)("Add extra connection information."))),key:"3"},(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Secure extra")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(de,{name:"masked_encrypted_extra",value:(null==e?void 0:e.masked_encrypted_extra)||"",placeholder:(0,d.t)("Secure extra"),onChange:e=>n({json:e,name:"masked_encrypted_extra"}),width:"100%",height:"160px"})),(0,N.tZ)("div",{className:"helper"},(0,N.tZ)("div",null,(0,d.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Root certificate")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,d.t)("Enter CA_BUNDLE"),onChange:a})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines."))),(0,N.tZ)(se,{css:m?{}:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:t,labelText:(0,d.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")}))),m&&(0,N.tZ)(se,{css:null!=e&&e.allow_file_upload?{}:V},(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(B.Z,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:t,labelText:(0,d.t)("Allow file uploads to database")}))),m&&!(null==e||!e.allow_file_upload)&&(0,N.tZ)(se,{css:V},(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Schemas allowed for File upload")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==g?void 0:g.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("A comma-separated list of schemas that files are allowed to upload to.")))),i&&v&&y&&(0,N.tZ)(J.Z.Panel,{header:(0,N.tZ)("div",null,b&&(0,N.tZ)(b,null),(0,N.tZ)("span",{css:e=>({fontSize:e.typography.sizes.l,fontWeight:e.typography.weights.bold})},null==i?void 0:i.title),(0,N.tZ)("p",{className:"helper"},(0,N.tZ)(y,null))),key:null==i?void 0:i.title,collapsible:null!=i.enabled&&i.enabled()?"icon":"disabled"},(0,N.tZ)(se,{css:V},(0,N.tZ)(v,{db:e,onEdit:i.onEdit}))),(0,N.tZ)(J.Z.Panel,{header:(0,N.tZ)("div",null,(0,N.tZ)("h4",null,(0,d.t)("Other")),(0,N.tZ)("p",{className:"helper"},(0,d.t)("Additional settings."))),key:"4"},(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Metadata Parameters")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(de,{name:"metadata_params",placeholder:(0,d.t)("Metadata Parameters"),onChange:e=>o({json:e,name:"metadata_params"}),width:"100%",height:"160px",value:Object.keys((null==g?void 0:g.metadata_params)||{}).length?null==g?void 0:g.metadata_params:""})),(0,N.tZ)("div",{className:"helper"},(0,N.tZ)("div",null,(0,d.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Engine Parameters")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(de,{name:"engine_params",placeholder:(0,d.t)("Engine Parameters"),onChange:e=>o({json:e,name:"engine_params"}),width:"100%",height:"160px",value:Object.keys((null==g?void 0:g.engine_params)||{}).length?null==g?void 0:g.engine_params:""})),(0,N.tZ)("div",{className:"helper"},(0,N.tZ)("div",null,(0,d.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Version")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"text",name:"version",placeholder:(0,d.t)("Version number"),onChange:l,value:(null==g?void 0:g.version)||""})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Specify the database version. This is used with Presto for query cost estimation, and Dremio for syntax changes, among others.")))))};var Ce=a(8911);const Se=({db:e,onInputChange:t,testConnection:a,conf:n,testInProgress:l=!1,children:o})=>{var i,r;const s=(null==Ce.Z||null==(i=Ce.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:i.SQLALCHEMY_DOCS_URL)||"https://docs.sqlalchemy.org/en/13/core/engines.html",c=(null==Ce.Z||null==(r=Ce.Z.DB_MODAL_SQLALCHEMY_FORM)?void 0:r.SQLALCHEMY_DISPLAY_TEXT)||"SQLAlchemy docs";return(0,N.tZ)(u.Fragment,null,(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Display Name"),(0,N.tZ)("span",{className:"required"},"*")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:(0,d.t)("Name your database"),onChange:t})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Pick a name to help you identify this database."))),(0,N.tZ)(se,null,(0,N.tZ)("div",{className:"control-label"},(0,d.t)("SQLAlchemy URI"),(0,N.tZ)("span",{className:"required"},"*")),(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(null==e?void 0:e.sqlalchemy_uri_placeholder)||(0,d.t)("dialect+driver://username:password@host:port/database"),onChange:t})),(0,N.tZ)("div",{className:"helper"},(0,d.t)("Refer to the")," ",(0,N.tZ)("a",{href:s||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer"},c||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||"")," ",(0,d.t)("for more information on how to structure your URI."))),o,(0,N.tZ)(y.Z,{onClick:a,loading:l,cta:!0,buttonStyle:"link",css:e=>(e=>N.iv`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e)},(0,d.t)("Test connection")))};var $e=a(49238);const ke={account:{helpText:(0,d.t)("Copy the identifier of the account you are trying to connect to."),placeholder:(0,d.t)("e.g. xy12345.us-east-2.aws")},warehouse:{placeholder:(0,d.t)("e.g. compute_wh"),className:"form-group-w-50"},role:{placeholder:(0,d.t)("e.g. AccountAdmin"),className:"form-group-w-50"}},Ne=({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l,field:o})=>{var i;return(0,N.tZ)(O.Z,{id:o,name:o,required:e,value:null==l||null==(i=l.parameters)?void 0:i[o],validationMethods:{onBlur:a},errorMessage:null==n?void 0:n[o],placeholder:ke[o].placeholder,helpText:ke[o].helpText,label:o,onChange:t.onParametersChange,className:ke[o].className||o})};var Ee,Ue=a(2857);!function(e){e[e.JsonUpload=0]="JsonUpload",e[e.CopyPaste=1]="CopyPaste"}(Ee||(Ee={}));const Te={gsheets:"service_account_info",bigquery:"credentials_info"};var Me={name:"s5xdrg",styles:"display:flex;align-items:center"};const Ae=({changeMethods:e,isEditMode:t,db:a,editNewDb:n})=>{var l,o,i;const[r,s]=(0,u.useState)(Ee.JsonUpload.valueOf()),[c,p]=(0,u.useState)(null),[h,m]=(0,u.useState)(!0),v="gsheets"===(null==a?void 0:a.engine)?!t&&!h:!t,b=t&&"{}"!==(null==a?void 0:a.masked_encrypted_extra),y=(null==a?void 0:a.engine)&&Te[a.engine],Z="object"==typeof(null==a||null==(l=a.parameters)?void 0:l[y])?JSON.stringify(null==a||null==(o=a.parameters)?void 0:o[y]):null==a||null==(i=a.parameters)?void 0:i[y];return(0,N.tZ)(be,null,"gsheets"===(null==a?void 0:a.engine)&&(0,N.tZ)("div",{className:"catalog-type-select"},(0,N.tZ)(Ue.Z,{css:e=>(e=>N.iv`
  margin-bottom: ${2*e.gridUnit}px;
`)(e),required:!0},(0,d.t)("Type of Google Sheets allowed")),(0,N.tZ)(g.IZ,{style:{width:"100%"},defaultValue:b?"false":"true",onChange:e=>m("true"===e)},(0,N.tZ)(g.IZ.Option,{value:"true",key:1},(0,d.t)("Publicly shared sheets only")),(0,N.tZ)(g.IZ.Option,{value:"false",key:2},(0,d.t)("Public and privately shared sheets")))),v&&(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Ue.Z,{required:!0},(0,d.t)("How do you want to enter service account credentials?")),(0,N.tZ)(g.IZ,{defaultValue:r,style:{width:"100%"},onChange:e=>s(e)},(0,N.tZ)(g.IZ.Option,{value:Ee.JsonUpload},(0,d.t)("Upload JSON file")),(0,N.tZ)(g.IZ.Option,{value:Ee.CopyPaste},(0,d.t)("Copy and Paste JSON credentials")))),r===Ee.CopyPaste||t||n?(0,N.tZ)("div",{className:"input-container"},(0,N.tZ)(Ue.Z,{required:!0},(0,d.t)("Service Account")),(0,N.tZ)("textarea",{className:"input-form",name:y,value:Z,onChange:e.onParametersChange,placeholder:(0,d.t)("Paste content of service credentials JSON file here")}),(0,N.tZ)("span",{className:"label-paste"},(0,d.t)("Copy and paste the entire service account .json file here"))):v&&(0,N.tZ)("div",{className:"input-container",css:e=>Y(e)},(0,N.tZ)("div",{css:Me},(0,N.tZ)(Ue.Z,{required:!0},(0,d.t)("Upload Credentials")),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Use the JSON file you automatically downloaded when creating your service account."),viewBox:"0 0 24 24"})),!c&&(0,N.tZ)(g.C0,{className:"input-upload-btn",onClick:()=>{var e,t;return null==(e=document)||null==(t=e.getElementById("selectedFile"))?void 0:t.click()}},(0,d.t)("Choose File")),c&&(0,N.tZ)("div",{className:"input-upload-current"},c,(0,N.tZ)(f.Z.DeleteFilled,{iconSize:"m",onClick:()=>{p(null),e.onParametersChange({target:{name:y,value:""}})}})),(0,N.tZ)("input",{id:"selectedFile",accept:".json",className:"input-upload",type:"file",onChange:async t=>{var a,n;let l;t.target.files&&(l=t.target.files[0]),p(null==(a=l)?void 0:a.name),e.onParametersChange({target:{type:null,name:y,value:await(null==(n=l)?void 0:n.text()),checked:!1}}),document.getElementById("selectedFile").value=null}})))},Pe=["host","port","database","username","password","access_token","http_path","database_name","credentials_info","service_account_info","catalog","query","encryption","account","warehouse","role","ssh"],De={host:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>{var o;return(0,N.tZ)(O.Z,{id:"host",name:"host",value:null==l||null==(o=l.parameters)?void 0:o.host,required:e,hasTooltip:!0,tooltipText:(0,d.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.host,placeholder:(0,d.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,d.t)("Host"),onChange:t.onParametersChange})},http_path:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>{var o,i;const r=JSON.parse((null==l?void 0:l.extra)||"{}");return(0,N.tZ)(O.Z,{id:"http_path",name:"http_path",required:e,value:null==(o=r.engine_params)||null==(i=o.connect_args)?void 0:i.http_path,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:t.onExtraInputChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},port:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>{var o;return(0,N.tZ)(u.Fragment,null,(0,N.tZ)(O.Z,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(o=l.parameters)?void 0:o.port,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.port,placeholder:(0,d.t)("e.g. 5432"),className:"form-group-w-50",label:(0,d.t)("Port"),onChange:t.onParametersChange}))},database:({required:e,changeMethods:t,getValidation:a,validationErrors:n,placeholder:l,db:o})=>{var i;return(0,N.tZ)(O.Z,{id:"database",name:"database",required:e,value:null==o||null==(i=o.parameters)?void 0:i.database,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.database,placeholder:null!=l?l:(0,d.t)("e.g. world_population"),label:(0,d.t)("Database name"),onChange:t.onParametersChange,helpText:(0,d.t)("Copy the name of the database you are trying to connect to.")})},username:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>{var o;return(0,N.tZ)(O.Z,{id:"username",name:"username",required:e,value:null==l||null==(o=l.parameters)?void 0:o.username,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.username,placeholder:(0,d.t)("e.g. Analytics"),label:(0,d.t)("Username"),onChange:t.onParametersChange})},password:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l,isEditMode:o})=>{var i;return(0,N.tZ)(O.Z,{id:"password",name:"password",required:e,visibilityToggle:!o,value:null==l||null==(i=l.parameters)?void 0:i.password,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.password,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Password"),onChange:t.onParametersChange})},access_token:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l,isEditMode:o})=>{var i;return(0,N.tZ)(O.Z,{id:"access_token",name:"access_token",required:e,visibilityToggle:!o,value:null==l||null==(i=l.parameters)?void 0:i.access_token,validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.access_token,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Access token"),onChange:t.onParametersChange})},database_name:({changeMethods:e,getValidation:t,validationErrors:a,db:n})=>(0,N.tZ)(u.Fragment,null,(0,N.tZ)(O.Z,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:t},errorMessage:null==a?void 0:a.database_name,placeholder:"",label:(0,d.t)("Display Name"),onChange:e.onChange,helpText:(0,d.t)("Pick a nickname for how the database will display in Superset.")})),query:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>(0,N.tZ)(O.Z,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:a},errorMessage:null==n?void 0:n.query,placeholder:(0,d.t)("e.g. param1=value1&param2=value2"),label:(0,d.t)("Additional Parameters"),onChange:t.onQueryChange,helpText:(0,d.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:t,db:a,sslForced:n})=>{var l;return(0,N.tZ)("div",{css:e=>Y(e)},(0,N.tZ)(g.KU,{disabled:n&&!e,checked:(null==a||null==(l=a.parameters)?void 0:l.encryption)||n,onChange:e=>{t.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,N.tZ)("span",{css:ee},"SSL"),(0,N.tZ)(L.Z,{tooltip:(0,d.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"}))},credentials_info:Ae,service_account_info:Ae,catalog:({required:e,changeMethods:t,getValidation:a,validationErrors:n,db:l})=>{const o=(null==l?void 0:l.catalog)||[],i=n||{};return(0,N.tZ)(xe,null,(0,N.tZ)("h4",{className:"gsheet-title"},(0,d.t)("Connect Google Sheets as tables to this database")),(0,N.tZ)("div",null,null==o?void 0:o.map(((n,l)=>{var r,s;return(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Ue.Z,{className:"catalog-label",required:!0},(0,d.t)("Google Sheet Name and URL")),(0,N.tZ)("div",{className:"catalog-name"},(0,N.tZ)(O.Z,{className:"catalog-name-input",required:e,validationMethods:{onBlur:a},errorMessage:null==(r=i[l])?void 0:r.name,placeholder:(0,d.t)("Enter a name for this sheet"),onChange:e=>{t.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:n.name}),(null==o?void 0:o.length)>1&&(0,N.tZ)(f.Z.CloseOutlined,{css:e=>N.iv`
                    align-self: center;
                    background: ${e.colors.grayscale.light4};
                    margin: 5px 5px 8px 5px;

                    &.anticon > * {
                      line-height: 0;
                    }
                  `,iconSize:"m",onClick:()=>t.onRemoveTableCatalog(l)})),(0,N.tZ)(O.Z,{className:"catalog-name-url",required:e,validationMethods:{onBlur:a},errorMessage:null==(s=i[l])?void 0:s.url,placeholder:(0,d.t)("Paste the shareable Google Sheet URL here"),onChange:e=>t.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:n.value}))})),(0,N.tZ)(fe,{className:"catalog-add-btn",onClick:()=>{t.onAddTableCatalog()}},"+ ",(0,d.t)("Add sheet"))))},warehouse:Ne,role:Ne,account:Ne,ssh:({isEditMode:e,changeMethods:t,clearValidationErrors:a,db:n})=>{var l;return(0,N.tZ)("div",{css:e=>Y(e)},(0,N.tZ)(g.KU,{disabled:e&&!i()(null==n?void 0:n.ssh_tunnel),checked:null==n||null==(l=n.parameters)?void 0:l.ssh,onChange:e=>{t.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:e}}),a()}}),(0,N.tZ)("span",{css:ee},(0,d.t)("SSH Tunnel")),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"}))}},Le=({dbModel:{parameters:e},db:t,editNewDb:a,getPlaceholder:n,getValidation:l,isEditMode:o=!1,onAddTableCatalog:i,onChange:r,onExtraInputChange:s,onParametersChange:d,onParametersUploadFileChange:c,onQueryChange:u,onRemoveTableCatalog:p,sslForced:h,validationErrors:m,clearValidationErrors:g})=>(0,N.tZ)($e.l0,null,(0,N.tZ)("div",{css:e=>[te,re(e)]},e&&Pe.filter((t=>Object.keys(e.properties).includes(t)||"database_name"===t)).map((v=>{var b;return De[v]({required:null==(b=e.required)?void 0:b.includes(v),changeMethods:{onParametersChange:d,onChange:r,onQueryChange:u,onParametersUploadFileChange:c,onAddTableCatalog:i,onRemoveTableCatalog:p,onExtraInputChange:s},validationErrors:m,getValidation:l,clearValidationErrors:g,db:t,key:v,field:v,isEditMode:o,sslForced:h,editNewDb:a,placeholder:n?n(v):void 0})})))),qe=(0,R.z)(),Oe=qe?qe.support:"https://superset.apache.org/docs/databases/installing-database-drivers",Ie={postgresql:"https://superset.apache.org/docs/databases/postgres",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},Fe=({isLoading:e,isEditMode:t,useSqlAlchemyForm:a,hasConnectedDb:n,db:l,dbName:o,dbModel:i,editNewDb:r,fileList:s})=>{const c=s&&(null==s?void 0:s.length)>0,p=(0,N.tZ)(W,null,(0,N.tZ)(ge,null,null==l?void 0:l.backend),(0,N.tZ)(ve,null,o)),h=(0,N.tZ)(W,null,(0,N.tZ)("p",{className:"helper-top"},(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})),(0,N.tZ)("h4",null,(0,d.t)("Enter Primary Credentials")),(0,N.tZ)("p",{className:"helper-bottom"},(0,d.t)("Need help? Learn how to connect your database")," ",(0,N.tZ)("a",{href:(null==qe?void 0:qe.default)||Oe,target:"_blank",rel:"noopener noreferrer"},(0,d.t)("here")),".")),m=(0,N.tZ)(Ze,null,(0,N.tZ)(W,null,(0,N.tZ)("p",{className:"helper-top"},(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:3,stepLast:3})),(0,N.tZ)("h4",{className:"step-3-text"},(0,d.t)("Database connected")),(0,N.tZ)("p",{className:"subheader-text"},(0,d.t)("Create a dataset to begin visualizing your data as a chart or go to\n          SQL Lab to query your data.")))),g=(0,N.tZ)(Ze,null,(0,N.tZ)(W,null,(0,N.tZ)("p",{className:"helper-top"},(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:3})),(0,N.tZ)("h4",null,(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})),(0,N.tZ)("p",{className:"helper-bottom"},(0,d.t)("Need help? Learn more about")," ",(0,N.tZ)("a",{href:(v=null==l?void 0:l.engine,v?qe?qe[v]||qe.default:Ie[v]?Ie[v]:`https://superset.apache.org/docs/databases/${v}`:null),target:"_blank",rel:"noopener noreferrer"},(0,d.t)("connecting to %(dbModelName)s.",{dbModelName:i.name}),"."))));var v;const b=(0,N.tZ)(W,null,(0,N.tZ)("div",{className:"select-db"},(0,N.tZ)("p",{className:"helper-top"},(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:1,stepLast:3})),(0,N.tZ)("h4",null,(0,d.t)("Select a database to connect")))),y=(0,N.tZ)(Ze,null,(0,N.tZ)(W,null,(0,N.tZ)("p",{className:"helper-top"},(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})),(0,N.tZ)("h4",null,(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})),(0,N.tZ)("p",{className:"helper-bottom"},c?s[0].name:"")));return c?y:e?(0,N.tZ)(u.Fragment,null):t?p:a?h:n&&!r?m:l||r?g:b};var Re=a(87183),ze=a(9875),He=a(77808),Ke=a(31097),je=a(10038),Be=a(55287);const Je=s.iK.div`
  padding-top: ${({theme:e})=>2*e.gridUnit}px;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
    text-transform: uppercase;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,Qe=(0,s.iK)(g.X2)`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,Ve=(0,s.iK)(g.qz.Item)`
  margin-bottom: 0 !important;
`,We=(0,s.iK)(He.Z.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,Ge=({db:e,onSSHTunnelParametersChange:t,setSSHTunnelLoginMethod:a})=>{var n,l,o,i,r,s;const[c,p]=(0,u.useState)(it.Password);return(0,N.tZ)($e.l0,null,(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24,md:12},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"server_address",required:!0},(0,d.t)("SSH Host")),(0,N.tZ)(ze.II,{name:"server_address",type:"text",placeholder:(0,d.t)("e.g. 127.0.0.1"),value:(null==e||null==(n=e.ssh_tunnel)?void 0:n.server_address)||"",onChange:t}))),(0,N.tZ)(g.JX,{xs:24,md:12},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"server_port",required:!0},(0,d.t)("SSH Port")),(0,N.tZ)(ze.II,{name:"server_port",type:"text",placeholder:(0,d.t)("22"),value:(null==e||null==(l=e.ssh_tunnel)?void 0:l.server_port)||"",onChange:t})))),(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"username",required:!0},(0,d.t)("Username")),(0,N.tZ)(ze.II,{name:"username",type:"text",placeholder:(0,d.t)("e.g. Analytics"),value:(null==e||null==(o=e.ssh_tunnel)?void 0:o.username)||"",onChange:t})))),(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"use_password",required:!0},(0,d.t)("Login with")),(0,N.tZ)(Ve,{name:"use_password",initialValue:c},(0,N.tZ)(Re.Y.Group,{onChange:({target:{value:e}})=>{p(e),a(e)}},(0,N.tZ)(Re.Y,{value:it.Password},(0,d.t)("Password")),(0,N.tZ)(Re.Y,{value:it.PrivateKey},(0,d.t)("Private Key & Password"))))))),c===it.Password&&(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"password",required:!0},(0,d.t)("SSH Password")),(0,N.tZ)(We,{name:"password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(i=e.ssh_tunnel)?void 0:i.password)||"",onChange:t,iconRender:e=>e?(0,N.tZ)(Ke.Z,{title:"Hide password."},(0,N.tZ)(je.Z,null)):(0,N.tZ)(Ke.Z,{title:"Show password."},(0,N.tZ)(Be.Z,null)),role:"textbox"})))),c===it.PrivateKey&&(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"private_key",required:!0},(0,d.t)("Private Key")),(0,N.tZ)(ze.Kx,{name:"private_key",placeholder:(0,d.t)("Paste Private Key here"),value:(null==e||null==(r=e.ssh_tunnel)?void 0:r.private_key)||"",onChange:t,rows:4})))),(0,N.tZ)(Qe,{gutter:16},(0,N.tZ)(g.JX,{xs:24},(0,N.tZ)(Je,null,(0,N.tZ)($e.lX,{htmlFor:"private_key_password",required:!0},(0,d.t)("Private Key Password")),(0,N.tZ)(We,{name:"private_key_password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(s=e.ssh_tunnel)?void 0:s.private_key_password)||"",onChange:t,iconRender:e=>e?(0,N.tZ)(Ke.Z,{title:"Hide password."},(0,N.tZ)(je.Z,null)):(0,N.tZ)(Ke.Z,{title:"Show password."},(0,N.tZ)(Be.Z,null)),role:"textbox"}))))))},Xe=({isEditMode:e,dbFetched:t,useSSHTunneling:a,setUseSSHTunneling:n,setDB:l,isSSHTunneling:o})=>o?(0,N.tZ)("div",{css:e=>Y(e)},(0,N.tZ)(g.KU,{disabled:e&&!i()(null==t?void 0:t.ssh_tunnel),checked:a,onChange:e=>{n(e),e||l({type:ot.RemoveSSHTunnelConfig})}}),(0,N.tZ)("span",{css:ee},(0,d.t)("SSH Tunnel")),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"})):null,Ye=(0,r.I)(),et=JSON.stringify({allows_virtual_table_explore:!0}),tt={[D.GSheet]:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},at=(0,s.iK)(m.ZP)`
  .ant-tabs-content {
    display: flex;
    width: 100%;
    overflow: inherit;

    & > .ant-tabs-tabpane {
      position: relative;
    }
  }
`,nt=s.iK.div`
  ${({theme:e})=>`\n    margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;\n  `};
`,lt=s.iK.div`
  ${({theme:e})=>`\n    padding: 0px ${4*e.gridUnit}px;\n  `};
`;var ot,it;!function(e){e[e.AddTableCatalogSheet=0]="AddTableCatalogSheet",e[e.ConfigMethodChange=1]="ConfigMethodChange",e[e.DbSelected=2]="DbSelected",e[e.EditorChange=3]="EditorChange",e[e.ExtraEditorChange=4]="ExtraEditorChange",e[e.ExtraInputChange=5]="ExtraInputChange",e[e.Fetched=6]="Fetched",e[e.InputChange=7]="InputChange",e[e.ParametersChange=8]="ParametersChange",e[e.QueryChange=9]="QueryChange",e[e.RemoveTableCatalogSheet=10]="RemoveTableCatalogSheet",e[e.Reset=11]="Reset",e[e.TextChange=12]="TextChange",e[e.ParametersSSHTunnelChange=13]="ParametersSSHTunnelChange",e[e.SetSSHTunnelLoginMethod=14]="SetSSHTunnelLoginMethod",e[e.RemoveSSHTunnelConfig=15]="RemoveSSHTunnelConfig"}(ot||(ot={})),function(e){e[e.Password=0]="Password",e[e.PrivateKey=1]="PrivateKey"}(it||(it={}));const rt=s.iK.div`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  margin-left: ${({theme:e})=>3*e.gridUnit}px;
`;function st(e,t){var a,n,o,i;const r={...e||{}};let s,d,c={},u="";const p=JSON.parse(r.extra||"{}");switch(t.type){case ot.ExtraEditorChange:try{d=JSON.parse(t.payload.json||"{}")}catch(e){d=t.payload.json}return{...r,extra:JSON.stringify({...p,[t.payload.name]:d})};case ot.ExtraInputChange:return"schema_cache_timeout"===t.payload.name||"table_cache_timeout"===t.payload.name?{...r,extra:JSON.stringify({...p,metadata_cache_timeout:{...null==p?void 0:p.metadata_cache_timeout,[t.payload.name]:t.payload.value}})}:"schemas_allowed_for_file_upload"===t.payload.name?{...r,extra:JSON.stringify({...p,schemas_allowed_for_file_upload:(t.payload.value||"").split(",").filter((e=>""!==e))})}:"http_path"===t.payload.name?{...r,extra:JSON.stringify({...p,engine_params:{connect_args:{[t.payload.name]:null==(h=t.payload.value)?void 0:h.trim()}}})}:"expand_rows"===t.payload.name?{...r,extra:JSON.stringify({...p,schema_options:{...null==p?void 0:p.schema_options,[t.payload.name]:!!t.payload.value}})}:{...r,extra:JSON.stringify({...p,[t.payload.name]:"checkbox"===t.payload.type?t.payload.checked:t.payload.value})};var h;case ot.InputChange:return"checkbox"===t.payload.type?{...r,[t.payload.name]:t.payload.checked}:{...r,[t.payload.name]:t.payload.value};case ot.ParametersChange:if(null!=(a=t.payload.type)&&a.startsWith("catalog")&&void 0!==r.catalog){var m;const e=[...r.catalog],a=null==(m=t.payload.type)?void 0:m.split("-")[1],n=e[a]||{};return n[t.payload.name]=t.payload.value,e.splice(parseInt(a,10),1,n),s=e.reduce(((e,t)=>{const a={...e};return a[t.name]=t.value,a}),{}),{...r,catalog:e,parameters:{...r.parameters,catalog:s}}}return{...r,parameters:{...r.parameters,[t.payload.name]:t.payload.value}};case ot.ParametersSSHTunnelChange:return{...r,ssh_tunnel:{...r.ssh_tunnel,[t.payload.name]:t.payload.value}};case ot.SetSSHTunnelLoginMethod:{let e={};var g,v,b;return null!=r&&r.ssh_tunnel&&(e=l()(r.ssh_tunnel,["id","server_address","server_port","username"])),t.payload.login_method===it.PrivateKey?{...r,ssh_tunnel:{private_key:null==r||null==(g=r.ssh_tunnel)?void 0:g.private_key,private_key_password:null==r||null==(v=r.ssh_tunnel)?void 0:v.private_key_password,...e}}:t.payload.login_method===it.Password?{...r,ssh_tunnel:{password:null==r||null==(b=r.ssh_tunnel)?void 0:b.password,...e}}:{...r}}case ot.RemoveSSHTunnelConfig:return{...r,ssh_tunnel:void 0};case ot.AddTableCatalogSheet:return void 0!==r.catalog?{...r,catalog:[...r.catalog,{name:"",value:""}]}:{...r,catalog:[{name:"",value:""}]};case ot.RemoveTableCatalogSheet:return null==(n=r.catalog)||n.splice(t.payload.indexToDelete,1),{...r};case ot.EditorChange:return{...r,[t.payload.name]:t.payload.json};case ot.QueryChange:return{...r,parameters:{...r.parameters,query:Object.fromEntries(new URLSearchParams(t.payload.value))},query_input:t.payload.value};case ot.TextChange:return{...r,[t.payload.name]:t.payload.value};case ot.Fetched:if(c=(null==(o=t.payload)||null==(i=o.parameters)?void 0:i.query)||{},u=Object.entries(c).map((([e,t])=>`${e}=${t}`)).join("&"),t.payload.masked_encrypted_extra&&t.payload.configuration_method===P.DynamicForm){var y;const e=null==(y={...JSON.parse(t.payload.extra||"{}")}.engine_params)?void 0:y.catalog,a=Object.entries(e||{}).map((([e,t])=>({name:e,value:t})));return{...t.payload,engine:t.payload.backend||r.engine,configuration_method:t.payload.configuration_method,catalog:a,parameters:{...t.payload.parameters||r.parameters,catalog:e},query_input:u}}return{...t.payload,masked_encrypted_extra:t.payload.masked_encrypted_extra||"",engine:t.payload.backend||r.engine,configuration_method:t.payload.configuration_method,parameters:t.payload.parameters||r.parameters,ssh_tunnel:t.payload.ssh_tunnel||r.ssh_tunnel,query_input:u};case ot.DbSelected:return{...t.payload,extra:et,expose_in_sqllab:!0};case ot.ConfigMethodChange:return{...t.payload};case ot.Reset:default:return null}}const dt=(0,q.ZP)((({addDangerToast:e,addSuccessToast:t,onDatabaseAdd:a,onHide:n,show:l,databaseId:o,dbEngine:r})=>{var s,f,Z,x,_;const[w,C]=(0,u.useReducer)(st,null),{state:{loading:S,resource:$,error:k},fetchResource:E,createResource:U,updateResource:T,clearError:M}=(0,R.LE)("database",(0,d.t)("database"),e,"connection"),[q,K]=(0,u.useState)("1"),[j,B]=(0,R.cb)(),[J,Q,V]=(0,R.h1)(),[W,ee]=(0,u.useState)(!1),[re,se]=(0,u.useState)(!1),[de,ce]=(0,u.useState)(""),[ge,ve]=(0,u.useState)(!1),[be,xe]=(0,u.useState)(!1),[Ce,$e]=(0,u.useState)(!1),[ke,Ne]=(0,u.useState)({}),[Ee,Ue]=(0,u.useState)({}),[Te,Me]=(0,u.useState)({}),[Ae,Pe]=(0,u.useState)({}),[De,qe]=(0,u.useState)(!1),[Ie,Re]=(0,u.useState)([]),[ze,He]=(0,u.useState)(!1),[Ke,je]=(0,u.useState)(),[Be,Je]=(0,u.useState)([]),[Qe,Ve]=(0,u.useState)([]),[We,et]=(0,u.useState)([]),[it,dt]=(0,u.useState)([]),[ct,ut]=(0,u.useState)({}),pt=null!=(s=Ye.get("ssh_tunnel.form.switch"))?s:Xe,[ht,mt]=(0,u.useState)(!1);let gt=Ye.get("databaseconnection.extraOption");gt&&(gt={...gt,onEdit:e=>{ut({...ct,...e})}});const vt=(0,z.c)(),bt=(0,R.rM)(),yt=(0,R.jb)(),ft=!!o,Zt=null==j||null==(f=j.databases)||null==(Z=f.find((e=>e.backend===(null==w?void 0:w.engine)||e.engine===(null==w?void 0:w.engine))))||null==(x=Z.engine_information)?void 0:x.disable_ssh_tunneling,xt=(0,c.cr)(c.TT.SshTunneling)&&!Zt,_t=yt||!(null==w||!w.engine||!tt[w.engine]),wt=(null==w?void 0:w.configuration_method)===P.SqlalchemyUri,Ct=ft||wt,St=J||k,$t=(0,p.k6)(),kt=(null==j||null==(_=j.databases)?void 0:_.find((e=>e.engine===(ft?null==w?void 0:w.backend:null==w?void 0:w.engine))))||{},Nt=e=>{if("database"===e)return(0,d.t)("e.g. world_population")},Et=()=>{C({type:ot.Reset}),ee(!1),V(null),M(),ve(!1),Re([]),He(!1),je(""),Je([]),Ve([]),et([]),dt([]),Ne({}),Ue({}),Me({}),Pe({}),qe(!1),mt(!1),n()},Ut=e=>{$t.push(e)},{state:{alreadyExists:Tt,passwordsNeeded:Mt,sshPasswordNeeded:At,sshPrivateKeyNeeded:Pt,sshPrivateKeyPasswordNeeded:Dt,loading:Lt,failed:qt},importResource:Ot}=(0,R.PW)("database",(0,d.t)("database"),(e=>{je(e)})),It=(e,t)=>{C({type:e,payload:t})},Ft=async()=>{var n,l;let o;if(null==(n=gt)||n.onSave(ct,w).then((({error:t})=>{t&&(o=t,e(t))})),o)return void xe(!1);const r={...w||{}};if(r.configuration_method===P.DynamicForm){var s,c;if(null!=r&&null!=(s=r.parameters)&&s.catalog&&(r.extra=JSON.stringify({...JSON.parse(r.extra||"{}"),engine_params:{catalog:r.parameters.catalog}})),null==r||!r.ssh_tunnel){xe(!0);const e=await Q(r,!0);if(J&&!i()(J)||e)return void xe(!1);xe(!1)}const e=ft?null==(c=r.parameters_schema)?void 0:c.properties:null==kt?void 0:kt.parameters.properties,t=JSON.parse(r.masked_encrypted_extra||"{}");Object.keys(e||{}).forEach((a=>{var n,l,o,i;e[a]["x-encrypted-extra"]&&null!=(n=r.parameters)&&n[a]&&("object"==typeof(null==(l=r.parameters)?void 0:l[a])?(t[a]=null==(o=r.parameters)?void 0:o[a],r.parameters[a]=JSON.stringify(r.parameters[a])):t[a]=JSON.parse((null==(i=r.parameters)?void 0:i[a])||"{}"))})),r.masked_encrypted_extra=JSON.stringify(t),r.engine===D.GSheet&&(r.impersonate_user=!0)}if(null!=r&&null!=(l=r.parameters)&&l.catalog&&(r.extra=JSON.stringify({...JSON.parse(r.extra||"{}"),engine_params:{catalog:r.parameters.catalog}})),xe(!0),null!=w&&w.id){if(await T(w.id,r,r.configuration_method===P.DynamicForm)){var u;if(a&&a(),null==(u=gt)||u.onSave(ct,w).then((({error:t})=>{t&&(o=t,e(t))})),o)return void xe(!1);ge||(Et(),t((0,d.t)("Database settings updated")))}}else if(w){if(await U(r,r.configuration_method===P.DynamicForm)){var p;if(ee(!0),a&&a(),null==(p=gt)||p.onSave(ct,w).then((({error:t})=>{t&&(o=t,e(t))})),o)return void xe(!1);Ct&&(Et(),t((0,d.t)("Database connected")))}}else{if(He(!0),!(Ie[0].originFileObj instanceof File))return;await Ot(Ie[0].originFileObj,ke,Ee,Te,Ae,De)&&(a&&a(),Et(),t((0,d.t)("Database connected")))}se(!0),ve(!1),xe(!1)},Rt=e=>{if("Other"===e)C({type:ot.DbSelected,payload:{database_name:e,configuration_method:P.SqlalchemyUri,engine:void 0,engine_information:{supports_file_upload:!0}}});else{const t=null==j?void 0:j.databases.filter((t=>t.name===e))[0],{engine:a,parameters:n,engine_information:l,default_driver:o,sqlalchemy_uri_placeholder:i}=t,r=void 0!==n;C({type:ot.DbSelected,payload:{database_name:e,engine:a,configuration_method:r?P.DynamicForm:P.SqlalchemyUri,engine_information:l,driver:o,sqlalchemy_uri_placeholder:i}}),a===D.GSheet&&C({type:ot.AddTableCatalogSheet})}},zt=()=>{$&&E($.id),se(!1),ve(!0)},Ht=()=>{ge&&ee(!1),ze&&He(!1),qt&&(He(!1),je(""),Je([]),Ve([]),et([]),dt([]),Ne({}),Ue({}),Me({}),Pe({})),C({type:ot.Reset}),Re([])},Kt=()=>w?!W||ge?(0,N.tZ)(u.Fragment,null,(0,N.tZ)(fe,{key:"back",onClick:Ht},(0,d.t)("Back")),(0,N.tZ)(fe,{key:"submit",buttonStyle:"primary",onClick:Ft,loading:be},(0,d.t)("Connect"))):(0,N.tZ)(u.Fragment,null,(0,N.tZ)(fe,{key:"back",onClick:zt},(0,d.t)("Back")),(0,N.tZ)(fe,{key:"submit",buttonStyle:"primary",onClick:Ft,loading:be},(0,d.t)("Finish"))):ze?(0,N.tZ)(u.Fragment,null,(0,N.tZ)(fe,{key:"back",onClick:Ht},(0,d.t)("Back")),(0,N.tZ)(fe,{key:"submit",buttonStyle:"primary",onClick:Ft,disabled:!!(Lt||Tt.length&&!De||Mt.length&&"{}"===JSON.stringify(ke)||At.length&&"{}"===JSON.stringify(Ee)||Pt.length&&"{}"===JSON.stringify(Te)||Dt.length&&"{}"===JSON.stringify(Ae)),loading:be},(0,d.t)("Connect"))):(0,N.tZ)(u.Fragment,null),jt=(0,u.useRef)(!0);(0,u.useEffect)((()=>{jt.current?jt.current=!1:Lt||Tt.length||Mt.length||At.length||Pt.length||Dt.length||be||qt||(Et(),t((0,d.t)("Database connected")))}),[Tt,Mt,Lt,qt,At,Pt,Dt]),(0,u.useEffect)((()=>{l&&(K("1"),xe(!0),B()),o&&l&&ft&&o&&(S||E(o).catch((t=>e((0,d.t)("Sorry there was an error fetching database information: %s",t.message)))))}),[l,o]),(0,u.useEffect)((()=>{$&&(C({type:ot.Fetched,payload:$}),ce($.database_name))}),[$]),(0,u.useEffect)((()=>{be&&xe(!1),j&&r&&Rt(r)}),[j]),(0,u.useEffect)((()=>{ze&&document.getElementsByClassName("ant-upload-list-item-name")[0].scrollIntoView()}),[ze]),(0,u.useEffect)((()=>{Je([...Mt])}),[Mt]),(0,u.useEffect)((()=>{Ve([...At])}),[At]),(0,u.useEffect)((()=>{et([...Pt])}),[Pt]),(0,u.useEffect)((()=>{dt([...Dt])}),[Dt]),(0,u.useEffect)((()=>{w&&xt&&mt(!i()(null==w?void 0:w.ssh_tunnel))}),[w,xt]);const Bt=()=>Ke?(0,N.tZ)(le,null,(0,N.tZ)(F.Z,{errorMessage:Ke,showDbInstallInstructions:Be.length>0})):null,Jt=e=>{var t,a;const n=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";qe(n.toUpperCase()===(0,d.t)("OVERWRITE"))},Qt=()=>{let e=[];var t;return i()(k)?i()(J)||"GENERIC_DB_ENGINE_ERROR"!==(null==J?void 0:J.error_type)||(e=[(null==J?void 0:J.description)||(null==J?void 0:J.message)]):e="object"==typeof k?Object.values(k):"string"==typeof k?[k]:[],e.length?(0,N.tZ)(nt,null,(0,N.tZ)(I.Z,{title:(0,d.t)("Database Creation Error"),description:(0,d.t)('We are unable to connect to your database. Click "See more" for database-provided information that may help troubleshoot the issue.'),subtitle:(null==(t=e)?void 0:t[0])||(null==J?void 0:J.description),copyText:null==J?void 0:J.description})):(0,N.tZ)(u.Fragment,null)},Vt=()=>{xe(!0),E(null==$?void 0:$.id).then((e=>{(0,h.LS)(h.dR.Database,e)}))},Wt=()=>(0,N.tZ)(Ge,{db:w,onSSHTunnelParametersChange:({target:e})=>It(ot.ParametersSSHTunnelChange,{type:e.type,name:e.name,value:e.value}),setSSHTunnelLoginMethod:e=>C({type:ot.SetSSHTunnelLoginMethod,payload:{login_method:e}})}),Gt=()=>{var e;return(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Le,{isEditMode:ft,db:w,sslForced:!1,dbModel:kt,onAddTableCatalog:()=>{C({type:ot.AddTableCatalogSheet})},onQueryChange:({target:e})=>It(ot.QueryChange,{name:e.name,value:e.value}),onExtraInputChange:({target:e})=>It(ot.ExtraInputChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{C({type:ot.RemoveTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:({target:e})=>It(ot.ParametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>It(ot.TextChange,{name:e.name,value:e.value}),getValidation:()=>Q(w),validationErrors:J,getPlaceholder:Nt,clearValidationErrors:()=>V(null)}),(null==w||null==(e=w.parameters)?void 0:e.ssh)&&(0,N.tZ)(lt,null,Wt()))};if(Ie.length>0&&(Tt.length||Be.length||Qe.length||We.length||it.length))return(0,N.tZ)(b.default,{css:e=>[X,ae(e),oe(e),ie(e)],name:"database",onHandledPrimaryAction:Ft,onHide:Et,primaryButtonName:(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,N.tZ)("h4",null,(0,d.t)("Connect a database")),footer:Kt()},(0,N.tZ)(Fe,{isLoading:be,isEditMode:ft,useSqlAlchemyForm:wt,hasConnectedDb:W,db:w,dbName:de,dbModel:kt,fileList:Ie}),Be.length||Qe.length||We.length||it.length?[...new Set([...Be,...Qe,...We,...it])].map((e=>(0,N.tZ)(u.Fragment,null,(0,N.tZ)(le,null,(0,N.tZ)(v.Z,{closable:!1,css:e=>ne(e),type:"info",showIcon:!0,message:"Database passwords",description:(0,d.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in explore files and should be added manually after the import if they are needed.')})),(null==Be?void 0:Be.indexOf(e))>=0&&(0,N.tZ)(O.Z,{id:"password_needed",name:"password_needed",required:!0,value:ke[e],onChange:t=>Ne({...ke,[e]:t.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==J?void 0:J.password_needed,label:(0,d.t)("%s PASSWORD",e.slice(10)),css:te}),(null==Qe?void 0:Qe.indexOf(e))>=0&&(0,N.tZ)(O.Z,{id:"ssh_tunnel_password_needed",name:"ssh_tunnel_password_needed",required:!0,value:Ee[e],onChange:t=>Ue({...Ee,[e]:t.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==J?void 0:J.ssh_tunnel_password_needed,label:(0,d.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),css:te}),(null==We?void 0:We.indexOf(e))>=0&&(0,N.tZ)(O.Z,{id:"ssh_tunnel_private_key_needed",name:"ssh_tunnel_private_key_needed",required:!0,value:Te[e],onChange:t=>Me({...Te,[e]:t.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==J?void 0:J.ssh_tunnel_private_key_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),css:te}),(null==it?void 0:it.indexOf(e))>=0&&(0,N.tZ)(O.Z,{id:"ssh_tunnel_private_key_password_needed",name:"ssh_tunnel_private_key_password_needed",required:!0,value:Ae[e],onChange:t=>Pe({...Ae,[e]:t.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==J?void 0:J.ssh_tunnel_private_key_password_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),css:te})))):null,Tt.length?(0,N.tZ)(u.Fragment,null,(0,N.tZ)(le,null,(0,N.tZ)(v.Z,{closable:!1,css:e=>(e=>N.iv`
  border: 1px solid ${e.colors.warning.light1};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;
  color: ${e.colors.warning.dark2};

  .ant-alert-message {
    margin: 0;
  }

  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),type:"warning",showIcon:!0,message:"",description:(0,d.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?")})),(0,N.tZ)(O.Z,{id:"confirm_overwrite",name:"confirm_overwrite",required:!0,validationMethods:{onBlur:()=>{}},errorMessage:null==J?void 0:J.confirm_overwrite,label:(0,d.t)('Type "%s" to confirm',(0,d.t)("OVERWRITE")),onChange:Jt,css:te})):null,Bt());const Xt=ft?(e=>(0,N.tZ)(u.Fragment,null,(0,N.tZ)(fe,{key:"close",onClick:Et},(0,d.t)("Close")),(0,N.tZ)(fe,{key:"submit",buttonStyle:"primary",onClick:Ft,disabled:null==e?void 0:e.is_managed_externally,loading:be,tooltip:null!=e&&e.is_managed_externally?(0,d.t)("This database is managed externally, and can't be edited in Superset"):""},(0,d.t)("Finish"))))(w):Kt();return Ct?(0,N.tZ)(b.default,{css:e=>[G,X,ae(e),oe(e),ie(e)],name:"database",onHandledPrimaryAction:Ft,onHide:Et,primaryButtonName:ft?(0,d.t)("Save"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,N.tZ)("h4",null,ft?(0,d.t)("Edit database"):(0,d.t)("Connect a database")),footer:Xt},(0,N.tZ)(Ze,null,(0,N.tZ)(me,null,(0,N.tZ)(Fe,{isLoading:be,isEditMode:ft,useSqlAlchemyForm:wt,hasConnectedDb:W,db:w,dbName:de,dbModel:kt}))),(0,N.tZ)(at,{defaultActiveKey:"1",activeKey:q,onTabClick:e=>K(e),animated:{inkBar:!0,tabPane:!0}},(0,N.tZ)(m.ZP.TabPane,{tab:(0,N.tZ)("span",null,(0,d.t)("Basic")),key:"1"},wt?(0,N.tZ)(ue,null,(0,N.tZ)(Se,{db:w,onInputChange:({target:e})=>It(ot.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:vt,testConnection:()=>{var a;if(null==w||!w.sqlalchemy_uri)return void e((0,d.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==w?void 0:w.sqlalchemy_uri)||"",database_name:(null==w||null==(a=w.database_name)?void 0:a.trim())||void 0,impersonate_user:(null==w?void 0:w.impersonate_user)||void 0,extra:null==w?void 0:w.extra,masked_encrypted_extra:(null==w?void 0:w.masked_encrypted_extra)||"",server_cert:(null==w?void 0:w.server_cert)||void 0,ssh_tunnel:(null==w?void 0:w.ssh_tunnel)||void 0};$e(!0),(0,R.xx)(n,(t=>{$e(!1),e(t)}),(e=>{$e(!1),t(e)}))},testInProgress:Ce},(0,N.tZ)(pt,{isEditMode:ft,dbFetched:$,disableSSHTunnelingForEngine:Zt,useSSHTunneling:ht,setUseSSHTunneling:mt,setDB:C,isSSHTunneling:xt}),ht&&Wt()),(ea=(null==w?void 0:w.backend)||(null==w?void 0:w.engine),void 0!==(null==j||null==(ta=j.databases)||null==(aa=ta.find((e=>e.backend===ea||e.engine===ea)))?void 0:aa.parameters)&&!ft&&(0,N.tZ)("div",{css:e=>Y(e)},(0,N.tZ)(y.Z,{buttonStyle:"link",onClick:()=>C({type:ot.ConfigMethodChange,payload:{database_name:null==w?void 0:w.database_name,configuration_method:P.DynamicForm,engine:null==w?void 0:w.engine}}),css:e=>(e=>N.iv`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e)},(0,d.t)("Connect this database using the dynamic form instead")),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})))):Gt(),!ft&&(0,N.tZ)(le,null,(0,N.tZ)(v.Z,{closable:!1,css:e=>ne(e),message:(0,d.t)("Additional fields may be required"),showIcon:!0,description:(0,N.tZ)(u.Fragment,null,(0,d.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,N.tZ)("a",{href:Oe,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},(0,d.t)("here")),"."),type:"info"})),St&&Qt()),(0,N.tZ)(m.ZP.TabPane,{tab:(0,N.tZ)("span",null,(0,d.t)("Advanced")),key:"2"},(0,N.tZ)(we,{extraExtension:gt,db:w,onInputChange:({target:e})=>It(ot.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>It(ot.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>It(ot.EditorChange,e),onExtraInputChange:({target:e})=>{It(ot.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{It(ot.ExtraEditorChange,e)}})))):(0,N.tZ)(b.default,{css:e=>[X,ae(e),oe(e),ie(e)],name:"database",onHandledPrimaryAction:Ft,onHide:Et,primaryButtonName:W?(0,d.t)("Finish"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,N.tZ)("h4",null,(0,d.t)("Connect a database")),footer:Kt()},!be&&W?(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Fe,{isLoading:be,isEditMode:ft,useSqlAlchemyForm:wt,hasConnectedDb:W,db:w,dbName:de,dbModel:kt,editNewDb:ge}),re&&(0,N.tZ)(rt,null,(0,N.tZ)(y.Z,{buttonStyle:"secondary",onClick:()=>{xe(!0),Vt(),Ut("/dataset/add/")}},(0,d.t)("CREATE DATASET")),(0,N.tZ)(y.Z,{buttonStyle:"secondary",onClick:()=>{xe(!0),Vt(),Ut("/sqllab?db=true")}},(0,d.t)("QUERY DATA IN SQL LAB"))),ge?Gt():(0,N.tZ)(we,{extraExtension:gt,db:w,onInputChange:({target:e})=>It(ot.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>It(ot.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>It(ot.EditorChange,e),onExtraInputChange:({target:e})=>{It(ot.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>It(ot.ExtraEditorChange,e)})):(0,N.tZ)(u.Fragment,null,!be&&(w?(0,N.tZ)(u.Fragment,null,(0,N.tZ)(Fe,{isLoading:be,isEditMode:ft,useSqlAlchemyForm:wt,hasConnectedDb:W,db:w,dbName:de,dbModel:kt}),_t&&(()=>{var e,t,a,n,l;const{hostname:o}=window.location;let i=(null==yt||null==(e=yt.REGIONAL_IPS)?void 0:e.default)||"";const r=(null==yt?void 0:yt.REGIONAL_IPS)||{};return Object.entries(r).forEach((([e,t])=>{const a=new RegExp(e);o.match(a)&&(i=t)})),(null==w?void 0:w.engine)&&(0,N.tZ)(le,null,(0,N.tZ)(v.Z,{closable:!1,css:e=>ne(e),type:"info",showIcon:!0,message:(null==(t=tt[w.engine])?void 0:t.message)||(null==yt||null==(a=yt.DEFAULT)?void 0:a.message),description:(null==(n=tt[w.engine])?void 0:n.description)||(null==yt||null==(l=yt.DEFAULT)?void 0:l.description)+i}))})(),Gt(),(0,N.tZ)("div",{css:e=>Y(e)},kt.engine!==D.GSheet&&(0,N.tZ)(u.Fragment,null,(0,N.tZ)(y.Z,{buttonStyle:"link",onClick:()=>C({type:ot.ConfigMethodChange,payload:{engine:w.engine,configuration_method:P.SqlalchemyUri,database_name:w.database_name}}),css:pe},(0,d.t)("Connect this database with a SQLAlchemy URI string instead")),(0,N.tZ)(L.Z,{tooltip:(0,d.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"}))),St&&Qt()):(0,N.tZ)(ye,null,(0,N.tZ)(Fe,{isLoading:be,isEditMode:ft,useSqlAlchemyForm:wt,hasConnectedDb:W,db:w,dbName:de,dbModel:kt}),(0,N.tZ)("div",{className:"preferred"},null==j||null==(Yt=j.databases)?void 0:Yt.filter((e=>e.preferred)).map((e=>(0,N.tZ)(A,{className:"preferred-item",onClick:()=>Rt(e.name),buttonText:e.name,icon:null==bt?void 0:bt[e.engine],key:`${e.name}`})))),(()=>{var e,t;return(0,N.tZ)("div",{className:"available"},(0,N.tZ)("h4",{className:"available-label"},(0,d.t)("Or choose from a list of other databases we support:")),(0,N.tZ)("div",{className:"control-label"},(0,d.t)("Supported databases")),(0,N.tZ)(g.IZ,{className:"available-select",onChange:Rt,placeholder:(0,d.t)("Choose a database..."),showSearch:!0},null==(e=[...(null==j?void 0:j.databases)||[]])?void 0:e.sort(((e,t)=>e.name.localeCompare(t.name))).map(((e,t)=>(0,N.tZ)(g.IZ.Option,{value:e.name,key:`database-${t}`},e.name))),(0,N.tZ)(g.IZ.Option,{value:"Other",key:"Other"},(0,d.t)("Other"))),(0,N.tZ)(v.Z,{showIcon:!0,closable:!1,css:e=>ne(e),type:"info",message:(null==yt||null==(t=yt.ADD_DATABASE)?void 0:t.message)||(0,d.t)("Want to add a new database?"),description:null!=yt&&yt.ADD_DATABASE?(0,N.tZ)(u.Fragment,null,(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,N.tZ)("a",{href:null==yt?void 0:yt.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer"},null==yt?void 0:yt.ADD_DATABASE.contact_description_link)," ",null==yt?void 0:yt.ADD_DATABASE.description):(0,N.tZ)(u.Fragment,null,(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,N.tZ)("a",{href:Oe,target:"_blank",rel:"noopener noreferrer"},(0,d.t)("here")),".")}))})(),(0,N.tZ)(_e,null,(0,N.tZ)(g.gq,{name:"databaseFile",id:"databaseFile",accept:".yaml,.json,.yml,.zip",customRequest:()=>{},onChange:async e=>{je(""),Je([]),Ve([]),et([]),dt([]),Ne({}),Ue({}),Me({}),Pe({}),He(!0),Re([{...e.file,status:"done"}]),e.file.originFileObj instanceof File&&await Ot(e.file.originFileObj,ke,Ee,Te,Ae,De)&&(null==a||a())},onRemove:e=>(Re(Ie.filter((t=>t.uid!==e.uid))),!1)},(0,N.tZ)(y.Z,{buttonStyle:"link",type:"link",css:he},(0,d.t)("Import database from file")))),Bt()))),be&&(0,N.tZ)(H.Z,null));var Yt,ea,ta,aa}))},49041:(e,t,a)=>{a.d(t,{Z:()=>le});var n=a(73126),l=a(23279),o=a.n(l),i=a(67294),r=a(51995),s=a(11965),d=a(23525),c=a(4715),u=a(83862),p=a(58593),h=a(16550),m=a(73727),g=a(85931),v=a(70707),b=a(29147),y=a(27600),f=a(41609),Z=a.n(f),x=a(15926),_=a.n(x),w=a(28216),C=a(35755),S=a(75049),$=a(61988),k=a(31069),N=a(37921),E=a(12617),U=a(22318),T=a(1315),M=a(40768);const A=({version:e="unknownVersion",sha:t="unknownSHA",build:a="unknownBuild"})=>{const n=`https://apachesuperset.gateway.scarf.sh/pixel/0d3461e1-abb1-4691-a0aa-5ed50de66af0/${e}/${t}/${a}`;return(0,s.tZ)("img",{referrerPolicy:"no-referrer-when-downgrade",src:n,width:0,height:0,alt:""})},{SubMenu:P}=u.MainNav,D=r.iK.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,L=r.iK.i`
  margin-top: 2px;
`;function q(e){const{locale:t,languages:a,...l}=e;return(0,s.tZ)(P,(0,n.Z)({"aria-label":"Languages",title:(0,s.tZ)("div",{className:"f16"},(0,s.tZ)(L,{className:`flag ${a[t].flag}`})),icon:(0,s.tZ)(v.Z.TriangleDown,null)},l),Object.keys(a).map((e=>(0,s.tZ)(u.MainNav.Item,{key:e,style:{whiteSpace:"normal",height:"auto"}},(0,s.tZ)(D,{className:"f16"},(0,s.tZ)("i",{className:`flag ${a[e].flag}`}),(0,s.tZ)("a",{href:a[e].url},a[e].name))))))}var O=a(39589);const I=(0,S.I)(),F=e=>s.iv`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,R=r.iK.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
`,z=e=>s.iv`
  color: ${e.colors.grayscale.light1};
  .ant-menu-item-active {
    color: ${e.colors.grayscale.light1};
    cursor: default;
  }
`,H=r.iK.div`
  display: flex;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
  .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
`,K=r.iK.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`,j=r.iK.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,B=e=>s.iv`
  color: ${e.colors.grayscale.light5};
`,J=e=>s.iv`
  &:hover {
    color: ${e.colors.primary.base} !important;
    cursor: pointer !important;
  }
`,{SubMenu:Q}=u.MainNav,V=({align:e,settings:t,navbarRight:a,isFrontendRoute:n,environmentTag:l,setQuery:o})=>{const d=(0,w.v9)((e=>e.user)),c=(0,w.v9)((e=>{var t;return null==(t=e.dashboardInfo)?void 0:t.id})),h=d||{},{roles:g}=h,{CSV_EXTENSIONS:b,COLUMNAR_EXTENSIONS:y,EXCEL_EXTENSIONS:f,ALLOWED_EXTENSIONS:x,HAS_GSHEETS_INSTALLED:C}=(0,w.v9)((e=>e.common.conf)),[S,P]=(0,i.useState)(!1),[D,L]=(0,i.useState)(""),V=(0,E.R)("can_sqllab","Superset",g),W=(0,E.R)("can_write","Dashboard",g),G=(0,E.R)("can_write","Chart",g),X=(0,E.R)("can_write","Database",g),Y=(0,E.R)("can_write","Dataset",g),{canUploadData:ee,canUploadCSV:te,canUploadColumnar:ae,canUploadExcel:ne}=(0,M.Mc)(g,b,y,f,x),le=V||G||W,[oe,ie]=(0,i.useState)(!1),[re,se]=(0,i.useState)(!1),de=(0,U.i5)(d),ce=oe||de,ue=[{label:(0,$.t)("Data"),icon:"fa-database",childs:[{label:(0,$.t)("Connect database"),name:O.Z.DbConnection,perm:X&&!re},{label:(0,$.t)("Create dataset"),name:O.Z.DatasetCreation,url:"/dataset/add/",perm:Y&&re},{label:(0,$.t)("Connect Google Sheet"),name:O.Z.GoogleSheets,perm:X&&C},{label:(0,$.t)("Upload CSV to database"),name:"Upload a CSV",url:"/csvtodatabaseview/form",perm:te&&ce,disable:de&&!oe},{label:(0,$.t)("Upload columnar file to database"),name:"Upload a Columnar file",url:"/columnartodatabaseview/form",perm:ae&&ce,disable:de&&!oe},{label:(0,$.t)("Upload Excel file to database"),name:"Upload Excel",url:"/exceltodatabaseview/form",perm:ne&&ce,disable:de&&!oe}]},{label:(0,$.t)("SQL query"),url:"/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,$.t)("Chart"),url:Number.isInteger(c)?`/chart/add?dashboard_id=${c}`:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,$.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],pe=()=>{k.Z.get({endpoint:`/api/v1/database/?q=${_().encode({filters:[{col:"allow_file_upload",opr:"upload_is_enabled",value:!0}]})}`}).then((({json:e})=>{var t;const a=(null==e||null==(t=e.result)?void 0:t.filter((e=>{var t;return null==e||null==(t=e.engine_information)?void 0:t.supports_file_upload})))||[];ie((null==a?void 0:a.length)>=1)}))},he=()=>{k.Z.get({endpoint:`/api/v1/database/?q=${_().encode({filters:[{col:"database_name",opr:"neq",value:"examples"}]})}`}).then((({json:e})=>{se(e.count>=1)}))};(0,i.useEffect)((()=>{ee&&pe()}),[ee]),(0,i.useEffect)((()=>{(X||Y)&&he()}),[X,Y]);const me=e=>(0,s.tZ)(i.Fragment,null,(0,s.tZ)("i",{className:`fa ${e.icon}`}),e.label),ge=(0,$.t)("Enable 'Allow file uploads to database' in any database's settings"),ve=I.get("navbar.right"),be=I.get("navbar.right-menu.item.icon"),ye=(0,r.Fg)();return(0,s.tZ)(H,{align:e},X&&(0,s.tZ)(T.ZP,{onHide:()=>{L(""),P(!1)},show:S,dbEngine:D,onDatabaseAdd:()=>o({databaseAdded:!0})}),(null==l?void 0:l.text)&&(0,s.tZ)(N.Z,{css:(0,s.iv)({borderRadius:125*ye.gridUnit+"px"},"",""),color:/^#(?:[0-9a-f]{3}){1,2}$/i.test(l.color)?l.color:l.color.split(".").reduce(((e,t)=>e[t]),ye.colors)},(0,s.tZ)("span",{css:B},l.text)),(0,s.tZ)(u.MainNav,{selectable:!1,mode:"horizontal",onClick:e=>{e.key===O.Z.DbConnection?P(!0):e.key===O.Z.GoogleSheets&&(P(!0),L("Google Sheets"))},onOpenChange:e=>(e.length>1&&!Z()(null==e?void 0:e.filter((e=>{var t;return e.includes(`sub2_${null==ue||null==(t=ue[0])?void 0:t.label}`)})))&&(ee&&pe(),(X||Y)&&he()),null)},ve&&(0,s.tZ)(ve,null),!a.user_is_anonymous&&le&&(0,s.tZ)(Q,{title:(0,s.tZ)(R,{className:"fa fa-plus"}),icon:(0,s.tZ)(v.Z.TriangleDown,null)},null==ue||null==ue.map?void 0:ue.map((e=>{var t;const a=null==(t=e.childs)?void 0:t.some((e=>"object"==typeof e&&!!e.perm));if(e.childs){var l;if(a)return(0,s.tZ)(Q,{key:`sub2_${e.label}`,className:"data-menu",title:me(e)},null==e||null==(l=e.childs)||null==l.map?void 0:l.map(((e,t)=>"string"!=typeof e&&e.name&&e.perm?(0,s.tZ)(i.Fragment,{key:e.name},3===t&&(0,s.tZ)(u.MainNav.Divider,null),(e=>e.disable?(0,s.tZ)(u.MainNav.Item,{key:e.name,css:z},(0,s.tZ)(p.u,{placement:"top",title:ge},e.label)):(0,s.tZ)(u.MainNav.Item,{key:e.name,css:J},e.url?(0,s.tZ)("a",{href:e.url}," ",e.label," "):e.label))(e)):null)));if(!e.url)return null}return(0,E.R)(e.perm,e.view,g)&&(0,s.tZ)(u.MainNav.Item,{key:e.label},n(e.url)?(0,s.tZ)(m.rU,{to:e.url||""},(0,s.tZ)("i",{className:`fa ${e.icon}`})," ",e.label):(0,s.tZ)("a",{href:e.url},(0,s.tZ)("i",{className:`fa ${e.icon}`})," ",e.label))}))),(0,s.tZ)(Q,{title:(0,$.t)("Settings"),icon:(0,s.tZ)(v.Z.TriangleDown,{iconSize:"xl"})},null==t||null==t.map?void 0:t.map(((e,a)=>{var l;return[(0,s.tZ)(u.MainNav.ItemGroup,{key:`${e.label}`,title:e.label},null==e||null==(l=e.childs)||null==l.map?void 0:l.map((e=>{if("string"!=typeof e){const t=be?(0,s.tZ)(K,null,e.label,(0,s.tZ)(be,{menuChild:e})):e.label;return(0,s.tZ)(u.MainNav.Item,{key:`${e.label}`},n(e.url)?(0,s.tZ)(m.rU,{to:e.url||""},t):(0,s.tZ)("a",{href:e.url},t))}return null}))),a<t.length-1&&(0,s.tZ)(u.MainNav.Divider,{key:`divider_${a}`})]})),!a.user_is_anonymous&&[(0,s.tZ)(u.MainNav.Divider,{key:"user-divider"}),(0,s.tZ)(u.MainNav.ItemGroup,{key:"user-section",title:(0,$.t)("User")},a.user_info_url&&(0,s.tZ)(u.MainNav.Item,{key:"info"},(0,s.tZ)("a",{href:a.user_info_url},(0,$.t)("Info"))),(0,s.tZ)(u.MainNav.Item,{key:"logout"},(0,s.tZ)("a",{href:a.user_logout_url},(0,$.t)("Logout"))))],(a.version_string||a.version_sha)&&[(0,s.tZ)(u.MainNav.Divider,{key:"version-info-divider"}),(0,s.tZ)(u.MainNav.ItemGroup,{key:"about-section",title:(0,$.t)("About")},(0,s.tZ)("div",{className:"about-section"},a.show_watermark&&(0,s.tZ)("div",{css:F},(0,$.t)("Powered by Apache Superset")),a.version_string&&(0,s.tZ)("div",{css:F},(0,$.t)("Version"),": ",a.version_string),a.version_sha&&(0,s.tZ)("div",{css:F},(0,$.t)("SHA"),": ",a.version_sha),a.build_number&&(0,s.tZ)("div",{css:F},(0,$.t)("Build"),": ",a.build_number)))]),a.show_language_picker&&(0,s.tZ)(q,{locale:a.locale,languages:a.languages})),a.documentation_url&&(0,s.tZ)(i.Fragment,null,(0,s.tZ)(j,{href:a.documentation_url,target:"_blank",rel:"noreferrer",title:a.documentation_text||(0,$.t)("Documentation")},a.documentation_icon?(0,s.tZ)("i",{className:a.documentation_icon}):(0,s.tZ)("i",{className:"fa fa-question"})),(0,s.tZ)("span",null," ")),a.bug_report_url&&(0,s.tZ)(i.Fragment,null,(0,s.tZ)(j,{href:a.bug_report_url,target:"_blank",rel:"noreferrer",title:a.bug_report_text||(0,$.t)("Report a bug")},a.bug_report_icon?(0,s.tZ)("i",{className:a.bug_report_icon}):(0,s.tZ)("i",{className:"fa fa-bug"})),(0,s.tZ)("span",null," ")),a.user_is_anonymous&&(0,s.tZ)(j,{href:a.user_login_url},(0,s.tZ)("i",{className:"fa fa-fw fa-sign-in"}),(0,$.t)("Login")),(0,s.tZ)(A,{version:a.version_string,sha:a.version_sha,build:a.build_number}))},W=e=>{const[,t]=(0,C.Kx)({databaseAdded:C.dJ,datasetAdded:C.dJ});return(0,s.tZ)(V,(0,n.Z)({setQuery:t},e))};class G extends i.PureComponent{constructor(...e){super(...e),this.state={hasError:!1},this.noop=()=>{}}static getDerivedStateFromError(){return{hasError:!0}}render(){return this.state.hasError?(0,s.tZ)(V,(0,n.Z)({setQuery:this.noop},this.props)):this.props.children}}const X=e=>(0,s.tZ)(G,e,(0,s.tZ)(W,e)),Y=r.iK.header`
  ${({theme:e})=>`\n      background-color: ${e.colors.grayscale.light5};\n      margin-bottom: 2px;\n      z-index: 10;\n\n      &:nth-last-of-type(2) nav {\n        margin-bottom: 2px;\n      }\n      .caret {\n        display: none;\n      }\n      .navbar-brand {\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        /* must be exactly the height of the Antd navbar */\n        min-height: 50px;\n        padding: ${e.gridUnit}px\n          ${2*e.gridUnit}px\n          ${e.gridUnit}px\n          ${4*e.gridUnit}px;\n        max-width: ${e.gridUnit*e.brandIconMaxWidth}px;\n        img {\n          height: 100%;\n          object-fit: contain;\n        }\n      }\n      .navbar-brand-text {\n        border-left: 1px solid ${e.colors.grayscale.light2};\n        border-right: 1px solid ${e.colors.grayscale.light2};\n        height: 100%;\n        color: ${e.colors.grayscale.dark1};\n        padding-left: ${4*e.gridUnit}px;\n        padding-right: ${4*e.gridUnit}px;\n        margin-right: ${6*e.gridUnit}px;\n        font-size: ${4*e.gridUnit}px;\n        float: left;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n\n        span {\n          max-width: ${58*e.gridUnit}px;\n          white-space: nowrap;\n          overflow: hidden;\n          text-overflow: ellipsis;\n        }\n        @media (max-width: 1127px) {\n          display: none;\n        }\n      }\n      .main-nav .ant-menu-submenu-title > svg {\n        top: ${5.25*e.gridUnit}px;\n      }\n      @media (max-width: 767px) {\n        .navbar-brand {\n          float: none;\n        }\n      }\n      .ant-menu-horizontal .ant-menu-item {\n        height: 100%;\n        line-height: inherit;\n      }\n      .ant-menu > .ant-menu-item > a {\n        padding: ${4*e.gridUnit}px;\n      }\n      @media (max-width: 767px) {\n        .ant-menu-item {\n          padding: 0 ${6*e.gridUnit}px 0\n            ${3*e.gridUnit}px !important;\n        }\n        .ant-menu > .ant-menu-item > a {\n          padding: 0px;\n        }\n        .main-nav .ant-menu-submenu-title > svg:nth-of-type(1) {\n          display: none;\n        }\n        .ant-menu-item-active > a {\n          &:hover {\n            color: ${e.colors.primary.base} !important;\n            background-color: transparent !important;\n          }\n        }\n      }\n      .ant-menu-item a {\n        &:hover {\n          color: ${e.colors.grayscale.dark1};\n          background-color: ${e.colors.primary.light5};\n          border-bottom: none;\n          margin: 0;\n          &:after {\n            opacity: 1;\n            width: 100%;\n          }\n        }\n      }\n  `}
`,ee=e=>s.iv`
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light.ant-menu-submenu-placement-bottomLeft {
    border-radius: 0px;
  }
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light {
    border-radius: 0px;
  }
  .ant-menu-vertical > .ant-menu-submenu.data-menu > .ant-menu-submenu-title {
    height: 28px;
    i {
      padding-right: ${2*e.gridUnit}px;
      margin-left: ${1.75*e.gridUnit}px;
    }
  }
  .ant-menu-item-selected {
    background-color: transparent;
    &:not(.ant-menu-item-active) {
      color: inherit;
      border-bottom-color: transparent;
      & > a {
        color: inherit;
      }
    }
  }
  .ant-menu-horizontal > .ant-menu-item:has(> .is-active) {
    color: ${e.colors.primary.base};
    border-bottom-color: ${e.colors.primary.base};
    & > a {
      color: ${e.colors.primary.base};
    }
  }
  .ant-menu-vertical > .ant-menu-item:has(> .is-active) {
    background-color: ${e.colors.primary.light5};
    & > a {
      color: ${e.colors.primary.base};
    }
  }
`,{SubMenu:te}=u.MainNav,{useBreakpoint:ae}=c.Grid;function ne({data:{menu:e,brand:t,navbar_right:a,settings:n,environment_tag:l},isFrontendRoute:f=(()=>!1)}){const[Z,x]=(0,i.useState)("horizontal"),_=ae(),w=(0,b.fG)(),C=(0,r.Fg)();let S;(0,i.useEffect)((()=>{function e(){window.innerWidth<=767?x("inline"):x("horizontal")}e();const t=o()((()=>e()),10);return window.addEventListener("resize",t),()=>window.removeEventListener("resize",t)}),[]),function(e){e.Explore="/explore",e.Dashboard="/dashboard",e.Chart="/chart",e.Datasets="/tablemodelview"}(S||(S={}));const $=[],[k,N]=(0,i.useState)($),E=(0,h.TH)();return(0,i.useEffect)((()=>{const e=E.pathname;switch(!0){case e.startsWith(S.Dashboard):N(["Dashboards"]);break;case e.startsWith(S.Chart)||e.startsWith(S.Explore):N(["Charts"]);break;case e.startsWith(S.Datasets):N(["Datasets"]);break;default:N($)}}),[E.pathname]),(0,d.eY)(y.KD.standalone)||w.hideNav?(0,s.tZ)(i.Fragment,null):(0,s.tZ)(Y,{className:"top",id:"main-menu",role:"navigation"},(0,s.tZ)(s.xB,{styles:ee(C)}),(0,s.tZ)(c.X2,null,(0,s.tZ)(c.JX,{md:16,xs:24},(0,s.tZ)(p.u,{id:"brand-tooltip",placement:"bottomLeft",title:t.tooltip,arrowPointAtCenter:!0},f(window.location.pathname)?(0,s.tZ)(g.m,{className:"navbar-brand",to:t.path},(0,s.tZ)("img",{src:t.icon,alt:t.alt})):(0,s.tZ)("a",{className:"navbar-brand",href:t.path},(0,s.tZ)("img",{src:t.icon,alt:t.alt}))),t.text&&(0,s.tZ)("div",{className:"navbar-brand-text"},(0,s.tZ)("span",null,t.text)),(0,s.tZ)(u.MainNav,{mode:Z,className:"main-nav",selectedKeys:k},e.map(((e,t)=>{var a;return(({label:e,childs:t,url:a,index:n,isFrontendRoute:l})=>a&&l?(0,s.tZ)(u.MainNav.Item,{key:e,role:"presentation"},(0,s.tZ)(m.OL,{role:"button",to:a,activeClassName:"is-active"},e)):a?(0,s.tZ)(u.MainNav.Item,{key:e},(0,s.tZ)("a",{href:a},e)):(0,s.tZ)(te,{key:n,title:e,icon:"inline"===Z?(0,s.tZ)(i.Fragment,null):(0,s.tZ)(v.Z.TriangleDown,null)},null==t?void 0:t.map(((t,a)=>"string"==typeof t&&"-"===t&&"Data"!==e?(0,s.tZ)(u.MainNav.Divider,{key:`$${a}`}):"string"!=typeof t?(0,s.tZ)(u.MainNav.Item,{key:`${t.label}`},t.isFrontendRoute?(0,s.tZ)(m.OL,{to:t.url||"",exact:!0,activeClassName:"is-active"},t.label):(0,s.tZ)("a",{href:t.url},t.label)):null))))({index:t,...e,isFrontendRoute:f(e.url),childs:null==(a=e.childs)?void 0:a.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:f(e.url)}))})})))),(0,s.tZ)(c.JX,{md:8,xs:24},(0,s.tZ)(X,{align:_.md?"flex-end":"flex-start",settings:n,navbarRight:a,isFrontendRoute:f,environmentTag:l}))))}function le({data:e,...t}){const a={...e},l={Data:!0,Security:!0,Manage:!0},o=[],i=[];return a.menu.forEach((e=>{if(!e)return;const t=[],a={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&t.push(e)})),a.childs=t),l.hasOwnProperty(e.name)?i.push(a):o.push(a)})),a.menu=o,a.settings=i,(0,s.tZ)(ne,(0,n.Z)({data:a},t))}},61337:(e,t,a)=>{var n;function l(e,t){try{const a=localStorage.getItem(e);return null===a?t:JSON.parse(a)}catch{return t}}function o(e,t){try{localStorage.setItem(e,JSON.stringify(t))}catch{}}function i(e,t){return l(e,t)}function r(e,t){o(e,t)}a.d(t,{I_:()=>o,LS:()=>r,OH:()=>l,dR:()=>n,rV:()=>i}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(n||(n={}))}}]);
//# sourceMappingURL=9041.7abd0895f1d7abd9c5bd.entry.js.map