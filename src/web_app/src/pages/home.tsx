import React from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import {
    Button, Container, Typography
} from "@mui/material";
import ArrowRightIcon from "@mui/icons-material/ArrowRight";
import Stack from "@mui/material/Stack";
import cvrp_image from "../images/cvrp.PNG";
import {AppbarStyle} from "../components/appBar";

export function HomePage() {
    return (
        <React.Fragment>
            <GlobalStyles styles={{
                ul: {
                    margin: 0, padding: 0, listStyle: "none"
                }
            }} />
            <CssBaseline />
            <AppbarStyle/>
            <Container disableGutters component="main" maxWidth="md" sx={{pt: 8, ml: 20}}>
                <Typography
                    variant="h4"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold", mb: 5}}
                >
          ECVRPTW Solver
                </Typography>
                <Grid container justifyContent="space-between"
                    alignItems="center" sx={{mt: 20, m: 2}} >
                    <Grid item xs={7}>
                        <Typography variant="h6" sx={{fontWeight: "bold"}} align="justify" color="text.secondary" component="p">
          ECVRPTW Solver est un outil qui permet de résoudre les problèmes d'acheminement
          des véhicules électriques avec fenêtres de temps et contraintes de capacités.
                            <br/>Il construit des itinéraires de véhicules qui visitent chaque client
          exactement une fois et qui respectent les contraintes de capacité et
          de temps spécifiées par l'utilisateur.
          Les résultats sont affichés sous forme de graphe (carte) et de texte.
                        </Typography>
                        <Link href="/about" sx={{mt: 2}} >Lire la suite</Link>
                    </Grid>
                    <Grid item xs={4} sx={{ml: 1}}>
                        <img src={cvrp_image} alt="cvrp_image" width= "100%" />
                    </Grid>
                </Grid>
                <Stack
                    sx={{mt: 3}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}} href="/run" >
                Démarrer
                        <ArrowRightIcon/>
                    </Button>
                </Stack>
            </Container>
        </React.Fragment>
    );
}
