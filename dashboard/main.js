// NYC ZIP Code to Neighborhood Mapping
const zipToArea = {
  // MANHATTAN
  10001: "Chelsea/Midtown",
  10002: "Lower East Side",
  10003: "East Village",
  10004: "Financial District",
  10005: "Wall Street",
  10006: "World Trade Center",
  10007: "Tribeca",
  10009: "Alphabet City",
  10010: "Gramercy",
  10011: "Chelsea",
  10012: "SoHo/NoHo",
  10013: "Tribeca/Chinatown",
  10014: "West Village",
  10016: "Murray Hill",
  10017: "Grand Central",
  10018: "Garment District",
  10019: "Midtown West",
  10021: "Upper East Side",
  10022: "Midtown East",
  10023: "Lincoln Square",
  10024: "Upper West Side",
  10025: "Manhattan Valley",
  10026: "Central Harlem",
  10027: "Morningside Heights",
  10028: "Yorkville",
  10029: "East Harlem",
  10031: "Hamilton Heights",
  10036: "Hell's Kitchen",
  10044: "Roosevelt Island",
  10280: "Battery Park City",

  // BROOKLYN
  11201: "Brooklyn Heights/DUMBO",
  11203: "East Flatbush",
  11204: "Bensonhurst",
  11205: "Clinton Hill",
  11206: "Williamsburg/Bushwick",
  11207: "East New York",
  11208: "Cypress Hills",
  11209: "Bay Ridge",
  11210: "Flatbush",
  11211: "Williamsburg",
  11212: "Brownsville",
  11213: "Crown Heights",
  11214: "Bensonhurst",
  11215: "Park Slope",
  11216: "Bed-Stuy",
  11217: "Boerum Hill",
  11218: "Kensington",
  11219: "Borough Park",
  11220: "Sunset Park",
  11221: "Bushwick",
  11222: "Greenpoint",
  11223: "Gravesend",
  11225: "Crown Heights South",
  11226: "Flatbush",
  11230: "Midwood",
  11231: "Red Hook",
  11232: "Sunset Park East",
  11233: "Stuyvesant Heights",
  11234: "Marine Park/Flatlands",
  11235: "Sheepshead Bay",
  11237: "Bushwick North",
  11238: "Prospect Heights",
  11249: "Williamsburg Waterfront",

  // QUEENS
  11101: "Long Island City",
  11102: "Astoria",
  11103: "Astoria",
  11104: "Sunnyside",
  11105: "Astoria/Ditmars",
  11106: "Astoria South",
  11354: "Flushing",
  11355: "Flushing South",
  11357: "Whitestone",
  11358: "Auburndale",
  11360: "Bayside (North)",
  11361: "Bayside",
  11364: "Oakland Gardens",
  11365: "Fresh Meadows",
  11367: "Kew Gardens Hills",
  11368: "Corona",
  11369: "East Elmhurst",
  11372: "Jackson Heights",
  11373: "Elmhurst",
  11374: "Rego Park",
  11375: "Forest Hills",
  11377: "Woodside",
  11378: "Maspeth",
  11379: "Middle Village",
  11385: "Ridgewood",
  11412: "St. Albans",
  11413: "Laurelton",
  11415: "Kew Gardens",
  11417: "Ozone Park",
  11418: "Richmond Hill",
  11419: "South Richmond Hill",
  11420: "South Ozone Park",
  11421: "Woodhaven",
  11432: "Jamaica",
  11434: "South Jamaica",
  11435: "Briarwood",
  11691: "Far Rockaway",
  11694: "Rockaway Park",

  // BRONX
  10451: "Concourse",
  10452: "Highbridge",
  10453: "Morris Heights",
  10454: "Mott Haven",
  10455: "Melrose",
  10456: "Morrisania",
  10457: "Tremont",
  10458: "Fordham",
  10459: "Longwood",
  10460: "West Farms",
  10461: "Pelham Bay",
  10462: "Parkchester",
  10463: "Kingsbridge",
  10464: "City Island",
  10465: "Throggs Neck",
  10466: "Wakefield",
  10467: "Norwood",
  10468: "University Heights",
  10469: "Williamsbridge",
  10471: "Riverdale",
  10472: "Soundview",
  10473: "Castle Hill",
  10475: "Co-op City",

  // STATEN ISLAND
  10301: "St. George",
  10302: "Port Richmond",
  10303: "Mariners Harbor",
  10304: "Stapleton",
  10305: "South Beach",
  10306: "New Dorp",
  10307: "Tottenville",
  10308: "Great Kills",
  10309: "Charleston",
  10310: "West Brighton",
  10312: "Eltingville",
  10314: "Mid-Island",
};

let industryData = [],
  neighborhoodSummary = [];
let charts = { main: null, scatter: null, share: null };

