/* eslint-disable @typescript-eslint/restrict-plus-operands */
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
import {useLocation} from "react-router-dom";
import http from "../http-common";
import Alert from "@mui/material/Alert";

export function RunPage() {
    const url = useLocation().pathname;

    const theme = useTheme();
    const [
        activeStep,
        setActiveStep
    ] = React.useState(0);
    const [
        status,
        setStatus
    ] = React.useState("free");
    const [
        open,
        setOpen
    ] = React.useState(false);
    const [
        datasets,
        setDatasets
    ] = React.useState([
        {
            "name"   : "E-n112-k8-s11.evrp",
            "details": "112 villes - 8 véhicules - 11 stations"
        }
    ]);
    const maxSteps = datasets.length;

    useEffect(() => {
        void (
            async() => {
                await http.get("benchmarks")
                    .then(response => {
                        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
                        setDatasets(response.data);
                    });
            }
        )();
    }, []);

    useEffect(() => {
        void (
            async() => {
                await http.get("status")
                    .then(response => {
                        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
                        setStatus(response.data.status);
                        if (status === "free") {
                            setOpen(false);
                        } else {
                            setOpen(true);
                        }
                    });
            }
        )();
    }, [status]);

    const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === "clickaway") {
            return;
        }
        setOpen(false);
    };

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
                    data-testid = "run_title"
                    gutterBottom
                    sx={{
                        fontWeight: "bold", mb: 5, mt: 5
                    }}
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
                    sx={{mt: 8, mb: 5}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}} disabled={open}
                        href={url + "/" + activeStep.toString() + "/algo_choice"} >
                        Suivant
                    </Button>
                </Stack>
                { open &&
            <Alert onClose={handleClose} severity="warning" sx={{width: "100%"}}>
                Le solveur est actuellement entrain de tourner. Vous ne pouvez pas
                démarrer une nouvelle résolution. <br/>Veuillez patienter !
            </Alert>}
            </Container>
        </React.Fragment>
    );
}