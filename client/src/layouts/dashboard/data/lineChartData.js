export const lineChartDataDashboard = [
  {
    name: "Bozzetti",
    data: [[new Date().getTime(), 0.0]], // Start with a timestamp
  },
  {
    name: "Simon",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Vorderbruegge",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Meierlohr",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Maier",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Huber",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Hoerter",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Rogg",
    data: [[new Date().getTime(), 0.0]],
  },
];

/*
function addDynamicData() {
  let interval = setInterval(() => {
    const currentTime = new Date().getTime(); // Current timestamp in milliseconds

    lineChartDataDashboard.forEach((item) => {
      // Generate random data for demonstration purposes
      const newData = parseFloat((Math.random() * 20 - 10).toFixed(2));
      item.data.push([currentTime, newData]); // Push data as [timestamp, value]
    });

    console.log(lineChartDataDashboard);

    // Stop adding data after 100 entries
    if (lineChartDataDashboard[0].data.length >= 100) {
      clearInterval(interval);
    }
  }, 1000); // Add data every 1 seconds
}

addDynamicData();
 */