async function init() {
  try {
    const [indRes, summRes] = await Promise.all([
      fetch("industry_data.json"),
      fetch("neighborhood_summary.json"),
    ]);
    industryData = await indRes.json();
    neighborhoodSummary = await summRes.json();
    populateDropdown();
    setupSearch();
    updateDashboard();
  } catch (e) {
    console.error("Critical Data Failure:", e);
  }
}

function getArea(zip) {
  return zipToArea[zip] || `ZIP ${zip}`;
}

function populateDropdown() {
  const select = document.getElementById("category-select");
  const categories = [
    ...new Set(industryData.map((d) => d.business_category)),
  ].sort();
  categories.forEach((cat) => select.add(new Option(cat, cat)));
  select.value = categories[0];
  select.onchange = updateDashboard;
}

function setupSearch() {
  document.getElementById("zip-search").addEventListener("input", (e) => {
    updateTable(e.target.value.toLowerCase());
  });
}

function updateDashboard() {
  const category = document.getElementById("category-select").value;
  const filtered = industryData
    .filter((d) => d.business_category === category)
    .sort((a, b) => b.opportunity_score - a.opportunity_score);
  const top = filtered[0];

  // Update KPIs
  document.getElementById("kpi-rent").textContent = top
    ? `$${Math.round(top.avg_rent).toLocaleString()}`
    : "--";
  document.getElementById("kpi-stability").textContent = top
    ? `${top.neighborhood_avg_age.toFixed(1)}y`
    : "--";
  document.getElementById("kpi-score").textContent = top
    ? top.opportunity_score.toFixed(4)
    : "--";
  const sat = top
    ? Math.max(12, (100 - top.opportunity_score * 8500).toFixed(1))
    : "--";
  document.getElementById("kpi-saturation").textContent = `${sat}%`;

  // Pro-Tip
  document.getElementById("tip-text").innerHTML = top
    ? `ALGORITHM STATUS: High-probability entry found in <strong>${getArea(top.address_zip)}</strong>. Saturation is low (${sat}%), indicating significant market gap for <u>${category}</u>.`
    : "Select Industry...";

  renderMainChart(filtered.slice(0, 10));
  renderScatterChart(filtered);
  if (top) renderShareChart(top.address_zip);
  updateTable();
}

function renderMainChart(data) {
  const ctx = document.getElementById("opportunityChart").getContext("2d");
  if (charts.main) charts.main.destroy();

  // Create Gradient
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, "#00f2ff");
  gradient.addColorStop(1, "#7000ff");

  charts.main = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map((d) => getArea(d.address_zip)),
      datasets: [
        {
          label: "Opportunity Score",
          data: data.map((d) => d.opportunity_score),
          backgroundColor: gradient,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
    },
  });
}

function renderScatterChart(data) {
  const ctx = document.getElementById("scatterChart").getContext("2d");
  if (charts.scatter) charts.scatter.destroy();
  charts.scatter = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "All Zones",
          data: data.map((d) => ({
            x: d.avg_rent,
            y: d.neighborhood_avg_age,
            zip: d.address_zip,
          })),
          backgroundColor: "#7000ff",
          borderColor: "#00f2ff",
          borderWidth: 1,
          pointRadius: 6,
          hoverRadius: 10,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: "Rent ($)", color: "#94a3b8" },
          grid: { color: "#1e293b" },
        },
        y: {
          title: { display: true, text: "Stability (Yrs)", color: "#94a3b8" },
          grid: { color: "#1e293b" },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (c) => `${getArea(c.raw.zip)}: $${c.raw.x} / ${c.raw.y}yr`,
          },
        },
      },
    },
  });
}

function renderShareChart(zip) {
  const ctx = document.getElementById("marketShareChart").getContext("2d");
  if (charts.share) charts.share.destroy();
  const zipData = industryData.filter((d) => d.address_zip === zip).slice(0, 5);
  charts.share = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: zipData.map((d) => d.business_category),
      datasets: [
        {
          data: zipData.map((d) => d.opportunity_score),
          backgroundColor: [
            "#00f2ff",
            "#7000ff",
            "#00ff88",
            "#ffb800",
            "#ff0055",
          ],
          borderWidth: 0,
          hoverOffset: 20,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#94a3b8", font: { size: 10 } },
        },
      },
    },
  });
}

function updateTable(searchTerm = "") {
  const tbody = document.querySelector("#summaryTable tbody");
  const displayData = neighborhoodSummary.filter(
    (s) =>
      s.address_zip.toString().includes(searchTerm) ||
      getArea(s.address_zip).toLowerCase().includes(searchTerm),
  );
  tbody.innerHTML = displayData
    .slice(0, 15)
    .map(
      (s) => `
        <tr>
            <td><strong>${s.address_zip}</strong><br><small style="color:var(--text-dim)">${getArea(s.address_zip)}</small></td>
            <td><span style="color:var(--success)">${s.neighborhood_type}</span></td>
            <td>${s.top_recommended_biz}</td>
        </tr>
    `,
    )
    .join("");
}

init();
