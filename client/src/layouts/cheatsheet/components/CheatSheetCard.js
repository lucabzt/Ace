import Card from "@mui/material/Card";
import CheatsheetImage from "assets/images/cheatsheet/hand_ranking.JPG";
import billingCard from "assets/images/curved-images/white-curved.jpeg";

function CheatsheetCard() {
  return (
    <Card
      sx={{
        background: `url('${billingCard}') no-repeat center center, linear-gradient(135deg, #0070ba, #1546a0)`,
        backgroundSize: "cover",
        backdropFilter: "blur(31px)",
        borderRadius: "16px",
        overflow: "hidden", // Keine Inhalte außerhalb der Kartenränder
        color: "black",
        height: "80%", // Feste Kartengröße
        display: "flex", // Flexbox für Zentrierung
        alignItems: "center",
        justifyContent: "center",
        padding: "8px", // Abstand innerhalb der Karte
        boxSizing: "border-box", // Wichtig für Padding
      }}
    >
      <img
        src={CheatsheetImage}
        alt="Cheatsheet Full Image"
        style={{
          width: "100%", // Größe anpassen, um Rand zu verkleinern
          height: "100%", // Größe anpassen
          objectFit: "contain", // Das Bild wird vollständig angezeigt
        }}
      />
    </Card>
  );
}

export default CheatsheetCard;