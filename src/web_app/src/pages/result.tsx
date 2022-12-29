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
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LabelList
} from "recharts";
import * as Types from "../types/data";
import {getRandomColor} from "../config/utils";

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

export function ResultPage() {
    const url = useLocation().pathname;
    const dataset_choice = url.split("/")[2];
    const [
        colors,
        setColors
    ] = React.useState<Array<string>>([]);
    const [
        bench_id,
        setBench_id
    ] = React.useState("");
    const [
        sol,
        setSol
    ] = React.useState<Array<string>>([]);
    const [
        logs,
        setLogs
    ] = React.useState<Types.Log>(
        {
            "bench_id" : "",
            "log_id"   : "",
            "method"   : "",
            "snapshots": [
                {
                    "time"       : 0,
                    "individuals": [
                        {
                            "fitness" : 0,
                            "solution": []
                        }
                    ]
                }
            ]
        }
    );
    const [
        length,
        setLength
    ] = React.useState(1);
    const [
        graph_data,
        set_graph_data
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

    useEffect(() => {
        async function getNodes() {
            await http.get(`benchmark?bench_id=${bench_id}`)
                .then(response => {
                // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-assignment
                    setNodes(response.data);
                });
        }
        void getNodes();
    }, [bench_id]);

    useEffect(() => {
        setBench_id(datasets[parseInt(dataset_choice)]);
        async function getResults() {
            await http.get(`results?id=${bench_id}`)
                .then(response => {
                // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
                    setLogs(response.data);
                    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
                    setLength(response.data.snapshots[0].individuals.length);
                });
        }
        void getResults();
    }, [
        bench_id,
        dataset_choice,
        length
    ]);

    useEffect(() => {
        if (Object.keys(nodes).length > 1) {
            const solution = logs.snapshots[0].individuals[length - 1].solution;
            // eslint-disable-next-line @typescript-eslint/restrict-plus-operands
            setSol(solution.slice(0, -1).map(el => el + "-"));
            const zeros = [];
            for (const i in solution) {
                if (solution[i] === 0) {
                    zeros.push(parseInt(i));
                }
            }
            zeros.shift();

            const series = [];
            let current = 0;
            let n = 0;
            for (const z of zeros) {
                const next = z;
                const inter = solution.slice(current, next);
                const res = [];
                for (const s of inter) {
                    //Let el = nodes.find(element => Object.keys(element)[0] === s);
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
            set_graph_data(series);

            const inter:Array<string> = [];
            for (let i = 0;i < Object.keys(series).length;i++) {
                const c = getRandomColor();
                if (!inter.find(element => element === c)) {
                    inter.push(c);
                }
            }
            setColors(inter);
        }
    }, [
        nodes,
        logs.snapshots,
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
            <Container disableGutters component="main" sx={{pt: 3, mt: 8}}>
                <Typography
                    variant="h4"
                    data-testid = "result_title"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold"}}
                >
                    Résultat
                </Typography>

                <Grid container spacing={2} sx={{mt: 3}}>
                    <Grid item xs={7} sx={{ml: 7}}>
                        <LineChart
                            width={600}
                            height={350}
                        >
                            <CartesianGrid strokeDasharray="5 5" />
                            <XAxis dataKey="x" type="number" unit="km"/>
                            <YAxis dataKey="y" type="number" unit="km"/>
                            <Tooltip />
                            <Legend />
                            {graph_data.map((s, index) => <Line isAnimationActive={false} dataKey="y" data={s.data} name={"voiture " + s.id} type="linear"
                                stroke={colors[index]} key={s.id}>
                                <LabelList dataKey="node" position="top" />
                            </Line>
                            )}
                        </LineChart>
                    </Grid>
                    <Grid item xs={4} >
                        <Box
                            sx={{
                                width          : 320,
                                height         : 210,
                                backgroundColor: "black",
                                mt             : 5,
                                ml             : 2
                            }}
                        >
                            <Grid container alignItems="center" spacing={2}>
                                <Grid item xs={12}>
                                    <Typography color="#FFFFFF" sx={{ml: 3}}>
                                        ID : {logs.bench_id}
                                    </Typography>
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography color="#808080" sx={{ml: 3}}>
                                        Algorithme : {logs.method}
                                    </Typography>
                                </Grid>
                                <Grid item xs={6} color="#808080" >
                                    <Typography>
                                        Fitness : {logs.snapshots[0].individuals[length - 1].fitness}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} color="#808080" sx={{ml: 3}}>
                                    <Typography sx={{mr: 2}}>
                                        Temps d'exécution : {logs.snapshots[0].time}
                                    </Typography>
                                </Grid>
                                <Grid item alignItems="center" xs={12}>
                                    <Button variant="contained" sx={{
                                        height: 20, width: 260, ml: 3
                                    }} href="/logs" >
                                        Plus de détails
                                    </Button>
                                </Grid>
                                <Grid item alignItems="center" xs={12}>
                                    <Button variant="contained"
                                        sx={{
                                            height: 20, width: 260, backgroundColor: "#434343", ml: 3
                                        }} href="/run" >
                                        <Typography color="#5455AF">
                                            Relancer
                                        </Typography>
                                    </Button>
                                </Grid>
                            </Grid>
                        </Box>
                    </Grid>
                    <Grid item xs={12}>
                        <Typography sx={{fontWeight: "bold", ml: 8}}>
                            Solution Finale:<br/>
                        </Typography>
                        <Typography sx={{ml: 13}}>
                            {sol}0
                        </Typography>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    );
}