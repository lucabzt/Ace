/**/

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

// @mui material components
import Grid from "@mui/material/Grid";

// Vision UI Dashboard React components
import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";

// Vision UI Dashboard React example components
import DefaultNavbar from "../../../../examples/Navbars/DefaultNavbar";
import PageLayout from "../../../../examples/LayoutContainers/PageLayout";

// Vision UI Dashboard React page layout routes
import pageRoutes from "page.routes";

// Images
import pattern from "assets/images/shapes/pattern-lines.svg";

function IllustrationLayout({ color, header, title, description, illustration, children }) {
  return (
    <PageLayout background="white">
      <DefaultNavbar
        routes={pageRoutes}
        action={{
          type: "external",
          route: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
          label: "RICK ROLL",
        }}
      />
      <Grid container>
        <Grid item xs={11} sm={8} md={6} lg={4} xl={3} sx={{ mx: "auto" }}>
          <VuiBox display="flex" flexDirection="column" justifyContent="center" height="100vh">
            <VuiBox pt={3} px={3}>
              {!header ? (
                <>
                  <VuiBox mb={1}>
                    <VuiTypography variant="h4" fontWeight="bold">
                      {title}
                    </VuiTypography>
                  </VuiBox>
                  <VuiTypography variant="body2" fontWeight="regular" color="text">
                    {description}
                  </VuiTypography>
                </>
              ) : (
                header
              )}
            </VuiBox>
            <VuiBox p={3}>{children}</VuiBox>
          </VuiBox>
        </Grid>
        <Grid item xs={12} lg={6}>
          <VuiBox
            display={{ xs: "none", lg: "flex" }}
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            width="calc(100% - 2rem)"
            height="calc(100vh - 2rem)"
            position="relative"
            borderRadius="lg"
            textAlign="center"
            bgColor={color}
            variant="gradient"
            m={2}
            px={13}
            sx={{ overflow: "hidden" }}
          >
            <VuiBox
              component="img"
              src={pattern}
              alt="pattern-lines"
              width="120rem"
              position="absolute"
              topl={0}
              left={0}
              opacity={0.4}
            />
            {illustration.image && (
              <VuiBox
                component="img"
                src={illustration.image}
                alt="chat-illustration"
                width="100%"
                maxWidth="31.25rem"
              />
            )}
            {illustration.title && (
              <VuiBox mt={6} mb={1}>
                <VuiTypography variant="h4" color="white" fontWeight="bold">
                  {illustration.title}
                </VuiTypography>
              </VuiBox>
            )}
            {illustration.description && (
              <VuiBox mb={1}>
                <VuiTypography variant="body2" color="white">
                  {illustration.description}
                </VuiTypography>
              </VuiBox>
            )}
          </VuiBox>
        </Grid>
      </Grid>
    </PageLayout>
  );
}

// Setting default values for the props of IllustrationLayout
IllustrationLayout.defaultProps = {
  color: "info",
  header: "",
  title: "",
  description: "",
  illustration: {},
};

// Typechecking props for the IllustrationLayout
IllustrationLayout.propTypes = {
  color: PropTypes.oneOf(["primary", "secondary", "info", "success", "warning", "error", "dark"]),
  header: PropTypes.node,
  title: PropTypes.string,
  description: PropTypes.string,
  children: PropTypes.node.isRequired,
  illustration: PropTypes.shape({
    image: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
  }),
};

export default IllustrationLayout;
