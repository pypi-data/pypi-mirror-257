/*! For license information please see 692.d7dd851ce6b7f32bbac2.js.LICENSE.txt */
"use strict";(self.webpackChunk_jupyterlite_javascript_kernel_extension=self.webpackChunk_jupyterlite_javascript_kernel_extension||[]).push([[692,312],{692:(e,t,n)=>{n.r(t),n.d(t,{JavaScriptKernel:()=>j});var r=n(388),a=n(960),s=n(464);const o=Symbol("Comlink.proxy"),i=Symbol("Comlink.endpoint"),c=Symbol("Comlink.releaseProxy"),u=Symbol("Comlink.finalizer"),l=Symbol("Comlink.thrown"),p=e=>"object"==typeof e&&null!==e||"function"==typeof e,m=new Map([["proxy",{canHandle:e=>p(e)&&e[o],serialize(e){const{port1:t,port2:n}=new MessageChannel;return d(e,t),[n,[n]]},deserialize:e=>(e.start(),g(e))}],["throw",{canHandle:e=>p(e)&&l in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function d(e,t=globalThis,n=["*"]){t.addEventListener("message",(function r(a){if(!a||!a.data)return;if(!function(e,t){for(const n of e){if(t===n||"*"===n)return!0;if(n instanceof RegExp&&n.test(t))return!0}return!1}(n,a.origin))return void console.warn(`Invalid origin '${a.origin}' for comlink proxy`);const{id:s,type:i,path:c}=Object.assign({path:[]},a.data),p=(a.data.argumentList||[]).map(x);let m;try{const t=c.slice(0,-1).reduce(((e,t)=>e[t]),e),n=c.reduce(((e,t)=>e[t]),e);switch(i){case"GET":m=n;break;case"SET":t[c.slice(-1)[0]]=x(a.data.value),m=!0;break;case"APPLY":m=n.apply(t,p);break;case"CONSTRUCT":m=function(e){return Object.assign(e,{[o]:!0})}(new n(...p));break;case"ENDPOINT":{const{port1:t,port2:n}=new MessageChannel;d(e,n),m=function(e,t){return E.set(e,t),e}(t,[t])}break;case"RELEASE":m=void 0;break;default:return}}catch(e){m={value:e,[l]:0}}Promise.resolve(m).catch((e=>({value:e,[l]:0}))).then((n=>{const[a,o]=_(n);t.postMessage(Object.assign(Object.assign({},a),{id:s}),o),"RELEASE"===i&&(t.removeEventListener("message",r),h(t),u in e&&"function"==typeof e[u]&&e[u]())})).catch((e=>{const[n,r]=_({value:new TypeError("Unserializable return value"),[l]:0});t.postMessage(Object.assign(Object.assign({},n),{id:s}),r)}))})),t.start&&t.start()}function h(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function g(e,t){return w(e,[],t)}function y(e){if(e)throw new Error("Proxy has been released and is not useable")}function f(e){return R(e,{type:"RELEASE"}).then((()=>{h(e)}))}const v=new WeakMap,b="FinalizationRegistry"in globalThis&&new FinalizationRegistry((e=>{const t=(v.get(e)||0)-1;v.set(e,t),0===t&&f(e)}));function w(e,t=[],n=function(){}){let r=!1;const a=new Proxy(n,{get(n,s){if(y(r),s===c)return()=>{!function(e){b&&b.unregister(e)}(a),f(e),r=!0};if("then"===s){if(0===t.length)return{then:()=>a};const n=R(e,{type:"GET",path:t.map((e=>e.toString()))}).then(x);return n.then.bind(n)}return w(e,[...t,s])},set(n,a,s){y(r);const[o,i]=_(s);return R(e,{type:"SET",path:[...t,a].map((e=>e.toString())),value:o},i).then(x)},apply(n,a,s){y(r);const o=t[t.length-1];if(o===i)return R(e,{type:"ENDPOINT"}).then(x);if("bind"===o)return w(e,t.slice(0,-1));const[c,u]=k(s);return R(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:c},u).then(x)},construct(n,a){y(r);const[s,o]=k(a);return R(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:s},o).then(x)}});return function(e,t){const n=(v.get(t)||0)+1;v.set(t,n),b&&b.register(e,t,e)}(a,e),a}function k(e){const t=e.map(_);return[t.map((e=>e[0])),(n=t.map((e=>e[1])),Array.prototype.concat.apply([],n))];var n}const E=new WeakMap;function _(e){for(const[t,n]of m)if(n.canHandle(e)){const[r,a]=n.serialize(e);return[{type:"HANDLER",name:t,value:r},a]}return[{type:"RAW",value:e},E.get(e)||[]]}function x(e){switch(e.type){case"HANDLER":return m.get(e.name).deserialize(e.value);case"RAW":return e.value}}function R(e,t,n){return new Promise((r=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(n){n.data&&n.data.id&&n.data.id===a&&(e.removeEventListener("message",t),r(n.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:a},t),n)}))}class j extends a.BaseKernel{constructor(e){super(e),this._ready=new s.PromiseDelegate,this._worker=this.initWorker(e),this._worker.onmessage=e=>this._processWorkerMessage(e.data),this.remoteKernel=this.initRemote(e),this._ready.resolve()}dispose(){this.isDisposed||(this._worker.terminate(),this._worker=null,super.dispose())}get ready(){return this._ready.promise}async kernelInfoRequest(){return{implementation:"JavaScript",implementation_version:"0.1.0",language_info:{codemirror_mode:{name:"javascript"},file_extension:".js",mimetype:"text/javascript",name:"javascript",nbconvert_exporter:"javascript",pygments_lexer:"javascript",version:"es2017"},protocol_version:"5.3",status:"ok",banner:"A JavaScript kernel running in the browser",help_links:[{text:"JavaScript Kernel",url:"https://github.com/jupyterlite/javascript-kernel"}]}}async executeRequest(e){const t=await this.remoteKernel.execute(e,this.parent);return t.execution_count=this.executionCount,t}async completeRequest(e){return await this.remoteKernel.complete(e,this.parent)}async inspectRequest(e){throw new Error("Not implemented")}async isCompleteRequest(e){throw new Error("Not implemented")}async commInfoRequest(e){throw new Error("Not implemented")}inputReply(e){throw new Error("Not implemented")}async commOpen(e){throw new Error("Not implemented")}async commMsg(e){throw new Error("Not implemented")}async commClose(e){throw new Error("Not implemented")}initWorker(e){return new Worker(new URL(n.p+n.u(584),n.b),{type:void 0})}initRemote(e){const t=g(this._worker);return t.initialize({baseUrl:r.PageConfig.getBaseUrl()}),t}_processWorkerMessage(e){var t,n,r,a,s,o,i;if(!e.type)return;const c=e.parentHeader||this.parentHeader;switch(e.type){case"stream":{const n=null!==(t=e.bundle)&&void 0!==t?t:{name:"stdout",text:""};this.stream(n,c);break}case"input_request":{const t=null!==(n=e.content)&&void 0!==n?n:{prompt:"",password:!1};this.inputRequest(t,c);break}case"display_data":{const t=null!==(r=e.bundle)&&void 0!==r?r:{data:{},metadata:{},transient:{}};this.displayData(t,c);break}case"update_display_data":{const t=null!==(a=e.bundle)&&void 0!==a?a:{data:{},metadata:{},transient:{}};this.updateDisplayData(t,c);break}case"clear_output":{const t=null!==(s=e.bundle)&&void 0!==s?s:{wait:!1};this.clearOutput(t,c);break}case"execute_result":{const t=null!==(o=e.bundle)&&void 0!==o?o:{execution_count:0,data:{},metadata:{}};this.publishExecuteResult(t,c);break}case"execute_error":{const t=null!==(i=e.bundle)&&void 0!==i?i:{ename:"",evalue:"",traceback:[]};this.publishExecuteError(t,c);break}case"comm_msg":case"comm_open":case"comm_close":this.handleComm(e.type,e.content,e.metadata,e.buffers,e.parentHeader)}}}}}]);