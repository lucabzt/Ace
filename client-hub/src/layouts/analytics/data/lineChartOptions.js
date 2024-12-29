export const lineChartOptionsDashboard = {
  chart: {
    toolbar: {
      show: false,
    },
  },
  tooltip: {
    theme: "dark",
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
    width: 4, // Increase stroke width to make the lines thicker
  },
  xaxis: {
    type: "datetime",
    categories: [
      "Day 0",
      "Day 1",
      "Day 2",
      "Day 3",
      "Day 4",
      "Day 5",
      "Day 6",
      "Day 7",
      "Day 8",
    ],
    labels: {
      style: {
        colors: "#FFF", // Text color for x-axis labels
        fontSize: "12px", // Slightly larger font size for better visibility
        fontWeight: "600", // Set font weight to make text bolder
      },
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: "#c8cfca", // Text color for y-axis labels
        fontSize: "12px", // Slightly larger font size for better visibility
        fontWeight: "600", // Set font weight to make text bolder
      },
    },
  },
  legend: {
    show: true, // Display legend so names are visible with colors
    position: "top", // Optional: position the legend at the top of the chart
    labels: {
      style: {
        colors: "#FFFFFF", // Ensure that legend text is white
        fontSize: "16px", // Increase font size for the legend text (e.g., 16px)
        fontWeight: "600", // Set font weight to make text bolder
      },
    },
    markers: {
      width: 10, // Optional: change width of legend markers
      height: 10, // Optional: change height of legend markers
      strokeWidth: 0, // Optional: remove stroke on legend markers
    },
  },
  grid: {
    show: true, // Keep grid lines, but no shading
    strokeDashArray: 0, // Remove dashed grid lines
    borderColor: "#56577A",
  },
  fill: {
    type: "solid", // Remove gradient fill under the lines
    opacity: 0, // Set opacity to 0 so there's no fill under the line
  },
  colors: [
    "#F39C12", // Color for Jura Jonas
    "#1ABC9C", // Color for Sebastian
    "#E74C3C", // Color for Paul
    "#9B59B6", // Color for Eliah
    "#2ECC71", // Color for Matthi
    "#3498DB", // Color for Markus
    "#F1C40F", // Color for Luca
    "#8E44AD", // Color for Jonas
  ],
};
