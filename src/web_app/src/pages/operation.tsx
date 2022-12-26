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
        enableButton,
        setEnableButton
    ] = React.useState(false);
    const ref = React.useRef<NodeJS.Timeout | null>(null);
    const [
        toggle,
        setToggle
    ] = React.useState<boolean>(true);

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
            console.log(data.length);
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            if (response.data.has_next) {
                return await get_snapshot();
            } else {
                setToggle(false);
                setEnableButton(true);
            }
            return true;
        }
        return await get_snapshot();
    }, [data]);

    useEffect(() => {
        void gather_data();
    }, [gather_data]);

    React.useEffect(() => {
        ref.current = setInterval(() => {
            if (toggle) {
                setPlotdata1(data);
                console.log(plotdata1);
            }
        }, 3000);

        return () => {
            if (ref.current) {
                clearInterval(ref.current);
            }
        };
    }, [
        data,
        plotdata1,
        toggle
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

                <Grid container alignItems="center" spacing={2}>
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
            </Container>
        </React.Fragment>
    );
}