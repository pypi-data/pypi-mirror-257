var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,o,a,i,l,u,f,d,s,p,c,h,v,y,b,m,g,j,w,k={624:(e,r,t)=>{var n={"./index":()=>Promise.all([t.e(772),t.e(154)]).then((()=>()=>t(260))),"./extension":()=>Promise.all([t.e(772),t.e(154)]).then((()=>()=>t(260)))},o=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),a=(e,r)=>{if(t.S){var n="default",o=t.S[n];if(o&&o!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>o,init:()=>a})}},P={};function _(e){var r=P[e];if(void 0!==r)return r.exports;var t=P[e]={exports:{}};return k[e](t,t.exports,_),t.exports}_.m=k,_.c=P,_.amdO={},r=Object.getPrototypeOf?e=>Object.getPrototypeOf(e):e=>e.__proto__,_.t=function(t,n){if(1&n&&(t=this(t)),8&n)return t;if("object"==typeof t&&t){if(4&n&&t.__esModule)return t;if(16&n&&"function"==typeof t.then)return t}var o=Object.create(null);_.r(o);var a={};e=e||[null,r({}),r([]),r(r)];for(var i=2&n&&t;"object"==typeof i&&!~e.indexOf(i);i=r(i))Object.getOwnPropertyNames(i).forEach((e=>a[e]=()=>t[e]));return a.default=()=>t,_.d(o,a),o},_.d=(e,r)=>{for(var t in r)_.o(r,t)&&!_.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},_.f={},_.e=e=>Promise.all(Object.keys(_.f).reduce(((r,t)=>(_.f[t](e,r),r)),[])),_.u=e=>e+"."+{128:"cb82559482664768a01e",136:"d81524385b84f5da0d63",154:"903f9cba1eb1062facff",532:"bc8437207579d19f20cf",576:"e47a4b5a16a66a5936fa",772:"c96e3c5dad26b78f0ee4"}[e]+".js?v="+{128:"cb82559482664768a01e",136:"d81524385b84f5da0d63",154:"903f9cba1eb1062facff",532:"bc8437207579d19f20cf",576:"e47a4b5a16a66a5936fa",772:"c96e3c5dad26b78f0ee4"}[e],_.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),_.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),t={},n="@jupyterlite/pyodide-kernel-extension:",_.l=(e,r,o,a)=>{if(t[e])t[e].push(r);else{var i,l;if(void 0!==o)for(var u=document.getElementsByTagName("script"),f=0;f<u.length;f++){var d=u[f];if(d.getAttribute("src")==e||d.getAttribute("data-webpack")==n+o){i=d;break}}i||(l=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,_.nc&&i.setAttribute("nonce",_.nc),i.setAttribute("data-webpack",n+o),i.src=e),t[e]=[r];var s=(r,n)=>{i.onerror=i.onload=null,clearTimeout(p);var o=t[e];if(delete t[e],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((e=>e(n))),r)return r(n)},p=setTimeout(s.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=s.bind(null,i.onerror),i.onload=s.bind(null,i.onload),l&&document.head.appendChild(i)}},_.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{_.S={};var e={},r={};_.I=(t,n)=>{n||(n=[]);var o=r[t];if(o||(o=r[t]={}),!(n.indexOf(o)>=0)){if(n.push(o),e[t])return e[t];_.o(_.S,t)||(_.S[t]={});var a=_.S[t],i="@jupyterlite/pyodide-kernel-extension",l=(e,r,t,n)=>{var o=a[e]=a[e]||{},l=o[r];(!l||!l.loaded&&(!n!=!l.eager?n:i>l.from))&&(o[r]={get:t,from:i,eager:!!n})},u=[];return"default"===t&&(l("@jupyterlite/pyodide-kernel-extension","0.3.0-alpha.0",(()=>Promise.all([_.e(772),_.e(154)]).then((()=>()=>_(260))))),l("@jupyterlite/pyodide-kernel","0.3.0-alpha.0",(()=>Promise.all([_.e(128),_.e(136),_.e(772)]).then((()=>()=>_(808)))))),e[t]=u.length?Promise.all(u).then((()=>e[t]=1)):1}}})(),(()=>{var e;_.g.importScripts&&(e=_.g.location+"");var r=_.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");if(t.length)for(var n=t.length-1;n>-1&&!e;)e=t[n--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),_.p=e})(),o=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},a=(e,r)=>{e=o(e),r=o(r);for(var t=0;;){if(t>=e.length)return t<r.length&&"u"!=(typeof r[t])[0];var n=e[t],a=(typeof n)[0];if(t>=r.length)return"u"==a;var i=r[t],l=(typeof i)[0];if(a!=l)return"o"==a&&"n"==l||"s"==l||"u"==a;if("o"!=a&&"u"!=a&&n!=i)return n<i;t++}},i=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(l=e[o]))[0]?"-":(n>0?".":"")+(n=2,l);return t}var a=[];for(o=1;o<e.length;o++){var l=e[o];a.push(0===l?"not("+u()+")":1===l?"("+u()+" || "+u()+")":2===l?a.pop()+" "+a.pop():i(l))}return u();function u(){return a.pop().replace(/^\((.+)\)$/,"$1")}},l=(e,r)=>{if(0 in e){r=o(r);var t=e[0],n=t<0;n&&(t=-t-1);for(var a=0,i=1,u=!0;;i++,a++){var f,d,s=i<e.length?(typeof e[i])[0]:"";if(a>=r.length||"o"==(d=(typeof(f=r[a]))[0]))return!u||("u"==s?i>t&&!n:""==s!=n);if("u"==d){if(!u||"u"!=s)return!1}else if(u)if(s==d)if(i<=t){if(f!=e[i])return!1}else{if(n?f>e[i]:f<e[i])return!1;f!=e[i]&&(u=!1)}else if("s"!=s&&"n"!=s){if(n||i<=t)return!1;u=!1,i--}else{if(i<=t||d<s!=n)return!1;u=!1}else"s"!=s&&"n"!=s&&(u=!1,i--)}}var p=[],c=p.pop.bind(p);for(a=1;a<e.length;a++){var h=e[a];p.push(1==h?c()|c():2==h?c()&c():h?l(h,r):!c())}return!!c()},u=(e,r)=>{var t=_.S[e];if(!t||!_.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},f=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&a(e,r)?r:e),0)},d=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+i(n)+")",s=(e,r,t,n)=>{var o=f(e,t);return l(n,o)||c(d(e,t,o,n)),h(e[t][o])},p=(e,r,t)=>{var n=e[r];return(r=Object.keys(n).reduce(((e,r)=>!l(t,r)||e&&!a(e,r)?e:r),0))&&n[r]},c=e=>{"undefined"!=typeof console&&console.warn&&console.warn(e)},h=e=>(e.loaded=1,e.get()),y=(v=e=>function(r,t,n,o){var a=_.I(r);return a&&a.then?a.then(e.bind(e,r,_.S[r],t,n,o)):e(r,_.S[r],t,n,o)})(((e,r,t,n)=>(u(e,t),s(r,0,t,n)))),b=v(((e,r,t,n,o)=>{var a=r&&_.o(r,t)&&p(r,t,n);return a?h(a):o()})),m={},g={281:()=>y("default","@jupyterlab/coreutils",[1,6,0,12]),448:()=>y("default","@jupyterlite/kernel",[2,0,3,0,,"alpha",0]),376:()=>y("default","@jupyterlite/server",[2,0,3,0,,"alpha",0]),904:()=>y("default","@jupyterlite/contents",[2,0,3,0,,"alpha",0]),464:()=>y("default","@lumino/coreutils",[1,2,0,0]),532:()=>b("default","@jupyterlite/pyodide-kernel",[2,0,3,0,,"alpha",0],(()=>Promise.all([_.e(128),_.e(136)]).then((()=>()=>_(808)))))},j={136:[464],154:[376,904],532:[532],772:[281,448]},w={},_.f.consumes=(e,r)=>{_.o(j,e)&&j[e].forEach((e=>{if(_.o(m,e))return r.push(m[e]);if(!w[e]){var t=r=>{m[e]=0,_.m[e]=t=>{delete _.c[e],t.exports=r()}};w[e]=!0;var n=r=>{delete m[e],_.m[e]=t=>{throw delete _.c[e],r}};try{var o=g[e]();o.then?r.push(m[e]=o.then(t).catch(n)):t(o)}catch(e){n(e)}}}))},(()=>{_.b=document.baseURI||self.location.href;var e={480:0};_.f.j=(r,t)=>{var n=_.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else if(/^(53|77)2$/.test(r))e[r]=0;else{var o=new Promise(((t,o)=>n=e[r]=[t,o]));t.push(n[2]=o);var a=_.p+_.u(r),i=new Error;_.l(a,(t=>{if(_.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var o=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+o+": "+a+")",i.name="ChunkLoadError",i.type=o,i.request=a,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,o,[a,i,l]=t,u=0;if(a.some((r=>0!==e[r]))){for(n in i)_.o(i,n)&&(_.m[n]=i[n]);l&&l(_)}for(r&&r(t);u<a.length;u++)o=a[u],_.o(e,o)&&e[o]&&e[o][0](),e[o]=0},t=self.webpackChunk_jupyterlite_pyodide_kernel_extension=self.webpackChunk_jupyterlite_pyodide_kernel_extension||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var S=_(624);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@jupyterlite/pyodide-kernel-extension"]=S})();
//# sourceMappingURL=remoteEntry.0b52bcb9e036442e31cb.js.map