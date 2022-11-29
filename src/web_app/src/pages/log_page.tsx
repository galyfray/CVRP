/* eslint-disable @typescript-eslint/no-floating-promises */
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import GlobalStyles from "@mui/material/GlobalStyles";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import React, {useEffect} from "react";
import {AppbarStyle} from "../components/appBar";
import http from "../http-common";
import {Types} from "../types/data";
import Paper from "@mui/material/Paper";
import Row from "../components/log_row";

export function LogsPage() {
    const [
        logs,
        setLogs
    ] = React.useState<Array<Types.Log>>([
        {
            "id"    : "",
            "method": "",
            "logs"  : []
        }
    ]);

    useEffect(() => {
        (
            async() => {
                await http.get("get_logs")
                    .then(response => {
                        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
                        console.log(response.data.data);
                        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
                        setLogs(response.data.data);
                    });
            }
        )();
    }, []);
    return (
        <React.Fragment>
            <GlobalStyles styles={{
                ul: {
                    margin: 0, padding: 0, listStyle: "none"
                }
            }} />
            <CssBaseline />
            <AppbarStyle/>
            <Container component="main" maxWidth="md" sx={{pt: 5}}>
                <Typography
                    variant="h4"
                    align="center"
                    color="text.primary"
                    gutterBottom
                    sx={{fontWeight: "bold", mb: 2}}
                >
            Résultat
                </Typography>
                <Typography
                    variant="h6"
                    data-testid = "logpage_title"
                    align="left"
                    color="text.primary"
                    gutterBottom
                    sx={{mt: 2, mb: 5}}
                >
            Cette page présente les résultats envoyés par le solveur au cours des différentes résolutions
                </Typography>
                <TableContainer component={Paper}>
                    <Table aria-label="collapsible table">
                        <TableHead>
                            <TableRow>
                                <TableCell />
                                <TableCell>Bench_ID</TableCell>
                                <TableCell align="right">Method</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {logs.map((log, index) => <Row key={index} row={log} />
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        </React.Fragment>
    );
}