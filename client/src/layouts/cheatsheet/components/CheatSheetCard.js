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
        overflow: "hidden",
        color: "black",
        height: "80%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "8px",
        boxSizing: "border-box",
      }}
    >
      <img
        src={CheatsheetImage}
        alt="Cheatsheet Full Image"
        style={{
          width: "100%",
          height: "100%",
          borderRadius: "10px",
          objectFit: "contain",
          filter: "contrast(1.2) brightness(0.8) hue-rotate(-1deg)",
        }}
      />
    </Card>
  );
}

export default CheatsheetCard;