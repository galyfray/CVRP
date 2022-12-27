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
import {getMinFitness, getRandomColor} from "../config/utils";

export function ReviewPage() {
    const url = useLocation().pathname;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const log_id:string = useLocation().state.log_id;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const bench_id:string = useLocation().state.bench_id;
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
        data,
        setData
    ] = React.useState<Array<{"generation" : number, "fitness" : number, "solution": []}>>([
        {
            "generation": 0,
            "fitness"   : 0,
            "solution"  : []
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
        async function getData() {
            await http.get(`log/${log_id}`)
                .then(response => {
                    // eslint-disable-next-line
                    const snapshots:Array<{"time" : number, "individuals": [Types.individual]}> = response.data.snapshots;
                    const inter:Array<{"generation" : number, "fitness" : number, "solution": []}> = [];

                    for (let i = 0;i < snapshots.length;i++) {
                        const s = snapshots[i];
                        const bestFitness = getMinFitness(s.individuals);
                        const bestSnapshot = s.individuals.find(e => e.fitness === bestFitness);
                        if (bestSnapshot) {
                            const solution = bestSnapshot.solution;
                            inter.push({
                                "generation": i, "fitness": bestFitness, "solution": solution
                            });
                        }
                    }
                    console.log(inter);
                    setData(inter);
                });
        }
        void getData();
    }, [log_id]);

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

    const getSeriesB = useCallback((snapshot: Types.individual) => {
        const zeros = [];
        const sol = snapshot.solution;
        for (const i in sol) {
            if (sol[i] === 0) {
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
            const inter = sol.slice(current, next);
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

    }, [nodes]);

    useEffect(() => {
        if (data.length > 1) {
            const step = data.length / 2; // 25 comme step plus tard avec de vrais données;
            const reducer = data;
            setPlotdata1(reducer.slice(0, step));

            const snapshot = reducer.at(step - 1);
            if (snapshot) {
                const res = getSeriesB(snapshot);
                setgraphdata(res);
                const inter:Array<string> = [];
                for (let i = 0;i < Object.keys(res).length;i++) {
                    const c = getRandomColor();
                    if (!inter.find(element => element === c)) {
                        inter.push(c);
                    }
                }
                setColors(inter);
            }

            console.log("plot 1", reducer.slice(0, step));
            reduce_data(step, reducer);
        }
    },
    [
        data,
        getSeriesB,
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

                <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={5} sx={{mt: 4}}>
                        <LineChart
                            width={450}
                            height={350}
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
                    <Grid item xs={7} sx={{mt: 2}}>
                        <LineChart
                            width={450}
                            height={350}
                        >
                            <CartesianGrid strokeDasharray="5 5" />
                            <XAxis dataKey="x" type="number" unit="km"/>
                            <YAxis dataKey="y" type="number" unit="km"/>
                            <Tooltip />
                            <Legend />
                            {graphdata.map((s, index) => <Line isAnimationActive={false} dataKey="y" data={s.data} name={"voiture " + s.id} type="linear"
                                stroke={colors[index]} key={s.id}>
                                <LabelList dataKey="node" position="top" />
                            </Line>
                            )}
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