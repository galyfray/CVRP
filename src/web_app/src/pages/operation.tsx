/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-floating-promises */
import React, {useCallback, useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from "recharts";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import RoadGraph from "../components/roadGraph";
import {useLocation} from "react-router-dom";
import * as d3Types from "../types/d3Types";
import * as Types from "../types/data";
import sleep from "../config/sleep_funct";

export function OperationPage() {
    const url = useLocation().pathname;
    const dataset_choice = url.split("/")[2];
    const method_choice = url.split("/")[4];
    const [
        method_str,
        setMethod_str
    ] = React.useState("");
    const [
        data,
        setData
    ] = React.useState<d3Types.d3Graph>(
        {nodes: [], links: []});
    const [
        data1,
        setData1
    ] = React.useState<[Types.Received_data]>([
        {
            "time"   : 0,
            "fitness": 0
        }
    ]);
    const [
        data2,
        setData2
    ] = React.useState<[Types.Received_data]>([
        {
            "time"   : 0,
            "fitness": 0
        }
    ]);
    const [
        data3,
        setData3
    ] = React.useState<[Types.Received_data]>([
        {
            "time"   : 0,
            "fitness": 0
        }
    ]);
    const [
        data4,
        setData4
    ] = React.useState<[Types.Received_data]>([
        {
            "time"   : 0,
            "fitness": 0
        }
    ]);
    const [
        start,
        setStart
    ] = React.useState<boolean>(false);
    const [
        enableButton,
        setEnableButton
    ] = React.useState(false);
    useEffect(() => {
        (
            async() => {
                await http.get(`get_first_sol?${dataset_choice}`)
                    .then(response_f => {
                        setData(response_f.data);
                        if (method_choice === "ga") {
                            setMethod_str("Genetic Algorithm");
                        } else {
                            setMethod_str("Deep Reinforcement Learning");
                        }
                    });
            }
        )();
    }, [
        dataset_choice,
        method_choice
    ]);

    useEffect(() => {
        (
            async() => {
                await sleep(10000)
                    .then(
                        async() => {
                            await http.get(`get_snapshots?${dataset_choice}&${method_choice}`)
                                .then(response => {
                                    console.log(typeof response.data.data);
                                    setData1(response.data.data);

                                    checking(response.data.data.length);
                                    setStart(true);
                                });
                        });
            }
        )();
    }, [
        dataset_choice,
        method_choice
    ]);

    function checking(length:number) {
        if (length === 0) {
            setEnableButton(true);
            setStart(false);
        }
    }

    const update_plot1 = useCallback(async() => {
        const response = await http.get(`get_snapshots?${dataset_choice}&${method_choice}`);
        setData1(response.data.data);
    }, [
        dataset_choice,
        method_choice
    ]);


    const update_plot2 = useCallback(async() => {
        const response = await http.get(`get_snapshots?${dataset_choice}&${method_choice}`);
        setData2(response.data.data);
    }, [
        dataset_choice,
        method_choice
    ]);

    const update_plot3 = useCallback(async() => {
        const response = await http.get(`get_snapshots?${dataset_choice}&${method_choice}`);
        setData3(response.data.data);
    }, [
        dataset_choice,
        method_choice
    ]);


    const update_plot4 = useCallback(async() => {
        const response = await http.get(`get_snapshots?${dataset_choice}&${method_choice}`);
        setData4(response.data.data);
    }, [
        dataset_choice,
        method_choice
    ]);

    const update_plots = useCallback(async() => {
        await sleep(5000);
        await update_plot2();
        await sleep(5000);
        await update_plot3();
        await sleep(5000);
        await update_plot4();
        await sleep(5000);
        await update_plot1();
    }, [
        update_plot1,
        update_plot2,
        update_plot3,
        update_plot4
    ]);

    useEffect(() => {
        //While(start){
        let i = 0;
        while (start && i < 2) {
            update_plots();
            i++;
            if (i === 2) {
                setEnableButton(true);
            }
        }
    }, [
        start,
        update_plots
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
            <Container component="main" sx={{pt: 2, ml: 3}}>
                <Typography
                    variant="h5"
                    align="center"
                    data-testid = "operation_title"
                    color="text.primary"
                    gutterBottom
                    sx={{
                        fontWeight: "bold", mr: 9, mb: 2
                    }}
                >
                    {method_str}
                </Typography>

                {/**
           * {first && <Grid sx={{mb:0}}>
                            <RoadGraph width={450} height={200} graph={data}/>
                        </Grid>}
           */
                }
                {start && <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={6} sx={{mb: 0}}>
                        <LineChart
                            width={450}
                            height={200}
                            data={data1}
                            margin={{
                                top   : 5,
                                right : 30,
                                left  : 20,
                                bottom: 3
                            }}
                        >
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" strokeWidth={2} />
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="time" />
                            <YAxis dataKey="fitness" />
                            <Tooltip />
                            <Legend />

                        </LineChart>
                    </Grid>
                    <Grid item xs={6} sx={{mb: 0}}>
                        <LineChart
                            width={450}
                            height={200}
                            data={data2}
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
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" strokeWidth={2}/>
                        </LineChart>
                    </Grid>
                    <Grid item xs={6} sx={{mb: 0}}>
                        <LineChart
                            width={450}
                            height={200}
                            data={data3}
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
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" strokeWidth={2}/>
                        </LineChart>
                    </Grid>
                    <Grid item xs={6} sx={{mb: 0}}>
                        <LineChart
                            width={450}
                            height={200}
                            data={data4}
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
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" strokeWidth={2}/>
                        </LineChart>
                    </Grid>
                    <Grid item xs={8}></Grid>
                    <Grid item xs={4} >
                        {enableButton && <Button variant="contained" color="success" sx={{
                            height: 25, width: 200, mr: 0
                        }}
                        href={url + "/result"}
                        >
                    Continuer
                        </Button>}
                    </Grid>
                </Grid>
                }

            </Container>
        </React.Fragment>
    );
}