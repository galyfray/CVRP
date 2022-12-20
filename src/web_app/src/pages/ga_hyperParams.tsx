import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import Container from "@mui/material/Container";
import logging from "../config/logging";
import {useNavigate, useLocation} from "react-router-dom";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import * as Types from "../types/data";
import axios from "axios";
import Backdrop from "@mui/material/Backdrop";
import sleep from "../config/sleep_funct";
import CircularProgress from "@mui/material/CircularProgress";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

export function GaHyperParamsPage() {
    const url = useLocation().pathname;
    const dataset_choice = url.split("/")[2];
    const navigate = useNavigate();
    const [
        enablebutton,
        setEnablebutton
    ] = React.useState(true);
    const [
        open,
        setOpen
    ] = React.useState(false);
    const [
        override_check,
        setOverride_check
    ] = React.useState(false);
    const [
        nb_epochs,
        setNb_epochs
    ] = React.useState<number>(1000);
    const [
        pop_size,
        setPop_size
    ] = React.useState<number>(512);
    const [
        seed,
        setSeed
    ] = React.useState<number>(0.5);
    const [
        mutation_rate,
        setMutation_rate
    ] = React.useState<number>(0.2);
    const [
        param,
        setParam
    ] = React.useState<Types.Hyper_parameters>({
        type  : "ga",
        params: {
            "nb_epochs"    : 1000,
            "pop_size"     : 512,
            "seed"         : 0.5,
            "mutation_rate": 0.2,
            "learning_rate": 0.9,
            "batch_size"   : 32,
            "momentum"     : 0.2
        },
        override     : false,
        bench_id     : "0",
        snapshot_rate: 3
    });

    useEffect(() => {
        logging.info(`Loading ${url}`);
    });

    const handleClickNext = () => {
        setEnablebutton(false);
        setParam({
            type  : "ga",
            params: {
                "nb_epochs"    : nb_epochs,
                "pop_size"     : pop_size,
                "seed"         : seed,
                "mutation_rate": mutation_rate,
                "learning_rate": 0.9,
                "batch_size"   : 32,
                "momentum"     : 0.2
            },
            override     : override_check,
            bench_id     : dataset_choice,
            snapshot_rate: 3
        });

        axios.post("http://127.0.0.1:5000/run", {"param": param}, {headers: {"Content-Type": "multipart/form-data"}})
            .then(async() => {
                setOpen(true);
                await sleep(5000);
                // eslint-disable-next-line @typescript-eslint/no-unsafe-call
                navigate(url + "operation");
                setOpen(false);
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
                    data-testid = "ga_hp_title"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{
                        fontWeight: "bold", mb: 5, mt: 5
                    }}
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
                            defaultValue={param.params.nb_epochs}
                            onChange={e => setNb_epochs(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.params.pop_size}
                            onChange={e => setPop_size(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6} sx = {{mt: 3}}>
                        <Typography>
                        Random seed
                        </Typography>
                    </Grid>
                    <Grid item xs={6} sx = {{mt: 3}}>
                        <Typography>
                        Taux de mutation
                        </Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.params.seed}
                            onChange={e => setSeed(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.params.mutation_rate}
                            onChange={e => setMutation_rate(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    data-testid="account-delete-confirm"
                                    onChange={() => setOverride_check(!override_check)}
                                    color="primary"
                                />
                            }
                            label="J'accepte de remplacer les anciens résultats par les nouveaux"
                        />
                    </Grid>
                </Grid>
                <Stack
                    sx={{mt: 5}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}}
                        disabled={!enablebutton}
                        onClick= {handleClickNext}
                    >
                    Suivant
                    </Button>
                </Stack>
                {open && <Backdrop
                    sx={{color: "#fff", zIndex: theme => theme.zIndex.drawer + 1}}
                    open={open}
                >
                    <CircularProgress color="inherit" />
                </Backdrop>
                }
            </Container>
        </React.Fragment>
    );
}
