/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import Container from "@mui/material/Container";
import logging from "../config/logging";
import {useHistory, useRouteMatch} from "react-router-dom";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import {Types} from "../types/data";
import axios from "axios";

export function AlHyperParamsPage() {
    const {url} = useRouteMatch();
    const dataset_choice = url.split("/")[2];
    const history = useHistory();
    const [
        nb_epochs,
        setNb_epochs
    ] = React.useState<number>(1000);
    const [
        pop_size,
        setPop_size
    ] = React.useState<number>(512);
    const [
        crossover_rate,
        setCrossover_rate
    ] = React.useState<number>(0.5);
    const [
        mutation_rate,
        setMutation_rate
    ] = React.useState<number>(0.2);
    const [
        param,
        setParam
    ] = React.useState<Types.AG_hyper_parameters>({
        "nb_epochs"     : 1000,
        "pop_size"      : 512,
        "crossover_rate": 0.5,
        "mutation_rate" : 0.2
    });

    useEffect(() => {
        logging.info(`Loading ${url}`);
    });

    // eslint-disable-next-line @typescript-eslint/require-await
    const handleClickNext = async() => {
        setParam({
            "nb_epochs"     : nb_epochs,
            "pop_size"      : pop_size,
            "crossover_rate": crossover_rate,
            "mutation_rate" : mutation_rate
        });

        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
        axios.post("http://127.0.0.1:5000/operation_params/ag",
            {
                "d_c"         : dataset_choice,
                "hyper_params": JSON.stringify(param)
            },
            {headers: {"Content-Type": "multipart/form-data"}}
        )
            .then(() => {
                history.push(url + "/operation");
            })
            .catch(error => {
                // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
                console.log(error.response);
            });
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
                Entrez les hyperparamètres
                </Typography>
                <Grid container alignItems="center" spacing={2} sx={{ml: 10}}>
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
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.nb_epochs}
                            onChange={e => setNb_epochs(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.pop_size}
                            onChange={e => setPop_size(parseInt(e.target.value))}>
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
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.crossover_rate}
                            onChange={e => setCrossover_rate(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.mutation_rate}
                            onChange={e => setMutation_rate(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                </Grid>

                <Stack
                    sx={{mt: 8}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}}
                        href={url + "operation"}
                        onClick= {handleClickNext}
                    >
                Suivant
                    </Button>
                </Stack>
            </Container>
        </React.Fragment>
    );
}