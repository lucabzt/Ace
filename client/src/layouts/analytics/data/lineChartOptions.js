export const lineChartOptionsDashboard = {
  chart: {
    toolbar: { show: false },
  },
  tooltip: { theme: "light" },
  dataLabels: { enabled: false },
  stroke: { curve: "smooth", width: 4 },
  xaxis: {
    type: "datetime",
    categories: ["Day 0", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8", "Day 9"],
    labels: {
      style: { colors: "#FFF", fontSize: "12px", fontWeight: "600" },
    },
    axisBorder: { show: false },
    axisTicks: { show: false },
  },
  yaxis: {
    labels: { style: { colors: "#c8cfca", fontSize: "12px", fontWeight: "600" } },
  },
  legend: {
    show: true,
    position: "top",
    labels: {
      style: {
        colors: "#FFFFFF", // Force white color
        fontSize: "16px",
        fontWeight: "600",
      },
    },
    markers: { width: 10, height: 10, strokeWidth: 0 },
  },
  grid: {
    show: true,
    strokeDashArray: 0,
    borderColor: "#56577A",
  },
  fill: { type: "solid", opacity: 0 },
  colors: ["#F39C12", "#1ABC9C", "#E74C3C", "#9B59B6", "#2ECC71", "#3498DB", "#F1C40F", "#8E44AD"],
};
