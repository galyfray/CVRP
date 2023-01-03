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
import {useLocation, useNavigate} from "react-router-dom";
import * as Types from "../types/data";
import Badge from "@mui/material/Badge";
import Stack from "@mui/material/Stack";
import {
    getMaxX,
    getMaxY,
    getMinFitness, getMinX, getMinY, getRandomColor
} from "../config/utils";
import Avatar from "@mui/material/Avatar";

export function OperationPage() {
    const url = useLocation().pathname;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const datasets: [] = useLocation().state.benchmarks;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
    const gen:number = useLocation().state.nb_epochs;
    const dataset_choice = url.split("/")[2];
    const [
        nb_cars,
        setNb_cars
    ] = React.useState("1");
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

    const navigate = useNavigate();
    const handleClick = () => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        navigate(url + "/result", {state: {benchmarks: datasets}});
    };

    useEffect(() => {
        const obj: Types.BenchType = datasets[parseInt(dataset_choice)];
        // eslint-disable-next-line
        const benchmark: string = obj.name;
        // eslint-disable-next-line
        const veh:string = obj.name.split("-")[2];
        setNb_cars(veh.slice(1, veh.length));

        const inter:Array<string> = [];
        for (let i = 0;i < parseInt(nb_cars);i++) {
            const c = getRandomColor();
            if (!inter.find(element => element === c)) {
                inter.push(c);
            }
        }
        setColors(inter);
        
        async function getNodes() {
            // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
            await http.get(`benchmark/${benchmark}`)
                .then(response => {
                    // eslint-disable-next-line
                    setNodes(response.data["NODES"]);
                });
        }
        void getNodes();
    }, [dataset_choice, datasets, nb_cars]);

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
                            {colors.map((c, index) => <Avatar key={index} sx={{
                                bgcolor: c, width: 24, height: 24
                            }}>{index + 1}</Avatar>)}
                        </Stack>
                    </Grid>
                    <Grid item xs={8}></Grid>
                    <Grid item xs={4} sx= {{mt: 3}}>
                        {enableButton && <Button variant="contained" color="success" sx={{
                            height: 25, width: 200, mr: 0
                        }} onClick={handleClick}>
                            Continuer
                        </Button>}
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    );
}