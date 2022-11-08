import React, { useEffect } from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import { AppbarStyle } from "../components/appBar";
import Container from "@mui/material/Container";
import logging from "../config/logging";
import { useRouteMatch } from "react-router-dom";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";

export function AlHyperParamsPage() {
    let {url} = useRouteMatch();

    useEffect(() => {
        logging.info(`Loading ${url}`);
    })

    return (
      <React.Fragment>
        <GlobalStyles styles={{ ul: { margin: 0, padding: 0, listStyle: 'none' } }} />
        <CssBaseline />
        <AppbarStyle/>
        <Container component="main" maxWidth="md" sx={{ pt: 8 }}>
        <Typography
            variant="h4"
            align="center"
            color="text.primary"
            gutterBottom
            sx={{ fontWeight: 'bold', mb:5}}
            >
                Entrez les hyperparamètres
            </Typography>
            <Grid container alignItems="center" spacing={2} sx={{ml:10}}>
                <Grid item xs={6}>
                    <Typography>
                        Nombre de générations
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography>
                        Taille de la population
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" defaultValue={1000}>
                    </TextField>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" defaultValue={512}>
                    </TextField>
                </Grid>
                <Grid item xs={6} sx = {{mt: 3}}>
                    <Typography>
                        Taux de croisement
                    </Typography>
                </Grid>
                <Grid item xs={6} sx = {{mt: 3}}>
                    <Typography>
                        Taux de mutation
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" defaultValue={0.5}>
                    </TextField>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" defaultValue={0.2}>
                    </TextField>
                </Grid>
            </Grid>

            <Stack
              sx={{ mt: 8 }}
              direction="row"
              justifyContent="center"
            >
              <Button variant="contained" sx={{ height: 40, width:120 }} 
                href={url+ "resolution"} >
                Suivant
              </Button>
            </Stack>
        </Container>
        </React.Fragment>
    );
}