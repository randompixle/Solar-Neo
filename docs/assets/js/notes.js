import {h} from './common.js';

const NOTES_PATH='notes/notes.json';
const SUBMIT_ENDPOINT='../cgi-bin/submit_note.py';
const OWNER='randompixle';
const REPO='Solar-Neo';
const BRANCH='main';

function setStatus(msgEl, type, text){
  if(!msgEl) return;
  msgEl.textContent=text;
  msgEl.classList.remove('ok','err');
  if(type) msgEl.classList.add(type);
}

function setNotesMessage(container, text, state){
  if(!container) return;
  container.dataset.state=state||'';
  container.setAttribute('aria-busy', state==='loading' ? 'true' : 'false');
  container.innerHTML='';
  container.append(h('div',{class:'notes-placeholder'},text));
}

function renderNotes(container, data){
  if(!container) return;
  const entries=Object.entries(data||{})
    .map(([pkg, list])=>[pkg, Array.isArray(list)?list.filter(item=>typeof item==='string'&&item.trim()):[]])
    .filter(([, list])=>list.length>0)
    .sort((a,b)=>a[0].localeCompare(b[0], undefined,{sensitivity:'base'}));

  if(entries.length===0){
    setNotesMessage(container,'No notes yet. Submit the first update to kick things off.','empty');
    return;
  }

  container.dataset.state='ready';
  container.setAttribute('aria-busy','false');
  container.innerHTML='';
  const frag=document.createDocumentFragment();
  for(const [pkg, list] of entries){
    const items=list.map(item=>h('li',{},item));
    frag.append(h('article',{class:'notes-package', role:'listitem'},[
      h('div',{class:'notes-package-title'},pkg),
      h('ul',{class:'notes-package-list'},items)
    ]));
  }
  container.append(frag);
}

async function fetchJSON(url){
  const res=await fetch(url,{cache:'no-store'});
  if(res.status===404){
    return {};
  }
  if(!res.ok){
    throw new Error(`HTTP ${res.status}`);
  }
  try{
    return await res.json();
  }catch(err){
    throw new Error('Invalid notes payload');
  }
}

async function loadFromLocal(){
  return fetchJSON(`../${NOTES_PATH}?cache=`+Date.now());
}

async function loadFromGitHubRaw(){
  return fetchJSON(`https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${NOTES_PATH}?cache=`+Date.now());
}

function getToken(){
  return (localStorage.getItem('SOLAR_GH_TOKEN')||'').trim();
}

async function shaOf(path, token){
  const res=await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}?ref=${BRANCH}`,{
    headers:{
      'Accept':'application/vnd.github+json',
      'Authorization':`Bearer ${token}`
    }
  });
  if(res.status===404){
    return null;
  }
  if(!res.ok){
    const text=await res.text();
    throw new Error(`GitHub metadata failed: ${res.status} ${text}`);
  }
  const json=await res.json();
  return json?.sha||null;
}

async function writeNotesToGit(notes,pkg){
  const token=getToken();
  if(!token){
    throw new Error('Store a GitHub token in localStorage as `SOLAR_GH_TOKEN` or use the shared password.');
  }
  const content=JSON.stringify(notes,null,2)+'\n';
  const body={
    message:`Add note for ${pkg}`,
    content:btoa(unescape(encodeURIComponent(content))),
    branch:BRANCH
  };
  const sha=await shaOf(NOTES_PATH,token);
  if(sha){
    body.sha=sha;
  }
  const res=await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${NOTES_PATH}`,{
    method:'PUT',
    headers:{
      'Accept':'application/vnd.github+json',
      'Content-Type':'application/json',
      'Authorization':`Bearer ${token}`
    },
    body:JSON.stringify(body)
  });
  if(!res.ok){
    const text=await res.text();
    throw new Error(`GitHub write failed: ${res.status} ${text}`);
  }
  return res.json();
}

async function readNotesForWrite(){
  try{
    return await loadFromGitHubRaw();
  }catch(err){
    console.warn('Falling back to local notes for submission',err);
    try{
      return await loadFromLocal();
    }catch{
      return {};
    }
  }
}

export default function initNotesPage(){
  const notesList=document.querySelector('[data-notes]');
  if(!notesList) return;

  const msg=document.getElementById('msg');
  const submitBtn=document.getElementById('submit');
  const pkgInput=document.getElementById('pkg');
  const noteInput=document.getElementById('note');
  const passwordInput=document.getElementById('password');
  const refreshBtn=document.querySelector('[data-notes-refresh]');
  const defaultSubmitLabel=submitBtn?.textContent||'Submit note';

  async function loadNotes({showSpinner=true}={}){
    if(showSpinner){
      setNotesMessage(notesList,'Loading notes…','loading');
    }
    let payload=null;
    try{
      payload=await loadFromLocal();
    }catch(err){
      console.warn('Local notes load failed, attempting GitHub',err);
      try{
        payload=await loadFromGitHubRaw();
      }catch(remoteErr){
        console.error('Failed to load notes',remoteErr);
        setNotesMessage(notesList,'Unable to load notes. Serve the repo with `python -m http.server --cgi` or provide a GitHub token for write access.','error');
        return;
      }
    }
    renderNotes(notesList,payload);
  }

  submitBtn?.addEventListener('click', async()=>{
    setStatus(msg,'','');
    const pkg=(pkgInput?.value||'').trim();
    const note=(noteInput?.value||'').trim();
    const password=(passwordInput?.value||'').trim();
    if(!pkg||!note){ setStatus(msg,'err','Package and note are required.'); return; }

    if(submitBtn){
      submitBtn.disabled=true;
      submitBtn.setAttribute('aria-busy','true');
      submitBtn.textContent='Submitting…';
    }

    try{
      if(password){
        const res=await fetch(SUBMIT_ENDPOINT,{
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({password,pkg,note})
        });
        let out=null;
        try{ out=await res.json(); }catch{}
        if(!res.ok||!out?.ok){
          const err=out?.error||`Submission failed (${res.status})`;
          throw new Error(err);
        }
      }else{
        let notes=await readNotesForWrite();
        if(!notes||typeof notes!=='object'||Array.isArray(notes)){
          notes={};
        }else{
          notes={...notes};
        }
        const existing=Array.isArray(notes[pkg])?notes[pkg].slice():[];
        existing.push(note);
        notes[pkg]=existing;
        await writeNotesToGit(notes,pkg);
      }

      setStatus(msg,'ok','Note submitted.');
      if(!password && passwordInput){
        passwordInput.value='';
      }
      if(pkgInput) pkgInput.value='';
      if(noteInput) noteInput.value='';
      await loadNotes({showSpinner:false});
    }catch(e){
      setStatus(msg,'err',String(e?.message||e||'Unknown error'));
    }finally{
      if(submitBtn){
        submitBtn.disabled=false;
        submitBtn.removeAttribute('aria-busy');
        submitBtn.textContent=defaultSubmitLabel;
      }
    }
  });

  refreshBtn?.addEventListener('click', ()=>{
    loadNotes({showSpinner:true});
  });

  loadNotes({showSpinner:true});
}
