/**/

// @mui material components
import Grid from "@mui/material/Grid";

// @mui icons
import FacebookIcon from "@mui/icons-material/Facebook";
import TwitterIcon from "@mui/icons-material/Twitter";
import InstagramIcon from "@mui/icons-material/Instagram";
import PinterestIcon from "@mui/icons-material/Pinterest";
import LinkedInIcon from "@mui/icons-material/LinkedIn";

// Vision UI Dashboard React components
import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";

function Footer() {
  return (
    <VuiBox
      component="footer"
      py={6}
      sx={({ breakpoints }) => ({
        maxWidth: "450px",
        [breakpoints.down("xl")]: {
          maxWidth: "400px",
        },
      })}
    >
      <Grid container justifyContent="center">
        <Grid item xs={12} sx={{ textAlign: "center" }}>
          <VuiTypography
            variant="button"
            sx={{ textAlign: "center", fontWeight: "400 !important" }}
            color="text"
          >
            @ 2021, Made with ❤️&nbsp;&nbsp;&nbsp; by{" "}
            <VuiTypography
              component="a"
              variant="button"
              href="#"
              sx={{ textAlign: "center", fontWeight: "500 !important" }}
              color="text"
              mr="2px"
            >
              Simmmple
            </VuiTypography>
            &
            <VuiTypography
              ml="2px"
              mr="2px"
              component="a"
              variant="button"
              href="#"
              sx={{ textAlign: "center", fontWeight: "500 !important" }}
              color="text"
            >
              SPADE
            </VuiTypography>
            for a better web
          </VuiTypography>
        </Grid>
        <Grid item xs={10}>
          <VuiBox display="flex" justifyContent="center" flexWrap="wrap" mb={3}>
            <VuiBox mr={{ xs: "20px", lg: "46px" }}>
              <VuiTypography component="a" href="#" variant="body2" color="text">
                Marketplace
              </VuiTypography>
            </VuiBox>
            <VuiBox mr={{ xs: "20px", lg: "46px" }}>
              <VuiTypography component="a" href="#" variant="body2" color="text">
                Blog
              </VuiTypography>
            </VuiBox>
            <VuiBox>
              <VuiTypography component="a" href="#" variant="body2" color="text">
                License
              </VuiTypography>
            </VuiBox>
          </VuiBox>
        </Grid>
      </Grid>
    </VuiBox>
  );
}

export default Footer;
