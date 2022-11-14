import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import {
    Box, Button, Container, Typography
} from "@mui/material";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {useRouteMatch} from "react-router-dom";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from "recharts";


export function ResultPage() {
    const {url} = useRouteMatch();
    const dataset_choice = url.split("/")[2];
    const method_choice = url.split("/")[4];
    const [
        start,
        setStart
    ] = React.useState(false);
    const [
        dataXY,
        setDataXY
    ] = React.useState();
    const [
        method_str,
        setMethod_str
    ] = React.useState("");
    const [
        details,
        setDetails
    ] = React.useState({
        "fitness"        : 3780,
        "temps_execution": "4 min 52s"
    });

    useEffect(() => {
        setStart(true);
        setMethod_str(method_choice);
    }, [
        dataset_choice,
        method_choice
    ]);

    const getData = async() => {
        const response1 = await http.get("/result");
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        setDataXY(response1.data);
    };

    if (start) {
        // eslint-disable-next-line @typescript-eslint/no-use-before-define
        void getData();
    }

    return (
        <React.Fragment>
            <GlobalStyles styles={{
                ul: {
                    margin: 0, padding: 0, listStyle: "none"
                }
            }} />
            <CssBaseline />
            <AppbarStyle/>
            <Container disableGutters component="main" maxWidth="md" sx={{pt: 3, ml: 20}}>
                <Typography
                    variant="h4"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold", mb: 2}}
                >
                    Résultat
                </Typography>
                <Grid sx = {{ml: 25, mb: 2}}>
                    <LineChart
                        width={450}
                        height={250}
                        data={dataXY}
                        margin={{
                            top   : 5,
                            right : 30,
                            left  : 20,
                            bottom: 5
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="x" />
                        <YAxis dataKey="y" />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="y" stroke="#82ca9d" />
                    </LineChart>
                </Grid>
                <Grid sx={{ml: 40, mb: 5}}>
                    <Box
                        sx={{
                            width          : 300,
                            height         : 210,
                            backgroundColor: "black"
                        }}
                    >
                        <Grid container alignItems="center" spacing={2}>
                            <Grid item xs={12}>
                                <Typography color="#FFFFFF" sx={{ml: 2}}>
                                    ID :
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography color="#808080" sx={{ml: 2}}>
                                    Algorithme : {method_str}
                                </Typography>
                            </Grid>
                            <Grid item xs={6} color="#808080">
                                <Typography sx={{mr: 2}}>
                                    Fitness : {details.fitness}
                                </Typography>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography color="#808080" sx={{ml: 2}}>
                                    Temps d'exécution : {details.temps_execution}
                                </Typography>
                            </Grid>
                            <Grid item alignItems="center" xs={12}>
                                <Button variant="contained" sx={{
                                    height: 20, width: 260, ml: 2.5
                                }} href="/logs" >
                                    Plus de détails
                                </Button>
                            </Grid>
                            <Grid item alignItems="center" xs={12}>
                                <Button variant="contained"
                                    sx={{
                                        height: 20, width: 260, backgroundColor: "#434343", ml: 2.5
                                    }} href="/" >
                                    <Typography color="#5455AF">
                                        Relancer
                                    </Typography>
                                </Button>
                            </Grid>
                        </Grid>
                    </Box>
                </Grid>
            </Container>
        </React.Fragment>
    );
}