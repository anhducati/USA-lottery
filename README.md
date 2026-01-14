<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>XSMB Daily Dashboard</title>
  <meta name="description" content="Dashboard XSMB tông sáng, cập nhật tự động mỗi ngày: kết quả mới nhất, lịch 7 ngày, top 10 lâu chưa về, 30 ngày và biểu đồ." />

  <style>
    :root{
      --bg:#f7fafc;
      --card:#ffffff;
      --text:#0f172a;
      --muted:#475569;
      --line:#e2e8f0;
      --shadow: 0 10px 26px rgba(2,6,23,.08);
      --radius:18px;
      --radius2:16px;

      --warn:#f59e0b;
      --ok:#22c55e;
      --err:#ef4444;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      color:var(--text);
      background:
        radial-gradient(900px 420px at 10% 0%, rgba(37,99,235,.15), transparent 60%),
        radial-gradient(900px 420px at 90% 5%, rgba(34,197,94,.12), transparent 55%),
        radial-gradient(900px 520px at 50% 105%, rgba(6,182,212,.10), transparent 60%),
        var(--bg);
      min-height:100vh;
    }
    a{color:#2563eb;text-decoration:none}
    a:hover{text-decoration:underline}
    .wrap{max-width:1200px;margin:0 auto;padding:22px 16px 56px}

    /* ===== LED frame ===== */
    .rainbow-frame{
      position:relative;
      border-radius: calc(var(--radius) + 6px);
      padding: 5px;
      background: linear-gradient(90deg,
        #ff0000,
        #ff7a00,
        #ffe600,
        #00d12f,
        #00c2ff,
        #2f5bff,
        #b100ff,
        #ff0000
      );
      background-size: 400% 100%;
      animation: ledFlow 3.2s linear infinite;
      box-shadow: 0 18px 40px rgba(2,6,23,.10);
    }
    .rainbow-frame::before{
      content:"";
      position:absolute; inset:-3px;
      border-radius: calc(var(--radius) + 10px);
      background: inherit;
      background-size: 400% 100%;
      animation: ledFlow 3.2s linear infinite;
      filter: blur(14px);
      opacity:.35;
      z-index:0;
    }
    .rainbow-inner{
      position:relative;
      z-index:1;
      border-radius: var(--radius);
      background: rgba(255,255,255,.82);
      backdrop-filter: blur(10px);
      border:1px solid rgba(255,255,255,.75);
    }
    @keyframes ledFlow{
      0%   { background-position:   0% 50%; }
      100% { background-position: 400% 50%; }
    }

    /* states */
    .rainbow-frame.is-loading{
      animation: ledFlow 2.6s linear infinite, ledPulse 0.9s ease-in-out infinite;
    }
    .rainbow-frame.is-loading::before{
      animation: ledFlow 2.6s linear infinite, ledPulse 0.9s ease-in-out infinite;
      opacity:.55;
    }
    .rainbow-frame.is-success{
      animation: ledFlow 10s linear infinite;
    }
    .rainbow-frame.is-success::before{
      animation: ledFlow 10s linear infinite;
      opacity:.25;
    }
    .rainbow-frame.is-warn{
      animation: ledFlow 3.2s linear infinite, warnPulse 1.0s ease-in-out infinite;
    }
    .rainbow-frame.is-warn::before{
      animation: ledFlow 3.2s linear infinite, warnPulse 1.0s ease-in-out infinite;
      opacity:.60;
    }
    .rainbow-frame.is-error{
      animation: ledFlow 2.2s linear infinite, errPulse 0.6s ease-in-out infinite;
    }
    .rainbow-frame.is-error::before{
      animation: ledFlow 2.2s linear infinite, errPulse 0.6s ease-in-out infinite;
      opacity:.65;
    }
    @keyframes ledPulse{
      0%,100% { filter: saturate(1.05) brightness(1.00); }
      50%     { filter: saturate(1.40) brightness(1.14); }
    }
    @keyframes warnPulse{
      0%,100% { filter: saturate(1.15) brightness(1.02); box-shadow: 0 18px 40px rgba(245,158,11,.18); }
      50%     { filter: saturate(1.60) brightness(1.18); box-shadow: 0 18px 40px rgba(245,158,11,.28); }
    }
    @keyframes errPulse{
      0%,100% { filter: saturate(1.10) brightness(1.02); box-shadow: 0 18px 40px rgba(239,68,68,.18); }
      50%     { filter: saturate(1.65) brightness(1.20); box-shadow: 0 18px 40px rgba(239,68,68,.30); }
    }

    .topbar{
      display:flex; gap:14px; align-items:center; justify-content:space-between; flex-wrap:wrap;
      padding:14px 14px;
    }
    .brand{display:flex; gap:12px; align-items:center}
    .logo{
      width:44px;height:44px;border-radius:14px;
      background: conic-gradient(from 210deg,
        #ff0000, #ff7a00, #ffe600, #00d12f, #00c2ff, #2f5bff, #b100ff, #ff0000
      );
      box-shadow: 0 12px 22px rgba(2,6,23,.12);
      border:1px solid rgba(255,255,255,.7);
    }
    .brand h1{margin:0;font-size:18px}
    .brand .sub{font-size:12px;color:var(--muted);margin-top:2px}

    .chips{display:flex; gap:8px; flex-wrap:wrap; align-items:center; justify-content:flex-end}
    .chip{
      font-size:12px; color:var(--muted);
      padding:8px 10px; border-radius:999px;
      border:1px solid var(--line);
      background: rgba(255,255,255,.85);
      display:flex; gap:8px; align-items:center;
      white-space:nowrap;
    }
    .dot{width:8px;height:8px;border-radius:99px;background:var(--ok); box-shadow:0 0 0 4px rgba(34,197,94,.16)}
    .dot.warn{background:var(--warn); box-shadow:0 0 0 4px rgba(245,158,11,.18)}
    .dot.err{background:var(--err); box-shadow:0 0 0 4px rgba(239,68,68,.18)}

    .btns{display:flex; gap:8px; flex-wrap:wrap}
    .btn{
      text-decoration:none;
      font-size:12px; font-weight:800;
      padding:9px 11px; border-radius:12px;
      border:1px solid var(--line);
      background:#fff;
      color: var(--text);
    }
    .btn:hover{background:#f8fafc}

    /* ✅ STACK dọc */
    .grid{display:grid; gap:14px; grid-template-columns: 1fr; margin-top:14px}

    .card{
      background: var(--card);
      border:1px solid var(--line);
      border-radius: var(--radius2);
      box-shadow: var(--shadow);
      padding:14px;
    }
    .card h2{margin:0 0 10px 0;font-size:14px;color: rgba(15,23,42,.92)}
    .sectionTitle{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}

    .kpiRow{display:grid; gap:10px; grid-template-columns: repeat(3, minmax(0,1fr))}
    @media (max-width: 780px){ .kpiRow{grid-template-columns:1fr} }
    .kpi{padding:12px;border:1px solid var(--line);border-radius: 14px;background:#fff}
    .kpi .label{font-size:12px;color:var(--muted)}
    .kpi .value{font-size:22px;font-weight:950;margin-top:4px}
    .mono{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;}

    .tableWrap{border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#fff}
    .table{
      width:100%;
      border-collapse: collapse;
      background:#fff;
      min-width: 520px;
    }
    .table th,.table td{padding:10px 10px;border-bottom:1px solid var(--line);font-size:13px; vertical-align:top}
    .table th{color:#0f172a;text-align:left;background:#f8fafc}
    .table tr:last-child td{border-bottom:none}

    .split{display:grid; gap:14px; grid-template-columns: 1fr 1fr}
    @media (max-width: 980px){ .split{grid-template-columns:1fr} }
    .imgCard{padding:12px;border-radius: 14px;border:1px solid var(--line);background:#fff}
    .imgCard h3{margin:0 0 10px 0;font-size:13px;color:#0f172a}
    img.chart{width:100%;display:block;border-radius: 12px;border:1px solid var(--line);background:#fff}

    .footer{margin-top:14px;color:var(--muted);font-size:12px;display:flex; gap:10px; flex-wrap:wrap; justify-content:space-between; align-items:center}

    /* mobile */
    @media (max-width: 520px){
      .btns{gap:6px}
      .btn{padding:8px 10px;border-radius:10px}
      .kpi .value{font-size:20px}
      .chip{max-width:100%; overflow:hidden; text-overflow:ellipsis}
      .tableWrap{overflow-x:auto; -webkit-overflow-scrolling: touch;}
      .table{min-width: 760px;}
    }

    .note{
      display:flex; align-items:center; gap:8px;
      padding:10px 12px;
      border-radius:14px;
      border:1px solid var(--line);
      background:#fff7ed;
      color:#7c2d12;
      font-size:13px;
      margin-top:10px;
    }
    .note.good{background:#f0fdf4;color:#14532d}
  </style>
</head>

<body>
  <div class="wrap">
    <div class="rainbow-frame is-loading" id="ledFrame">
      <div class="rainbow-inner">
        <div class="topbar">
          <div class="brand">
            <div class="logo" aria-hidden="true"></div>
            <div>
              <h1>XSMB Daily Dashboard</h1>
              <div class="sub">Tông sáng • LED 7 màu • Update 18:30 VN (retry ~5 phút nếu trễ)</div>
            </div>
          </div>

          <div class="chips">
            <div class="chip" id="liveChip">
              <span class="dot" id="liveDot"></span>
              <span id="statusText">Đang tải dữ liệu…</span>
            </div>
            <div class="chip mono">Updated (VN): <span id="updatedAt">—</span></div>
            <div class="chip mono">SHA: <span id="sha">—</span></div>
            <div class="chip mono">Run: <span id="runId">—</span></div>
            <div class="btns">
              <a class="btn" href="./data/xsmb.json">xsmb.json</a>
              <a class="btn" href="./data/last7.json">last7.json</a>
              <a class="btn" href="./data/site_meta.json">meta</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid">
      <!-- 1) Kết quả mới nhất -->
      <div class="card">
        <div class="sectionTitle">
          <h2 style="margin:0">Kết quả mới nhất</h2>
          <div class="chip mono" id="sourceText">Nguồn: —</div>
        </div>

        <div id="noteBox" class="note" style="display:none;">—</div>

        <div class="kpiRow" style="margin-top:10px">
          <div class="kpi">
            <div class="label">Ngày</div>
            <div class="value" id="lastDate">—</div>
          </div>
          <div class="kpi">
            <div class="label">Giải đặc biệt</div>
            <div class="value mono" id="special">—</div>
          </div>
          <div class="kpi">
            <div class="label">Đề (2 số cuối ĐB)</div>
            <div class="value mono" id="special2d">—</div>
          </div>
        </div>

        <div class="tableWrap" style="margin-top:12px">
          <table class="table" aria-label="Bảng kết quả xổ số">
            <thead>
              <tr><th style="width:170px">Giải</th><th>Kết quả</th></tr>
            </thead>
            <tbody id="resultRows">
              <tr><td style="color:var(--muted)">Đang tải…</td><td style="color:var(--muted)">—</td></tr>
            </tbody>
          </table>
        </div>

        <div class="footer">
          <div>© Auto generated by GitHub Actions</div>
          <div class="mono">Top10: <a href="./data/top10_delta.json">delta</a> • <a href="./data/top10_30d.json">30d</a></div>
        </div>
      </div>

      <!-- ✅ 2) Lịch 7 ngày nằm dưới KQ mới nhất -->
      <div class="card">
        <h2>Lịch gần nhất 7 ngày (full)</h2>
        <div class="tableWrap">
          <table class="table" id="last7Table" aria-label="Lịch 7 ngày">
            <thead>
              <tr>
                <th>Ngày</th>
                <th>ĐB</th>
                <th>Nhất</th>
                <th>Nhì</th>
                <th>Ba</th>
                <th>Tư</th>
                <th>Năm</th>
                <th>Sáu</th>
                <th>Bảy</th>
              </tr>
            </thead>
            <tbody>
              <tr><td colspan="9" style="color:var(--muted)">Đang tải…</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 3) Top10 & chart -->
      <div class="card">
        <h2>Top 10</h2>

        <div class="split">
          <div class="imgCard">
            <h3>Top 10 số lâu chưa về (text)</h3>
            <div class="tableWrap">
              <table class="table" id="top10DeltaTable">
                <thead><tr><th>#</th><th>Số</th><th>Delta (ngày)</th></tr></thead>
                <tbody><tr><td colspan="3" style="color:var(--muted)">Đang tải…</td></tr></tbody>
              </table>
            </div>
          </div>

          <div class="imgCard">
            <h3>Top 10 (30 ngày) (text)</h3>
            <div class="tableWrap">
              <table class="table" id="top10_30dTable">
                <thead><tr><th>#</th><th>Số</th><th>Lượt</th></tr></thead>
                <tbody><tr><td colspan="3" style="color:var(--muted)">Đang tải…</td></tr></tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="split" style="margin-top:14px">
          <div class="imgCard">
            <h3>Top 10 lâu chưa về (chart)</h3>
            <img class="chart" src="./images/delta_top_10.jpg" alt="Top 10 lâu chưa về" />
          </div>
          <div class="imgCard">
            <h3>Top 10 (30 ngày) (chart)</h3>
            <img class="chart" src="./images/top10_30d.jpg" alt="Top 10 30 ngày" />
          </div>
        </div>
      </div>

      <!-- 4) Biểu đồ -->
      <div class="card">
        <h2>Biểu đồ</h2>
        <div class="split">
          <div class="imgCard"><h3>Line 30D Total</h3><img class="chart" src="./images/line_30d_total.jpg" alt="30D total" /></div>
          <div class="imgCard"><h3>Line 30D Unique</h3><img class="chart" src="./images/line_30d_unique.jpg" alt="30D unique" /></div>
        </div>
        <div class="split" style="margin-top:14px">
          <div class="imgCard"><h3>Delta (00–99)</h3><img class="chart" src="./images/delta.jpg" alt="delta" /></div>
          <div class="imgCard"><h3>Heatmap (1 year)</h3><img class="chart" src="./images/heatmap.jpg" alt="heatmap" /></div>
        </div>
        <div class="split" style="margin-top:14px">
          <div class="imgCard"><h3>Top 10 (1 year)</h3><img class="chart" src="./images/top-10.jpg" alt="top10 year" /></div>
          <div class="imgCard"><h3>Distribution (1 year)</h3><img class="chart" src="./images/distribution.jpg" alt="dist" /></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const fmt2 = (n)=> String(n).padStart(2,'0');
    const fmtDateVN = (iso)=>{
      const d = new Date(iso);
      return d.toLocaleDateString("vi-VN", {year:"numeric", month:"2-digit", day:"2-digit"});
    };

    function safeInt(x){ const n = Number(x); return Number.isFinite(n) ? n : null; }

    function setLedState(state){
      const frame = document.getElementById("ledFrame");
      if(!frame) return;
      frame.classList.remove("is-loading","is-success","is-warn","is-error");
      frame.classList.add("is-" + state);
    }

    function setStatus(kind, text){
      const dot = document.getElementById("liveDot");
      document.getElementById("statusText").textContent = text;
      dot.classList.remove("warn","err");
      if(kind === "warn") dot.classList.add("warn");
      if(kind === "err") dot.classList.add("err");
    }

    function buildLatestRows(latest){
      const map = [
        ["Giải ĐB", ["special"]],
        ["Giải nhất", ["prize1"]],
        ["Giải nhì", ["prize2_1","prize2_2"]],
        ["Giải ba", ["prize3_1","prize3_2","prize3_3","prize3_4","prize3_5","prize3_6"]],
        ["Giải tư", ["prize4_1","prize4_2","prize4_3","prize4_4"]],
        ["Giải năm", ["prize5_1","prize5_2","prize5_3","prize5_4","prize5_5","prize5_6"]],
        ["Giải sáu", ["prize6_1","prize6_2","prize6_3"]],
        ["Giải bảy", ["prize7_1","prize7_2","prize7_3","prize7_4"]],
      ];
      const tbody = document.getElementById("resultRows");
      tbody.innerHTML = map.map(([label, cols]) => {
        const vals = cols.map(c => latest[c]).filter(v => v !== undefined && v !== null);
        return `<tr><td>${label}</td><td class="mono">${vals.join(", ") || "—"}</td></tr>`;
      }).join("");
    }

    function renderTop10Delta(rows){
      const tb = document.querySelector("#top10DeltaTable tbody");
      if(!Array.isArray(rows) || rows.length === 0){
        tb.innerHTML = `<tr><td colspan="3" style="color:var(--muted)">Chưa có dữ liệu</td></tr>`;
        return;
      }
      tb.innerHTML = rows.slice(0,10).map((r, i)=>`
        <tr>
          <td>${i+1}</td>
          <td class="mono">${String(r.num).padStart(2,"0")}</td>
          <td class="mono">${r.delta}</td>
        </tr>
      `).join("");
    }

    function renderTop10_30d(rows){
      const tb = document.querySelector("#top10_30dTable tbody");
      if(!Array.isArray(rows) || rows.length === 0){
        tb.innerHTML = `<tr><td colspan="3" style="color:var(--muted)">Chưa có dữ liệu</td></tr>`;
        return;
      }
      tb.innerHTML = rows.slice(0,10).map((r, i)=>`
        <tr>
          <td>${i+1}</td>
          <td class="mono">${String(r.num).padStart(2,"0")}</td>
          <td class="mono">${r.count}</td>
        </tr>
      `).join("");
    }

    function renderLast7(rows){
      const tb = document.querySelector("#last7Table tbody");
      if(!Array.isArray(rows) || rows.length === 0){
        tb.innerHTML = `<tr><td colspan="9" style="color:var(--muted)">Chưa có dữ liệu</td></tr>`;
        return;
      }

      const join = (obj, keys)=> keys.map(k=> obj[k]).join(", ");
      tb.innerHTML = rows.slice().reverse().map(r=>{
        const d = fmtDateVN(r.date);
        return `
          <tr>
            <td class="mono">${d}</td>
            <td class="mono">${r.special}</td>
            <td class="mono">${r.prize1}</td>
            <td class="mono">${join(r, ["prize2_1","prize2_2"])}</td>
            <td class="mono">${join(r, ["prize3_1","prize3_2","prize3_3","prize3_4","prize3_5","prize3_6"])}</td>
            <td class="mono">${join(r, ["prize4_1","prize4_2","prize4_3","prize4_4"])}</td>
            <td class="mono">${join(r, ["prize5_1","prize5_2","prize5_3","prize5_4","prize5_5","prize5_6"])}</td>
            <td class="mono">${join(r, ["prize6_1","prize6_2","prize6_3"])}</td>
            <td class="mono">${join(r, ["prize7_1","prize7_2","prize7_3","prize7_4"])}</td>
          </tr>
        `;
      }).join("");
    }

    async function fetchJson(url){
      const res = await fetch(url + "?ts=" + Date.now());
      if(!res.ok) throw new Error(url + " HTTP " + res.status);
      return await res.json();
    }

    async function main(){
      setLedState("loading");
      setStatus("ok", "Đang tải dữ liệu…");

      // META (để quyết định warn)
      let note = "";
      try{
        const meta = await fetchJson("./data/site_meta.json");
        document.getElementById("updatedAt").textContent = meta.updated_at_vn || "—";
        document.getElementById("sha").textContent = meta.sha || "—";
        document.getElementById("runId").textContent = meta.run_id || "—";
        document.getElementById("sourceText").textContent = "Nguồn: " + (meta.source || "—");
        note = (meta.note || "").toString();
      }catch(e){
        // ignore
      }

      // latest xsmb
      const arr = await fetchJson("./data/xsmb.json");
      if(!Array.isArray(arr) || arr.length === 0) throw new Error("xsmb.json rỗng");
      arr.sort((a,b)=> new Date(a.date) - new Date(b.date));
      const latest = arr[arr.length - 1];

      document.getElementById("lastDate").textContent = fmtDateVN(latest.date);
      const special = safeInt(latest.special);
      document.getElementById("special").textContent = (special !== null) ? String(special) : "—";
      document.getElementById("special2d").textContent = (special !== null) ? fmt2(special % 100) : "—";
      buildLatestRows(latest);

      // ✅ không crash nếu 404
      const results = await Promise.allSettled([
        fetchJson("./data/top10_delta.json"),
        fetchJson("./data/top10_30d.json"),
        fetchJson("./data/last7.json"),
      ]);

      const topDelta = (results[0].status === "fulfilled") ? results[0].value : [];
      const top30    = (results[1].status === "fulfilled") ? results[1].value : [];
      const last7    = (results[2].status === "fulfilled") ? results[2].value : [];

      renderTop10Delta(topDelta);
      renderTop10_30d(top30);
      renderLast7(last7);

      const missing =
        (results[0].status !== "fulfilled") ||
        (results[1].status !== "fulfilled") ||
        (results[2].status !== "fulfilled");

      // NOTE + LED
      const noteBox = document.getElementById("noteBox");
      if(note && note.trim()){
        noteBox.style.display = "flex";
        noteBox.textContent = note;

        if(note.includes("Chưa có kết quả hôm nay")){
          noteBox.classList.remove("good");
          setLedState("warn");
          setStatus("warn", "Chưa có kết quả hôm nay… (đang hiển thị ngày gần nhất)");
        } else {
          noteBox.classList.add("good");
          setLedState("success");
          setStatus("ok", "Online • Đã tải dữ liệu");
        }
      } else if (missing){
        noteBox.style.display = "flex";
        noteBox.classList.remove("good");
        noteBox.textContent = "Thiếu dữ liệu (top10/last7) — hãy chạy python src/main.py hoặc chờ GitHub Actions cập nhật.";
        setLedState("warn");
        setStatus("warn", "Thiếu dữ liệu một phần • Web vẫn hoạt động");
      } else {
        setLedState("success");
        setStatus("ok", "Online • Đã tải dữ liệu");
      }
    }

    main().catch(err=>{
      console.error(err);
      setLedState("error");
      setStatus("err", "Lỗi • " + err.message);
      document.getElementById("resultRows").innerHTML =
        `<tr><td style="color:var(--muted)">Lỗi</td><td style="color:var(--muted)">${err.message}</td></tr>`;
    });
  </script>
</body>
</html>
