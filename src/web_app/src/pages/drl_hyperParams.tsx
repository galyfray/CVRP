/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-misused-promises */
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

export function DrlHyperParamsPage() {
    const url = useLocation().pathname;
    const dataset_choice = url.split("/")[2];
    const [
        enablebutton,
        setEnablebutton
    ] = React.useState(true);
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    const navigate = useNavigate();
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
    ] = React.useState<number>(10000);
    const [
        learning_rate,
        setLearning_rate
    ] = React.useState<number>(0.9);
    const [
        batch_size,
        setBatch_size
    ] = React.useState<number>(32);
    const [
        momemtum,
        setMomentum
    ] = React.useState<number>(0.2);
    const [
        param,
        setParam
    ] = React.useState<Types.Hyper_parameters>({
        type  : "drl",
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
        bench_id     : "nothing",
        snapshot_rate: 3
    });

    useEffect(() => {
        logging.info(`Loading ${url}`);
    });

    // eslint-disable-next-line @typescript-eslint/require-await
    const handleClickNext = async() => {
        setEnablebutton(false);
        setParam({
            "type"  : "drl",
            "params": {
                "nb_epochs"    : nb_epochs,
                "pop_size"     : 512,
                "seed"         : 0.5,
                "mutation_rate": 0.2,
                "learning_rate": learning_rate,
                "batch_size"   : batch_size,
                "momentum"     : momemtum
            },
            override     : override_check,
            bench_id     : "nothing",
            snapshot_rate: 3
        });

        axios.post("http://127.0.0.1:5000/operation_params/drl", {
            "d_c"         : dataset_choice,
            "hyper_params": JSON.stringify(param)
        }, {headers: {"Content-Type": "multipart/form-data"}})
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
                    data-testid = "drl_hp_title"
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
                        Epochs
                        </Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <Typography>
                        Learning rate
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
                            defaultValue={param.params.learning_rate}
                            onChange={e => setLearning_rate(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6} sx = {{mt: 3}}>
                        <Typography>
                        Batch size
                        </Typography>
                    </Grid>
                    <Grid item xs={6} sx = {{mt: 3}}>
                        <Typography>
                        Momentum
                        </Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.params.batch_size}
                            onChange={e => setBatch_size(parseInt(e.target.value))}>
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField id="filled-basic" variant="filled"
                            defaultValue={param.params.momentum}
                            onChange={e => setMomentum(parseInt(e.target.value))}>
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
                    sx={{mt: 8}}
                    direction="row"
                    justifyContent="center"
                >
                    <Button variant="contained" sx={{height: 40, width: 120}}
                        disabled={!enablebutton}
                        onClick= {handleClickNext}>
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