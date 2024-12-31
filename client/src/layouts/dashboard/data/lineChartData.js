export const lineChartDataDashboard = [
  {
    name: "Jura Jonas",
    data: [[new Date().getTime(), 0.0]], // Start with a timestamp
  },
  {
    name: "Sebastian",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Paul",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Eliah",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Matthi",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Markus",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Luca",
    data: [[new Date().getTime(), 0.0]],
  },
  {
    name: "Jonas",
    data: [[new Date().getTime(), 0.0]],
  },
];

// Add data every 5 seconds instead of every second
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
  }, 5000); // Add data every 5 seconds
}

addDynamicData();
