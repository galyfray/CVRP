import React, { useEffect } from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import { AppbarStyle } from "../components/appBar";
import Container from "@mui/material/Container";
import logging from "../config/logging";
import { useHistory, useRouteMatch } from "react-router-dom";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { Types } from "../types/data";
import axios from "axios";

export function DrlHyperParamsPage() {
    let {url} = useRouteMatch();
    const dataset_choice = url.split("/")[2]
    const history = useHistory();
    const [nb_epochs, setNb_epochs] = React.useState<number>(10000)
    const [learning_rate, setLearning_rate] = React.useState<number>(0.9)
    const [batch_size, setBatch_size] = React.useState<number>(32)
    const [momemtum, setMomentum] = React.useState<number>(0.2)
    const [param, setParam] = React.useState<Types.DRL_hyper_parameters>({
        "nb_epochs" : 10000,
        "learning_rate" : 0.9,
        "batch_size" : 32,
        "momentum" : 0.2
    });

    useEffect(() => {
        logging.info(`Loading ${url}`);
    })

    const handleClickNext = async() => {
        setParam({
            "nb_epochs" : nb_epochs,
            "learning_rate" : learning_rate,
            "batch_size" : batch_size,
            "momentum" : momemtum
        })

        axios.post("http://127.0.0.1:5000/operation_params/drl", {
            'd_c': dataset_choice, 
            'hyper_params' : JSON.stringify(param)
        }, {
                headers: {
                    'Content-Type': "multipart/form-data" 
                }
        })
        .then(() => {
            history.push(url + "/operation");
        })
        .catch(error => {
            console.log(error.response)
        });
    }

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
                    defaultValue={param.nb_epochs}
                    onChange={e => setNb_epochs(parseInt(e.target.value))}>
                    </TextField>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" 
                    defaultValue={param.learning_rate}
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
                    defaultValue={param.batch_size}
                    onChange={e => setBatch_size(parseInt(e.target.value))}>
                    </TextField>
                </Grid>
                <Grid item xs={6}>
                    <TextField id="filled-basic" variant="filled" 
                    defaultValue={param.momentum}
                    onChange={e => setMomentum(parseInt(e.target.value))}>
                    </TextField>
                </Grid>
            </Grid>

            <Stack
              sx={{ mt: 8 }}
              direction="row"
              justifyContent="center"
            >
              <Button variant="contained" sx={{ height: 40, width:120 }} 
                href={url+ "operation"} 
                onClick= {handleClickNext}>
                Suivant
              </Button>
            </Stack>
        </Container>
        </React.Fragment>
    );
}