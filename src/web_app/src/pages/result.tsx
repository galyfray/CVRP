/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-floating-promises */
import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import {
    Box, Button, Container, Typography
} from "@mui/material";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {useLocation} from "react-router-dom";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from "recharts";
import RoadGraph from "../components/roadGraph";
import {d3Types} from "../types/d3Types";
import {Types} from "../types/data";


export function ResultPage() {
    const url = useLocation().pathname;
    const dataset_choice = url.split("/")[2];
    const method_choice = url.split("/")[4];
    const [
        bench_id,
        setBench_id
    ] = React.useState("");
    const [
        dataXY,
        setDataXY
    ] = React.useState<[Types.Received_data]>([
        {
            "time"   : 0,
            "fitness": 0
        }
    ]);
    const [
        length,
        setLength
    ] = React.useState(1);
    const [
        graph_data,
        set_graph_data
    ] = React.useState<d3Types.d3Graph>(
        {nodes: [], links: []});
    const [
        method_str,
        setMethod_str
    ] = React.useState("");

    useEffect(() => {
        (
            async() => {
                setMethod_str(method_choice);
                await http.get(`get_points?${dataset_choice}/${method_choice}`)
                    .then(response1 => {
                        set_graph_data(response1.data);
                    });
                await http.get(`get_performance?${dataset_choice}/${method_choice}`)
                    .then(response2 => {
                        setDataXY(response2.data.data);
                        setLength(response2.data.data.length);
                        setBench_id(response2.data.bench_id);
                    });
            }
        )();
    }, [
        dataset_choice,
        method_choice,
        length
    ]);
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
                <Grid container alignItems="center" spacing={2}>
                    {/*
                    <Grid item xs={6} sx={{mb:0}}>
                        <RoadGraph width={450} height={200} graph={graph_data}/>
                    </Grid>
                    */
                    }
                    <Grid item xs={6} sx={{mb: 0}}>
                        <LineChart
                            width={450}
                            height={200}
                            data={dataXY}
                            margin={{
                                top   : 5,
                                right : 30,
                                left  : 20,
                                bottom: 3
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="time" />
                            <YAxis dataKey="fitness" />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" />
                        </LineChart>
                    </Grid>
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
                                    ID : {bench_id}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography color="#808080" sx={{ml: 2}}>
                                    Algorithme : {method_str}
                                </Typography>
                            </Grid>
                            <Grid item xs={6} color="#808080">
                                <Typography sx={{mr: 2}}>
                                    Fitness : {dataXY[length - 1].fitness}
                                </Typography>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography color="#808080" sx={{ml: 2}}>
                                    Temps d'exécution : {dataXY[length - 1].time}
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
                                    }} href="/run" >
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