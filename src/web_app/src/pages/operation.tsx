import React, {useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from "recharts";
import {useRouteMatch} from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";

export function OperationPage() {
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
            <Container component="main" sx={{pt: 2, ml: 3}}>
                <Typography
                    variant="h5"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{
                        fontWeight: "bold", mr: 9, mb: 2
                    }}
                >
                    {method_str}
                </Typography>

                <Grid container alignItems="center" spacing={2}>
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
                            <XAxis dataKey="x" />
                            <YAxis dataKey="y" />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="y" stroke="#82ca9d" />
                        </LineChart>
                    </Grid>
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
                            <XAxis dataKey="x" />
                            <YAxis dataKey="y" />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="y" stroke="#82ca9d" />
                        </LineChart>
                    </Grid>
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
                            <XAxis dataKey="x" />
                            <YAxis dataKey="y" />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="y" stroke="#82ca9d" />
                        </LineChart>
                    </Grid>
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
                            <XAxis dataKey="x" />
                            <YAxis dataKey="y" />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="y" stroke="#82ca9d" />
                        </LineChart>
                    </Grid>
                    <Grid item xs={8}></Grid>
                    <Grid item xs={4} >
                        <Button variant="contained" color="success" sx={{
                            height: 25, width: 200, mr: 0
                        }}
                        href={url + "/result"}
                        >
                    Continuer
                        </Button>
                    </Grid>
                </Grid>

            </Container>
        </React.Fragment>
    );
}