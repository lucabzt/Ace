/* eslint-disable react/prop-types */
// Vision UI Dashboard React components
import VuiBox from "../../../components/VuiBox";
import VuiTypography from "../../../components/VuiTypography";
import VuiAvatar from "../../../components/VuiAvatar";
import VuiBadge from "../../../components/VuiBadge";

// Images
import avatar1 from "../../../assets/images/avatar1.png";
import avatar2 from "../../../assets/images/avatar2.png";
import avatar3 from "../../../assets/images/avatar3.png";
import avatar4 from "../../../assets/images/avatar4.png";
import avatar5 from "../../../assets/images/avatar5.png";
import avatar6 from "../../../assets/images/avatar6.png";

function Author({ image, name, email }) {
  return (
    <VuiBox display="flex" alignItems="center" px={1} py={0.5}>
      <VuiBox mr={2}>
        <VuiAvatar src={image} alt={name} size="sm" variant="rounded" />
      </VuiBox>
      <VuiBox display="flex" flexDirection="column">
        <VuiTypography variant="button" color="white" fontWeight="medium">
          {name}
        </VuiTypography>
        <VuiTypography variant="caption" color="text">
          {email}
        </VuiTypography>
      </VuiBox>
    </VuiBox>
  );
}

function PnL({ value }) {
  return (
    <VuiTypography variant="caption" fontWeight="medium" color="white">
      {value} €
    </VuiTypography>
  );
}

function DaysPlayed({ value }) {
  return (
    <VuiTypography variant="caption" fontWeight="medium" color="white">
      {value} days
    </VuiTypography>
  );
}

export default {
  columns: [
    { name: "author", align: "left" },
    { name: "pnl", align: "left" },
    { name: "status", align: "center" },
    { name: "daysPlayed", align: "center" },
    { name: "action", align: "center" },
  ],

  rows: [
    {
      author: <Author image={avatar4} name="Sebastian Rogg" email="sebastian@simmmple.com" />,
      pnl: <PnL value={1500} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Online"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={45} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar2} name="Luca Bozzetti" email="luca@simmmple.com" />,
      pnl: <PnL value={-300} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Offline"
          size="xs"
          container
          sx={({ palette: { white }, borders: { borderRadius, borderWidth } }) => ({
            background: "unset",
            border: `${borderWidth[1]} solid ${white.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={30} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar3} name="Kyle Kreuter" email="kyle@simmmple.com" />,
      pnl: <PnL value={750} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Online"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={60} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar1} name="Paul Vorderbrügge" email="paul@simmmple.com" />,
      pnl: <PnL value={1000} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Online"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={80} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar5} name="Markus Huber" email="markus@simmmple.com" />,
      pnl: <PnL value={-500} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Offline"
          size="xs"
          container
          sx={({ palette: { white }, borders: { borderRadius, borderWidth } }) => ({
            background: "unset",
            border: `${borderWidth[1]} solid ${white.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={25} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar6} name="Jonas Hörter" email="jonas@simmmple.com" />,
      pnl: <PnL value={300} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Offline"
          size="xs"
          container
          sx={({ palette: { white }, borders: { borderRadius, borderWidth } }) => ({
            background: "unset",
            border: `${borderWidth[1]} solid ${white.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={15} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
    {
      author: <Author image={avatar3} name="Matthias Meierlohr" email="matthias@simmmple.com" />,
      pnl: <PnL value={2000} />,
      status: (
        <VuiBadge
          variant="standard"
          badgeContent="Online"
          color="success"
          size="xs"
          container
          sx={({ palette: { white, success }, borders: { borderRadius, borderWidth } }) => ({
            background: success.main,
            border: `${borderWidth[1]} solid ${success.main}`,
            borderRadius: borderRadius.md,
            color: white.main,
          })}
        />
      ),
      daysPlayed: <DaysPlayed value={100} />,
      action: (
        <VuiTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
          Edit
        </VuiTypography>
      ),
    },
  ],
};
