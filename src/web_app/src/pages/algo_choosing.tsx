import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import Container from "@mui/material/Container";
import logging from "../config/logging";
import {useLocation} from "react-router-dom";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import algo_gene_image from "../images/algo_gene.png";
import drl_image from "../images/drl.png";

export function AlgoChoosingPage() {
    const url = useLocation().pathname;

    useEffect(() => {
        logging.info(`Loading ${url}`);
    });

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
                    data-testid = "algo_choice_title"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold", mb: 5}}
                >
                    Choisir un algorithme pour la résolution
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={6}>
                        <Stack alignItems="center" >
                            <Link href={url + "/ga/"}>
                                <img src={algo_gene_image} alt="algo_gene_image" width= "75%"/>
                            </Link>
                            <Typography gutterBottom variant="h6" align="center" component="div" sx={{mr: 5}}>
                                Algorithme Génétique
                            </Typography>
                        </Stack>
                    </Grid>
                    <Grid item xs={6}>
                        <Stack alignItems="center"
                        >
                            <Link href={url + "/drl/"}>
                                <img src={drl_image} alt="drl_image" width= "180%"/>
                            </Link>
                            <Typography gutterBottom variant="h6" align="center" component="div" sx={{ml: 20}}>
                                Deep Reinforcement Learning
                            </Typography>
                        </Stack>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    );
}