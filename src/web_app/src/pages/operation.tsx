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

const datasets = [
    "E-n112-k8-s11.evrp",
    "E-n29-k4-s7.evrp",
    "E-n30-k3-s7.evrp",
    "E-n35-k3-s5.evrp",
    "E-n37-k4-s4.evrp",
    "E-n60-k5-s9.evrp",
    "E-n89-k7-s13.evrp",
    "F-n140-k5-s5.evrp",
    "F-n49-k4-s4.evrp",
    "F-n80-k4-s8.evrp",
    "M-n110-k10-s9.evrp",
    "M-n126-k7-s5.evrp",
    "M-n163-k12-s12.evrp",
    "M-n212-k16-s12.evrp",
    "X-n1006-k43-s5.evrp",
    "X-n147-k7-s4.evrp",
    "X-n221-k11-s7.evrp",
    "X-n360-k40-s9.evrp",
    "X-n469-k26-s10.evrp",
    "X-n577-k30-s4.evrp",
    "X-n698-k75-s13.evrp",
    "X-n759-k98-s10.evrp",
    "X-n830-k171-s11.evrp",
    "X-n920-k207-s4.evrp"
];

export function OperationPage() {
    const url = useLocation().pathname;
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
        checking,
        setChecking
    ] = React.useState<boolean>(true);
    const [
        enableButton,
        setEnableButton
    ] = React.useState(false);

    const gather_data = useCallback(async() => {
        async function get_snapshot(): Promise<boolean> {
            const response = await http.get("snapshot");
            const graph_data:Types.Point = {
                // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
                "generation": response.data.generation,
                // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
                "fitness"   : response.data.snapshot[0].fitness
            };
            setData(data.concat([graph_data]));
            console.log(graph_data);
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            if (response.data.has_next) {
                return await get_snapshot();
            } else {
                setChecking(false);
                setEnableButton(true);
            }
            return true;
        }
        return await get_snapshot();
    }, [data]);

    const update_plot = useCallback(() => {
        const myInterval = setInterval(() => {
            setPlotdata1(data);
        }, 5000);

        if (!checking) {
            clearInterval(myInterval);
        }
    }, []);

    useEffect(() => {
        setStart(true);
        for (let i = 0;i < 8;i++) {
            void gather_data();
        }
        if (data.length > 4) { // 25 comme step plus tard avec de vrais données;
            update_plot();
        }
    },
    [
        data,
        gather_data,
        update_plot
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
                    Evolution de la fitness au cours des générations
                </Typography>

                {start && <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={12} sx={{mt: 7, ml: 33}}>
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