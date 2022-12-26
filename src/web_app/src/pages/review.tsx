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
import {useLocation} from "react-router-dom";
import * as Types from "../types/data";
import logging from "../config/logging";

export function ReviewPage() {
    const url = useLocation().pathname;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const log_id:string = useLocation().state.log_id;
    const dataset_choice = url.split("/")[2];
    const [
        data,
        setData
    ] = React.useState<Array<Types.Point>>([
        {
            "generation": 0,
            "fitness"   : 0
        }
    ]);
    const [
        plotdata1,
        setPlotdata1
    ] = React.useState<Array<Types.Point>>([
        {
            "generation": 0,
            "fitness"   : 0
        }
    ]);
    const [
        start,
        setStart
    ] = React.useState<boolean>(true);
    const [
        enableButton,
        setEnableButton
    ] = React.useState(false);

    useEffect(() => {
        logging.info(`Log_id ${log_id}`);
    });

    useEffect(() => {
        async function getData() {
            setStart(true);
            await http.get(`log/${log_id}`)
                .then(response => {
                    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
                    const individuals:Array<Types.individual> = response.data.snapshots.individuals;
                    const inter:Array<Types.Point> = [];
                    for (let i = 0;i < individuals.length;i++) {
                        inter.push({"generation": i, "fitness": individuals[i].fitness});
                    }
                    console.log(inter);
                    setData(inter);
                });
        }
        void getData();
    }, [
        dataset_choice,
        log_id
    ]);

    const reduce_data = useCallback((step:number, reducer: Array<Types.Point>) => { //  Create a loop function
        setTimeout(() => {
            while (reducer.length > 0) {
                reducer = reducer.slice(step, reducer.length);
                if (reducer.slice(0, step).length > 0) {
                    console.log("plot 1", reducer.slice(0, step));
                    setPlotdata1(reducer.slice(0, step));
                }
                reducer = reduce_data(step, reducer);
                if (reducer.length - step < 0) {
                    step = reducer.length;
                }
                if (step === 0) {
                    setEnableButton(true);
                    break;
                }
            }
        }, 5000);

        return reducer;
    }, []);

    useEffect(() => {
        if (data.length > 1) {
            const step = data.length / 2; // 25 comme step plus tard avec de vrais données;
            const reducer = data;
            setPlotdata1(reducer.slice(0, step));
            console.log("plot 1", reducer.slice(0, step));
            reduce_data(step, reducer);
        }
    },
    [
        data,
        reduce_data
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
                        fontWeight: "bold", mb: 2, mt: 12
                    }}
                >
                    Evolution de la fitness au cours des générations
                </Typography>

                {start && <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={12} sx={{mt: 5, ml: 33}}>
                        <LineChart
                            width={600}
                            height={300}
                            data={plotdata1}
                            margin={{
                                top   : 5,
                                right : 30,
                                left  : 20,
                                bottom: 3
                            }}
                        >
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" strokeWidth={2} />
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="generation" type="number"/>
                            <YAxis dataKey="fitness" type="number"/>
                            <Tooltip />
                            <Legend />
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