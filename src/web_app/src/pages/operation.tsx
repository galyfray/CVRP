import React, {useCallback, useEffect} from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LabelList
} from "recharts";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import {useLocation} from "react-router-dom";
import * as Types from "../types/data";
import Badge from "@mui/material/Badge";
import Stack from "@mui/material/Stack";
import {
    getMaxX,
    getMaxY,
    getMinFitness, getMinX, getMinY, getRandomColor
} from "../config/utils";
import Avatar from "@mui/material/Avatar";

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
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const gen:number = useLocation().state.nb_epochs;
    const dataset_choice = url.split("/")[2];
    const nb_cars = datasets[parseInt(dataset_choice)].split("-")[2][1];
    const [
        nb_epochs,
        setNb_epochs
    ] = React.useState(1);
    const [
        colors,
        setColors
    ] = React.useState<Array<string>>([]);
    const [
        graphdata,
        setgraphdata
    ] = React.useState([
        {
            "id"  : "",
            "data": [
                {
                    "node": 0,
                    "x"   : 0,
                    "y"   : 0
                }
            ]
        }
    ]);
    const [
        nodes,
        setNodes
    ] = React.useState<{ [key: string]: [number, number] }>(
        {
            "0": [
                0,
                0
            ]
        }
    );
    const [
        plotdata,
        setplotdata
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
    const [
        toggle,
        setToggle
    ] = React.useState<boolean>(true);

    useEffect(() => {
        async function getNodes() {
            await http.get(`benchmark/${datasets[parseInt(dataset_choice)]}`)
                .then(response => {
                    // eslint-disable-next-line
                    setNodes(response.data["NODES"]);
                });
        }
        void getNodes();
    }, [dataset_choice]);

    useEffect(() => {
        const inter:Array<string> = [];
        for (let i = 0;i < parseInt(nb_cars);i++) {
            const c = getRandomColor();
            if (!inter.find(element => element === c)) {
                inter.push(c);
            }
        }
        setColors(inter);
    }, [nb_cars]);

    const getSeries = useCallback((s: Array<Types.individual>) => {
        const bestFitness = getMinFitness(s);
        const bestSnapshot = s.find(e => e.fitness === bestFitness);
        if (bestSnapshot) {
            const solution = bestSnapshot.solution;
            const zeros = [];
            for (const i in solution) {
                if (solution[i] === 0) {
                    zeros.push(parseInt(i));
                }
            }
            zeros.shift();

            // eslint-disable-next-line prefer-const
            let series = [];
            let current = 0;
            let n = 0;
            for (const z of zeros) {
                const next = z;
                const inter = solution.slice(current, next);
                const res = [];
                for (const s of inter) {
                    const el = nodes[s];
                    if (el) {
                        res.push({
                            "node": s, "x": el[0], "y": el[1]
                        });
                    }
                }
                res.push({
                    "node": 0, "x": nodes["0"][0], "y": nodes["0"][1]
                });
                series.push({"id": n.toString(), "data": res});
                n++;
                current = next;
            }
            return series;
        }
        return [];
    }, [nodes]);

    const update_plot = useCallback(async() => {
        const response = await http.get("snapshot");
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        const snapshot:Types.individual[] = response.data.snapshot;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
        setNb_epochs(response.data.generation);

        setplotdata(g => g.concat([
            {
                "generation": nb_epochs,
                "fitness"   : snapshot[0].fitness
            }
        ]));

        const res = getSeries(snapshot);
        setgraphdata(res);

        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        if (!response.data.has_next) {
            setToggle(false);
            setEnableButton(true);
        }
    }, [
        nb_epochs,
        getSeries
    ]);

    useEffect(() => {
        if (toggle) {
            void update_plot();
        }
    }, [
        plotdata,
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
                        fontWeight: "bold", mt: 10, mb: 2
                    }}
                >
                    Evolution de la fitness au cours des générations
                </Typography>
                <Stack direction="row" justifyContent="center">
                    <Typography variant="h6" fontStyle="italic">
                            Génération
                    </Typography>
                    <Badge badgeContent={nb_epochs} max={100000} color="secondary" sx={{ml: 2}}>
                    </Badge>
                </Stack>

                <Grid container alignItems="center">
                    <Grid item xs={6} sx={{mt: 5}}>
                        <LineChart width={500} height={300}
                            data={plotdata.slice(1, plotdata.length)}
                        >
                            <Line type="monotone" dataKey="fitness" stroke="#82ca9d" isAnimationActive={false} strokeWidth={2} />
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="generation" type="number"
                                domain={[
                                    1,
                                    gen + 10
                                ]}/>
                            <YAxis dataKey="fitness" type="number"/>
                            <Tooltip/>
                            <Legend/>
                        </LineChart>
                    </Grid>
                    <Grid item xs={6} sx={{mt: 2}}>
                        <LineChart width={500}height={300}>
                            <CartesianGrid strokeDasharray="5 5" />
                            <XAxis dataKey="x" type="number" unit="km" domain={[
                                getMinX(graphdata),
                                getMaxX(graphdata) + 10
                            ]}/>
                            <YAxis dataKey="y" type="number" unit="km" domain={[
                                getMinY(graphdata),
                                getMaxY(graphdata) + 10
                            ]}/>
                            <Tooltip/>
                            {graphdata.map((s, index) => <Line isAnimationActive={false} dataKey="y" data={s.data} name={"voiture " + s.id} type="linear"
                                stroke={colors[index]} key={s.id}>
                                <LabelList dataKey="node" position="top" />
                            </Line>
                            )}
                        </LineChart>
                    </Grid>
                    <Grid item xs={6}></Grid>
                    <Grid item xs={6} >
                        <Stack direction="row" spacing={1} sx={{ml: 7}}>
                            {colors.map((c, index) => <Avatar sx={{
                                bgcolor: c, width: 24, height: 24
                            }}>{index + 1}</Avatar>)}
                        </Stack>
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