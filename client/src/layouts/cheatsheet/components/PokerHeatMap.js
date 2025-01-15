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
            "https://cdn.anychart.com/samples/heat-map-charts/heat-map-in-poker/data.json",
            function (data) {
              const chart = window.anychart.heatMap(data);

              // Definiere Farbskalen
              const colorScale = window.anychart.scales.ordinalColor();
                 colorScale.ranges([
            { less: 0.35, color: "#1E88E5" }, // Darker blue (perfect)
            { from: 0.35, to: 0.45, color: "#64B5F6" }, // Light blue
            { from: 0.45, to: 0.5, color: "#BBDEFB" }, // Very light blue
            { from: 0.5, to: 0.55, color: "#FFE082" }, // Warm pale yellow-orange
            { from: 0.55, to: 0.6, color: "#FFCA60" }, // Richer golden yellow
            { from: 0.6, to: 0.65, color: "#FFA726" }, // Soft orange
            { from: 0.65, to: 0.7, color: "#FF7043" }, // Light orange-red
            { from: 0.7, to: 0.75, color: "#F4511E" }, // Muted orange-red
            { from: 0.75, to: 0.8, color: "#D84315" }, // Warm reddish-orange
            { greater: 0.8, color: "#BF360C" }, // Subdued red
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
                  const s = this.getData("symbol") === "s" ? "suited" : "unsuited";
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
              alignItems: "center",
              justifyContent: "center",
              padding: "8px",
              marginBottom: "10px",
              boxSizing: "border-box",}}></div>;

}

export default PokerHeatmap;