import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import GlobalStyles from "@mui/material/GlobalStyles";
import Typography from "@mui/material/Typography";
import React, {useEffect} from "react";
import {useTheme} from "@mui/material/styles";
import {AppbarStyle} from "../components/appBar";
import Stack from "@mui/material/Stack";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import logging from "../config/logging";
import {useRouteMatch} from "react-router-dom";

const datasets = [
    {
        "name"   : "E-n112-k8-s11.evrp",
        "details": "112 villes - 8 véhicules - 11 stations"
    },
    {
        "name"   : "E-n29-k4-s7.evrp",
        "details": "29 villes - 4 véhicules - 7 stations"
    },
    {
        "name"   : "E-n30-k3-s7.evrp",
        "details": "30 villes - 3 véhicules - 7 stations"
    },
    {
        "name"   : "E-n35-k3-s5.evrp",
        "details": "35 villes - 3 véhicules - 5 stations"
    },
    {
        "name"   : "E-n37-k4-s4.evrp",
        "details": "37 villes - 4 véhicules - 4 stations"
    },
    {
        "name"   : "E-n60-k5-s9.evrp",
        "details": "60 villes - 5 véhicules - 9 stations"
    },
    {
        "name"   : "E-n89-k7-s13.evrp",
        "details": "89 villes - 7 véhicules - 13 stations"
    },
    {
        "name"   : "F-n140-k5-s5.evrp",
        "details": "140 villes - 5 véhicules - 5 stations"
    },
    {
        "name"   : "F-n49-k4-s4.evrp",
        "details": "49 villes - 4 véhicules - 4 stations"
    },
    {
        "name"   : "F-n80-k4-s8.evrp",
        "details": "80 villes - 4 véhicules - 8 stations"
    },
    {
        "name"   : "M-n110-k10-s9.evrp",
        "details": "110 villes - 10 véhicules - 9 stations"
    },
    {
        "name"   : "M-n126-k7-s5.evrp",
        "details": "126 villes - 7 véhicules - 5 stations"
    },
    {
        "name"   : "M-n163-k12-s12.evrp",
        "details": "163 villes - 12 véhicules - 12 stations"
    },
    {
        "name"   : "M-n212-k16-s12.evrp",
        "details": "212 villes - 16 véhicules - 12 stations"
    },
    {
        "name"   : "X-n1006-k43-s5.evrp",
        "details": "1006 villes - 43 véhicules - 5 stations"
    },
    {
        "name"   : "X-n147-k7-s4.evrp",
        "details": "147 villes - 7 véhicules - 4 stations"
    },
    {
        "name"   : "X-n221-k11-s7.evrp",
        "details": "221 villes - 11 véhicules - 7 stations"
    },
    {
        "name"   : "X-n360-k40-s9.evrp",
        "details": "360 villes - 40 véhicules - 9 stations"
    },
    {
        "name"   : "X-n469-k26-s10.evrp",
        "details": "469 villes - 26 véhicules - 10 stations"
    },
    {
        "name"   : "X-n577-k30-s4.evrp",
        "details": "577 villes - 30 véhicules - 4 stations"
    },
    {
        "name"   : "X-n698-k75-s13.evrp",
        "details": "698 villes - 75 véhicules - 13 stations"
    },
    {
        "name"   : "X-n759-k98-s10.evrp",
        "details": "759 villes - 98 véhicules - 10 stations"
    },
    {
        "name"   : "X-n830-k171-s11.evrp",
        "details": "830 villes - 171 véhicules - 11 stations"
    },
    {
        "name"   : "X-n920-k207-s4.evrp",
        "details": "920 villes - 207 véhicules - 4 stations"
    }
];

export function RunPage() {
    const {url} = useRouteMatch();

    useEffect(() => {
        logging.info(`Loading ${url}`);
    });

    const theme = useTheme();
    const [
        activeStep,
        setActiveStep
    ] = React.useState(0);
    const maxSteps = datasets.length;

    const handleNext = () => {
        setActiveStep(prevActiveStep => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep(prevActiveStep => prevActiveStep - 1);
    };

    return (
        <React.Fragment>
            <GlobalStyles styles={{
                ul: {
                    margin: 0, padding: 0, listStyle: "none"
                }
            }} />
            <CssBaseline />
            <AppbarStyle/>
            <Container component="main" maxWidth="md" sx={{pt: 8}}>
                <Typography
                    variant="h4"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold", mb: 5}}
                >
          Choisir un jeu de données
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Typography variant="h6" sx={{fontWeight: "bold"}} align="center"
                        >
                            {datasets[activeStep].name}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sx={{mt: 2}}>
                        <MobileStepper
                            steps={maxSteps}
                            position="static"
                            activeStep={activeStep}
                            nextButton={
                                <Button
                                    size="small"
                                    onClick={handleNext}
                                    disabled={activeStep === maxSteps - 1}
                                >
                                    {theme.direction === "rtl" ? <KeyboardArrowLeft /> : <KeyboardArrowRight />
                                    }
                                </Button>
                            }
                            backButton={
                                <Button size="small" onClick={handleBack} disabled={activeStep === 0}>
                                    {theme.direction === "rtl" ? <KeyboardArrowRight /> : <KeyboardArrowLeft />
                                    }
                                </Button>
                            }
                        />
                    </Grid>
                    <Grid item xs={12} sx={{mt: 2}}>
                        <Typography variant="body1" align="center"
                        >
                            {datasets[activeStep].details}
                        </Typography>
                    </Grid>
                </Grid>

                <Stack
                    sx={{mt: 8}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}}
                        href={url + "/" + activeStep.toString() + "/algo_choice"} >
                Suivant
                    </Button>
                </Stack>
            </Container>
        </React.Fragment>
    );
}