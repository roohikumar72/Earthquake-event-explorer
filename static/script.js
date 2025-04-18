async function fetchAndRender() {
    const response = await fetch('/api/data');
    const data = await response.json();
  
    renderSummary(data);
    renderChart(data);
  
    document.getElementById("minMag").addEventListener("input", (e) => {
      const minMag = parseFloat(e.target.value);
      document.getElementById("magValue").textContent = minMag.toFixed(1);
      const filtered = data.filter(d => d.magnitude >= minMag);
      renderChart(filtered);
    });
  }
  
  function renderSummary(data) {
    document.getElementById("totalCount").textContent = `Total earthquakes: ${data.length}`;
    let max = data.reduce((a, b) => (a.magnitude > b.magnitude ? a : b));
    document.getElementById("strongest").textContent = `Strongest quake: ${max.magnitude} at ${max.place}`;
  
    let counts = {};
    data.forEach(d => {
      let day = new Date(d.time * 1000).toISOString().slice(0, 10);
      counts[day] = (counts[day] || 0) + 1;
    });
    let topDay = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];
    document.getElementById("topDay").textContent = `Most active day: ${topDay[0]} (${topDay[1]} quakes)`;
  }
  
  function renderChart(data) {
    const trace = {
      x: data.map(d => new Date(d.time * 1000)),
      y: data.map(d => d.magnitude),
      type: "scatter",
      mode: "markers",
      marker: { color: 'red', size: 8 },
      text: data.map(d => d.place),
    };
  
    const layout = {
      title: "Earthquake Magnitude Over Time",
      xaxis: { title: "Time" },
      yaxis: { title: "Magnitude" }
    };
  
    Plotly.newPlot("chart", [trace], layout);
  }
  
  fetchAndRender();
  