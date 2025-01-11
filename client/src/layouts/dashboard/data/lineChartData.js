export const lineChartDataDashboard = [
  {
    name: "Bozzetti",
    data: [], // Start with a timestamp
  },
  {
    name: "Simon",
    data: [],
  },
  {
    name: "Vorderbruegge",
    data: [],
  },
  {
    name: "Meierlohr",
    data: [],
  },
  {
    name: "Maier",
    data: [],
  },
  {
    name: "Huber",
    data: [],
  },
  {
    name: "Hoerter",
    data: [],
  },
  {
    name: "Rogg",
    data: [],
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
