const API_RELEASES = "https://api.github.com/repos/randompixle/Solar-Neo/releases";

async function loadVersions() {
    const container = document.getElementById("version-list");
    container.innerHTML = "<p>Loading…</p>";

    try {
        const res = await fetch(API_RELEASES);
        if (!res.ok) throw new Error("GitHub API fail");
        const releases = await res.json();

        if (!releases.length) {
            container.innerHTML = "<p>No releases found yet.</p>";
            return;
        }

        releases.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));

        container.innerHTML = "";
        releases.forEach(rel => {
            const assetZip = rel.assets.find(a => a.name.toLowerCase().endsWith(".zip"));
            const codename = rel.name.split(" ").slice(-1)[0] || "N/A";

            const card = document.createElement("div");
            card.className = "release-card";
            card.innerHTML = `
                <h2>${rel.tag_name}</h2>
                <p><strong>Codename:</strong> ${codename}</p>
                <p><strong>Date:</strong> ${new Date(rel.published_at).toLocaleDateString()}</p>
                <p><strong>Channel:</strong> ${rel.prerelease ? "Prerelease" : "Stable"}</p>
                <div class="actions">
                    ${assetZip ? `
                        <a class="btn" href="${assetZip.browser_download_url}">
                            Download ZIP
                        </a>
                    ` : `<span class="btn disabled">No ZIP asset</span>`}
                </div>
            `;
            container.appendChild(card);
        });

    } catch (err) {
        console.error(err);
        container.innerHTML = `
            <p style="color:red;">Error loading releases.</p>
            <p>Check GitHub rate limits or try again later.</p>
        `;
    }
}

loadVersions();
