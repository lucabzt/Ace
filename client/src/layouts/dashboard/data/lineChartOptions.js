export const lineChartOptionsDashboard = {
  chart: {
    toolbar: {
      show: false,
    },
  },
  tooltip: {
    theme: "light",
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
    width: 4, // Increase stroke width to make the lines thicker
  },
 xaxis: {
    type: "numeric",
    categories: [

    ],
    labels: {
      style: {
        colors: "#FFF", // Text color for x-axis labels
        fontSize: "12px", // Slightly larger font size for better visibility
        fontWeight: "600", // Set font weight to make text bolder
      },
      formatter: function (value) {
        const date = new Date(value);
        return date.getHours().toString().padStart(2, '0') + ":" + date.getMinutes().toString().padStart(2, '0');
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
    show: true,
    position: "top",
    horizontalAlign: "center", // Align legend in the center
    fontSize: "16px", // General font size for legend
    fontWeight: 500, // Regular weight for legend text
    labels: {
      colors: "#FFFFFF", // Force white text color for legend
      useSeriesColors: false, // Prevent using series colors for legend text
    },
    markers: {
      size: 10, // Increase marker size slightly for better visibility
      fillColors: undefined, // Default to series colors for markers
      strokeWidth: 0, // Add a small stroke to markers
    },
    onItemClick: {
      toggleDataSeries: true, // Allow toggling data series on click
    },
    onItemHover: {
      highlightDataSeries: true, // Highlight series on hover
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
      "#ff8800",
      "#1ABC9C",
      "#E74C3C",
      "#cb208e",
      "#2ECC71",
      "#3498DB",
      "#ffee20",
      "#8E44AD"
  ],
};