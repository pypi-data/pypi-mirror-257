"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7177],{6065:(e,t,l)=>{l.r(t),l.d(t,{default:()=>D});var a=l(51995),n=l(55867),r=l(31069),i=l(67294),o=l(19259),s=l(70163),u=l(18782),d=l(14114),c=l(58593),p=l(86074),h=l(15926),m=l.n(h),g=l(34858),f=l(11965),b=l(74069),v=l(81315),y=l(84101),Z=l(49238),w=l(8272);const x=[{label:(0,n.t)("Regular"),value:"Regular"},{label:(0,n.t)("Base"),value:"Base"}];var k;!function(e){e.REGULAR="Regular",e.BASE="Base"}(k||(k={}));const _=f.iv`
  margin: 0;

  .ant-input {
    margin: 0;
  }
`,R=(0,a.iK)(b.Z)`
  max-width: 1200px;
  min-width: min-content;
  width: 100%;
  .ant-modal-body {
    overflow: initial;
  }
  .ant-modal-footer {
    white-space: nowrap;
  }
`,T=e=>f.iv`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,N=a.iK.div`
  display: flex;
  flex-direction: column;
  padding: ${e=>{let{theme:t}=e;return`${3*t.gridUnit}px ${4*t.gridUnit}px ${2*t.gridUnit}px`}};

  label,
  .control-label {
    display: inline-block;
    font-size: ${e=>{let{theme:t}=e;return t.typography.sizes.s}}px;
    color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
    vertical-align: middle;
  }

  .info-solid-small {
    vertical-align: middle;
    padding-bottom: ${e=>{let{theme:t}=e;return t.gridUnit/2}}px;
  }
`,S=a.iK.div`
  display: flex;
  flex-direction: column;
  margin: ${e=>{let{theme:t}=e;return t.gridUnit}}px;
  margin-bottom: ${e=>{let{theme:t}=e;return 4*t.gridUnit}}px;

  .input-container {
    display: flex;
    align-items: center;

    > div {
      width: 100%;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  .required {
    margin-left: ${e=>{let{theme:t}=e;return t.gridUnit/2}}px;
    color: ${e=>{let{theme:t}=e;return t.colors.error.base}};
  }
`,E=a.iK.textarea`
  height: 100px;
  resize: none;
  margin-top: ${e=>{let{theme:t}=e;return t.gridUnit}}px;
  border: 1px solid ${e=>{let{theme:t}=e;return t.colors.secondary.light3}};
`,C={name:"",filter_type:k.REGULAR,tables:[],roles:[],clause:"",group_key:"",description:""},$=function(e){const{rule:t,addDangerToast:l,addSuccessToast:a,onHide:o,show:u}=e,[d,c]=(0,i.useState)({...C}),[p,h]=(0,i.useState)(!0),b=null!==t,{state:{loading:$,resource:A,error:F},fetchResource:D,createResource:H,updateResource:B,clearError:q}=(0,g.LE)("rowlevelsecurity",(0,n.t)("rowlevelsecurity"),l);(0,i.useEffect)((()=>{b?null===(null==t?void 0:t.id)||$||F||D(t.id):c({...C})}),[t]),(0,i.useEffect)((()=>{if(A){c({...A,id:null==t?void 0:t.id});const e=z();U("tables",(null==e?void 0:e.tables)||[]),U("roles",(null==e?void 0:e.roles)||[])}}),[A]);const z=(0,i.useCallback)((()=>{var e,t;if(!A)return null;const l=[],a=[];return null==(e=A.tables)||e.forEach((e=>{l.push({key:e.id,label:e.schema?`${e.schema}.${e.table_name}`:e.table_name,value:e.id})})),null==(t=A.roles)||t.forEach((e=>{a.push({key:e.id,label:e.name,value:e.id})})),{tables:l,roles:a}}),[null==A?void 0:A.tables,null==A?void 0:A.roles]),L=d||{};(0,i.useEffect)((()=>{j()}),[L.name,L.clause,null==L?void 0:L.tables]);const U=(e,t)=>{c((l=>({...l,[e]:t})))},M=e=>{U(e.name,e.value)},K=()=>{q(),c({...C}),o()},P=(0,i.useMemo)((()=>function(e,t,l){void 0===e&&(e="");const a=m().encode({filter:e,page:t,page_size:l});return r.Z.get({endpoint:`/api/v1/rowlevelsecurity/related/tables?q=${a}`}).then((e=>({data:e.json.result.map((e=>({label:e.text,value:e.value}))),totalCount:e.json.count})))}),[]),G=(0,i.useMemo)((()=>function(e,t,l){void 0===e&&(e="");const a=m().encode({filter:e,page:t,page_size:l});return r.Z.get({endpoint:`/api/v1/rowlevelsecurity/related/roles?q=${a}`}).then((e=>({data:e.json.result.map((e=>({label:e.text,value:e.value}))),totalCount:e.json.count})))}),[]),j=()=>{var e;null!=d&&d.name&&null!=d&&d.clause&&null!=(e=d.tables)&&e.length?h(!1):h(!0)};return(0,f.tZ)(R,{className:"no-content-padding",responsive:!0,show:u,onHide:K,primaryButtonName:b?(0,n.t)("Save"):(0,n.t)("Add"),disablePrimaryButton:p,onHandledPrimaryAction:()=>{var e,t;const l=[],r=[];null==(e=d.tables)||e.forEach((e=>l.push(e.key))),null==(t=d.roles)||t.forEach((e=>r.push(e.key)));const i={...d,tables:l,roles:r};if(b&&d.id){const e=d.id;delete i.id,B(e,i).then((e=>{e&&(a("Rule updated"),K())}))}else d&&H(i).then((e=>{e&&(a((0,n.t)("Rule added")),K())}))},width:"30%",maxWidth:"1450px",title:(0,f.tZ)("h4",null,b?(0,f.tZ)(s.Z.EditAlt,{css:T}):(0,f.tZ)(s.Z.PlusLarge,{css:T}),b?(0,n.t)("Edit Rule"):(0,n.t)("Add Rule"))},(0,f.tZ)(N,null,(0,f.tZ)("div",{className:"main-section"},(0,f.tZ)(S,null,(0,f.tZ)(Z.QA,{id:"name",name:"name",className:"labeled-input",value:d?d.name:"",required:!0,validationMethods:{onChange:e=>{let{target:t}=e;return M(t)}},css:_,label:(0,n.t)("Rule Name"),tooltipText:(0,n.t)("The name of the rule must be unique"),hasTooltip:!0})),(0,f.tZ)(S,null,(0,f.tZ)("div",{className:"control-label"},(0,n.t)("Filter Type")," ",(0,f.tZ)(w.Z,{tooltip:(0,n.t)("Regular filters add where clauses to queries if a user belongs to a role referenced in the filter, base filters apply filters to all queries except the roles defined in the filter, and can be used to define what users can see if no RLS filters within a filter group apply to them.")})),(0,f.tZ)("div",{className:"input-container"},(0,f.tZ)(v.Z,{name:"filter_type",ariaLabel:(0,n.t)("Filter Type"),placeholder:(0,n.t)("Filter Type"),onChange:e=>{U("filter_type",e)},value:null==d?void 0:d.filter_type,options:x}))),(0,f.tZ)(S,null,(0,f.tZ)("div",{className:"control-label"},(0,n.t)("Datasets")," ",(0,f.tZ)("span",{className:"required"},"*"),(0,f.tZ)(w.Z,{tooltip:(0,n.t)("These are the datasets this filter will be applied to.")})),(0,f.tZ)("div",{className:"input-container"},(0,f.tZ)(y.Z,{ariaLabel:(0,n.t)("Tables"),mode:"multiple",onChange:e=>{U("tables",e||[])},value:(null==d?void 0:d.tables)||[],options:P}))),(0,f.tZ)(S,null,(0,f.tZ)("div",{className:"control-label"},d.filter_type===k.BASE?(0,n.t)("Excluded roles"):(0,n.t)("Roles")," ",(0,f.tZ)(w.Z,{tooltip:(0,n.t)("For regular filters, these are the roles this filter will be applied to. For base filters, these are the roles that the filter DOES NOT apply to, e.g. Admin if admin should see all data.")})),(0,f.tZ)("div",{className:"input-container"},(0,f.tZ)(y.Z,{ariaLabel:(0,n.t)("Roles"),mode:"multiple",onChange:e=>{U("roles",e||[])},value:(null==d?void 0:d.roles)||[],options:G}))),(0,f.tZ)(S,null,(0,f.tZ)(Z.QA,{id:"group_key",name:"group_key",value:d?d.group_key:"",validationMethods:{onChange:e=>{let{target:t}=e;return M(t)}},css:_,label:(0,n.t)("Group Key"),hasTooltip:!0,tooltipText:(0,n.t)("Filters with the same group key will be ORed together within the group, while different filter groups will be ANDed together. Undefined group keys are treated as unique groups, i.e. are not grouped together. For example, if a table has three filters, of which two are for departments Finance and Marketing (group key = 'department'), and one refers to the region Europe (group key = 'region'), the filter clause would apply the filter (department = 'Finance' OR department = 'Marketing') AND (region = 'Europe').")})),(0,f.tZ)(S,null,(0,f.tZ)("div",{className:"control-label"},(0,f.tZ)(Z.QA,{id:"clause",name:"clause",value:d?d.clause:"",required:!0,validationMethods:{onChange:e=>{let{target:t}=e;return M(t)}},css:_,label:(0,n.t)("Clause"),hasTooltip:!0,tooltipText:(0,n.t)("This is the condition that will be added to the WHERE clause. For example, to only return rows for a particular client, you might define a regular filter with the clause `client_id = 9`. To display no rows unless a user belongs to a RLS filter role, a base filter can be created with the clause `1 = 0` (always false).")}))),(0,f.tZ)(S,null,(0,f.tZ)("div",{className:"control-label"},(0,n.t)("Description")),(0,f.tZ)("div",{className:"input-container"},(0,f.tZ)(E,{name:"description",value:d?d.description:"",onChange:e=>M(e.target)}))))))};var A=l(40768);const F=a.iK.div`
  color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
`,D=(0,d.ZP)((function(e){const{addDangerToast:t,addSuccessToast:l,user:a}=e,[d,h]=(0,i.useState)(!1),[b,v]=(0,i.useState)(null),{state:{loading:y,resourceCount:Z,resourceCollection:w,bulkSelectEnabled:x},hasPerm:k,fetchData:_,refreshData:R,toggleBulkSelect:T}=(0,g.Yi)("rowlevelsecurity",(0,n.t)("Row Level Security"),t,!0,void 0,void 0,!0);function N(e){v(e),h(!0)}function S(){v(null),h(!1),R()}const E=k("can_write"),C=k("can_write"),D=k("can_export"),H=(0,i.useMemo)((()=>[{accessor:"name",Header:(0,n.t)("Name")},{accessor:"filter_type",Header:(0,n.t)("Filter Type"),size:"xl"},{accessor:"group_key",Header:(0,n.t)("Group Key"),size:"xl"},{accessor:"clause",Header:(0,n.t)("Clause")},{Cell:e=>{let{row:{original:{changed_on_delta_humanized:t}}}=e;return(0,f.tZ)("span",{className:"no-wrap"},t)},Header:(0,n.t)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:e=>{let{row:{original:a}}=e;return(0,f.tZ)(F,{className:"actions"},E&&(0,f.tZ)(o.Z,{title:(0,n.t)("Please confirm"),description:(0,f.tZ)(i.Fragment,null,(0,n.t)("Are you sure you want to delete")," ",(0,f.tZ)("b",null,a.name)),onConfirm:()=>function(e,t,l,a){let{id:i,name:o}=e;return r.Z.delete({endpoint:`/api/v1/rowlevelsecurity/${i}`}).then((()=>{t(),l((0,n.t)("Deleted %s",o))}),(0,A.v$)((e=>a((0,n.t)("There was an issue deleting %s: %s",o,e)))))}(a,R,l,t)},(e=>(0,f.tZ)(c.u,{id:"delete-action-tooltip",title:(0,n.t)("Delete"),placement:"bottom"},(0,f.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},(0,f.tZ)(s.Z.Trash,null))))),C&&(0,f.tZ)(c.u,{id:"edit-action-tooltip",title:(0,n.t)("Edit"),placement:"bottom"},(0,f.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>N(a)},(0,f.tZ)(s.Z.EditAlt,null))))},Header:(0,n.t)("Actions"),id:"actions",hidden:!C&&!E&&!D,disableSortBy:!0}]),[a.userId,C,E,D,k,R,t,l]),B={title:(0,n.t)("No Rules yet"),image:"filter-results.svg",buttonAction:()=>N(null),buttonText:C?(0,f.tZ)(i.Fragment,null,(0,f.tZ)("i",{className:"fa fa-plus"})," ","Rule"," "):null},q=(0,i.useMemo)((()=>[{Header:(0,n.t)("Name"),key:"search",id:"name",input:"search",operator:u.p.startsWith},{Header:(0,n.t)("Filter Type"),key:"filter_type",id:"filter_type",input:"select",operator:u.p.equals,unfilteredLabel:(0,n.t)("Any"),selects:[{label:(0,n.t)("Regular"),value:"Regular"},{label:(0,n.t)("Base"),value:"Base"}]},{Header:(0,n.t)("Group Key"),key:"search",id:"group_key",input:"search",operator:u.p.startsWith}]),[a]),z=[{id:"changed_on_delta_humanized",desc:!0}],L=[];return E&&(L.push({name:(0,f.tZ)(i.Fragment,null,(0,f.tZ)("i",{className:"fa fa-plus"})," ",(0,n.t)("Rule")),buttonStyle:"primary",onClick:()=>N(null)}),L.push({name:(0,n.t)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:T})),(0,f.tZ)(i.Fragment,null,(0,f.tZ)(p.Z,{name:(0,n.t)("Row Level Security"),buttons:L}),(0,f.tZ)(o.Z,{title:(0,n.t)("Please confirm"),description:(0,n.t)("Are you sure you want to delete the selected rules?"),onConfirm:function(e){const a=e.map((e=>{let{id:t}=e;return t}));return r.Z.delete({endpoint:`/api/v1/rowlevelsecurity/?q=${m().encode(a)}`}).then((()=>{R(),l((0,n.t)("Deleted"))}),(0,A.v$)((e=>t((0,n.t)("There was an issue deleting rules: %s",e)))))}},(e=>{const a=[];return E&&a.push({key:"delete",name:(0,n.t)("Delete"),type:"danger",onSelect:e}),(0,f.tZ)(i.Fragment,null,(0,f.tZ)($,{rule:b,addDangerToast:t,onHide:S,addSuccessToast:l,show:d}),(0,f.tZ)(u.Z,{className:"rls-list-view",bulkActions:a,bulkSelectEnabled:x,disableBulkSelect:T,columns:H,count:Z,data:w,emptyState:B,fetchData:_,filters:q,initialSort:z,loading:y,pageSize:25}))})))}))}}]);
//# sourceMappingURL=93854ece4ba1a7bfc0c4.chunk.js.map