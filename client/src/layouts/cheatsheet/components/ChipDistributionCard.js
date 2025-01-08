import Card from "@mui/material/Card";
import CheatsheetImage from "assets/images/cheatsheet/hand_ranking.png";
import background from "assets/images/body-background.png";

function ChipDistributionCard() {
  return (
      <Card
          sx={{
              background: `url('${background}') no-repeat center center, linear-gradient(135deg, #0070ba, #1546a0)`,
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
          <div
              style={{
                  textAlign: "center",
                  color: "white",
                  fontSize: "1.2rem",
                  lineHeight: "1.8rem",
                  fontWeight: "bold",
              }}
          >
              <p>6 Chips à 5</p>
              <p>12 Chips à 10</p>
              <p>10 Chips à 25</p>
              <p>6 Chips à 100</p>
              <p>Das ergibt pro Spieler genau 1000 Chips</p>
          </div>
      </Card>
  );
}

export default ChipDistributionCard;