import React, { useEffect } from "react";
import background from "../../../assets/images/body-background.png";

function PokerHeatmap() {
  useEffect(() => {
    // Funktion zum Laden von Scripten mit Promises
    const loadScript = (src) => {
      return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        script.onload = resolve; // Resolve, wenn das Script vollständig geladen ist
        script.onerror = () => reject(new Error(`Failed to load script: ${src}`));
        document.body.appendChild(script);
      });
    };

    // Funktion zum Laden von Stylesheets
    const loadStyles = (href) => {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = href;
      document.head.appendChild(link);
    };

    // Heatmap-Rendering-Logik
    const loadHeatmap = () => {
      if (window.anychart) {
        window.anychart.onDocumentReady(() => {
          window.anychart.theme("darkBlue");

          // Lade Daten und erstelle das Heatmap-Diagramm
          window.anychart.data.loadJsonFile(
                        "https://localhost:5000/heatmap",
            function (data) {
              const chart = window.anychart.heatMap(data);

              // Definiere Farbskalen
              const colorScale = window.anychart.scales.ordinalColor();
                 colorScale.ranges([
        { from: 0.3, to: 0.325, color: "#0D47A1" }, // Dark Blue
        { from: 0.325, to: 0.35, color: "#1565C0" }, // Strong Blue
        { from: 0.35, to: 0.375, color: "#1976D2" }, // Medium Blue
        { from: 0.375, to: 0.4, color: "#1E88E5" }, // Darker Blue
        { from: 0.4, to: 0.425, color: "#42A5F5" }, // Bright Blue
        { from: 0.425, to: 0.45, color: "#64B5F6" }, // Light Blue
        { from: 0.45, to: 0.475, color: "#90CAF9" }, // Very Light Blue
        { from: 0.475, to: 0.5, color: "#BBDEFB" }, // Pale Blue
        { from: 0.5, to: 0.525, color: "#FFEB3B" }, // Bright Yellow
        { from: 0.525, to: 0.55, color: "#FFCA28" }, // Golden Yellow
        { from: 0.55, to: 0.575, color: "#FFB300" }, // Deep Yellow
        { from: 0.575, to: 0.6, color: "#FF9800" }, // Strong Orange
        { from: 0.6, to: 0.625, color: "#FF5722" }, // Red-Orange
        { from: 0.625, to: 0.65, color: "#F4511E" }, // Duller Orange-Red
        { from: 0.65, to: 0.675, color: "#E34220" }, // Warm Orange-Red
        { from: 0.675, to: 0.7, color: "#D84315" }, // Reddish Orange
        { from: 0.7, to: 0.725, color: "#C73702" }, // Intense Red
        { from: 0.725, to: 0.75, color: "#BF360C" }, // Deep Red
        { from: 0.75, to: 0.775, color: "#9A2A11" }, // Dark Red-Orange
        { from: 0.775, to: 0.8, color: "#8E2409" }, // Dark Red
        { from: 0.8, to: 0.825, color: "#8B0000" }, // Darker Red
        { greater: 0.85, color: "#7F0000" }  // Darkest Red
            ]);
              chart.colorScale(colorScale);

              // Chart konfigurieren
              chart
                .title()
                .useHtml(true)
                .enabled(true)
                .padding([0, 0, 10, 5])
                .align("left")
                .fontColor("white")
                .text(
                  "Hand Rankings <span style='font-size: 13px; color:#FFFFFF'>(Texas Hold'em)</span>"
                );

              chart
                .labels()
                .enabled(true)
                .maxFontSize(14)
                .format(function () {
                  return this.x + this.y + this.getData("symbol");
                });

              chart
                .yAxis(null)
                .xAxis(null)
                .stroke("#fff");

              chart
                .hovered()
                .stroke("6 #fff")
                .fill("#545f69")
                .labels({ fontColor: "#fff" });

              chart
                .legend()
                .enabled(true)
                .align("top")
                .position("right")
                .itemsLayout("vertical")
                .fontColor("white")
                .padding([2, 10, 0, 20]);

              chart
                .tooltip()
                .titleFormat(function () {
                  const s = this.getData("symbol") === "s" ? "suited" : "offsuit";
                  return `${this.x}${this.y} ${s}`;
                })
                .format(function () {
                  return `Win statistic: ${this.heat}`;
                });

              chart.container("heatmap-container");
              chart.background({ enabled: false });
              chart.draw();
            }
          );
        });
      }
    };

    // Scripte und Stylesheets laden
    const loadScriptsInOrder = async () => {
      try {
        // Lade Stylesheets
        [
          "https://cdn.anychart.com/releases/v8/css/anychart-ui.min.css",
          "https://cdn.anychart.com/releases/v8/fonts/css/anychart-font.min.css",
        ].forEach(loadStyles);

        // Lade Scripte in der richtigen Reihenfolge
        await loadScript("https://cdn.anychart.com/releases/v8/js/anychart-base.min.js");
        await Promise.all([
          loadScript("https://cdn.anychart.com/releases/v8/js/anychart-ui.min.js"),
          loadScript("https://cdn.anychart.com/releases/v8/js/anychart-exports.min.js"),
          loadScript("https://cdn.anychart.com/releases/v8/js/anychart-heatmap.min.js"),
          loadScript("https://cdn.anychart.com/releases/v8/js/anychart-data-adapter.min.js"),
          loadScript("https://cdn.anychart.com/releases/v8/themes/dark_blue.min.js"),
        ]);

        // Heatmap zeichnen
        loadHeatmap();
      } catch (err) {
        console.error("Error loading resources:", err);
      }
    };

    // Lade die Ressourcen
    loadScriptsInOrder();

    // Cleanup-Funktion
    return () => {
      // Keine Entfernung von Scripten/Styles notwendig
    };
  }, []);

  return <div id="heatmap-container" style={{ width: "100%", height: "80vh",
              background: `url('${background}') no-repeat center center, linear-gradient(135deg, #0070ba, #1546a0)`,
              borderRadius: "16px",
              backgroundSize: "cover", // Hier wird sichergestellt, dass das Bild den Container vollständig ausfüllt
              alignItems: "center",
              justifyContent: "center",
              padding: "8px",
              marginBottom: "10px",
              boxSizing: "border-box",}}></div>;

}

export default PokerHeatmap;