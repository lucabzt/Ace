import Card from "@mui/material/Card";
import CheatsheetImage from "assets/images/cheatsheet/hand_ranking.png";
import background from "assets/images/body-background.png";

function CheatsheetCard() {
  return (
      <Card
          sx={{
              background: `url('${background}') no-repeat center center, linear-gradient(135deg, #0070ba, #1546a0)`,
              backgroundSize: "cover",
              backdropFilter: "blur(31px)",
              borderRadius: "16px",
              overflow: "hidden",
              color: "black",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "8px",
              boxSizing: "border-box",
          }}
      >
          <h3 style={{textAlign: "center", marginBottom: "0px", color: "white"}}>Hand Rankings</h3>
          <img
              src={CheatsheetImage}
              alt="Cheatsheet Full Image"
              style={{
                  width: "95%",
                  height: "95%",
                  padding: "3px",
                  borderRadius: "16px",
                  filter: "contrast(1.3) brightness(0.9) hue-rotate(5deg) saturate(1)",
              }}
          />
      </Card>
  );
}

export default CheatsheetCard;