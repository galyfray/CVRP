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
import Badge from "@mui/material/Badge";
import Stack from "@mui/material/Stack";
export function OperationPage() {
    const url = useLocation().pathname;
    const [
        nb_epochs,
        setNb_epochs
    ] = React.useState(1);
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
        enableButton,
        setEnableButton
    ] = React.useState(false);
    const ref = React.useRef<NodeJS.Timeout | null>(null);
    const [
        toggle,
        setToggle
    ] = React.useState<boolean>(true);

    const update_plot = useCallback(async() => {
        const response = await http.get("snapshot");
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        const snapshot:Array<Types.individual> = response.data.snapshot;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
        setNb_epochs(response.data.generation);
        const graph_data:Array<Types.Point> = [];
        for (let i = 0;i < snapshot.length;i++) {
            graph_data.push(
                {"generation": i, "fitness": snapshot[i].fitness}
            );
        }
        setPlotdata1(graph_data);
        console.log("plot data", plotdata1);
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        if (!response.data.has_next) {
            setToggle(false);
            setEnableButton(true);
        }
    }, [plotdata1]);

    useEffect(() => {
        ref.current = setInterval(() => {
            if (toggle) {
                void update_plot();
            }
        }, 3000);

        return () => {
            if (ref.current) {
                clearInterval(ref.current);
            }
        };
    }, [
        toggle,
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
                        fontWeight: "bold", mt: 12, mb: 2
                    }}
                >
                    Evolution de la fitness au cours des générations
                </Typography>
                <Stack direction="row" justifyContent="center">
                    <Typography variant="h6" fontStyle="italic">
                            Génération
                    </Typography>
                    <Badge badgeContent={nb_epochs} max={10000} color="secondary" sx={{ml: 2}}>
                    </Badge>
                </Stack>

                <Grid container alignItems="center" spacing={2}>
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
            </Container>
        </React.Fragment>
    );
}