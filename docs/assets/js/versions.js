const BASE = "/Solar-Neo/docs";

async function loadVersions() {
    const listUrl = `${BASE}/Versions/Version_Index.json`;
    const res = await fetch(listUrl);
    const versions = await res.json();

    const container = document.getElementById("versionList");
    container.innerHTML = "";

    versions.forEach(v => {
        const zip = `${BASE}/Versions/${v.folder}/Release.zip`;
        const div = document.createElement("div");
        div.className = "version-entry";
        div.innerHTML = `
            <h3>${v.name} — ${v.version}</h3>
            <a href="${zip}" download>Download</a>
        `;
        container.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", loadVersions);
