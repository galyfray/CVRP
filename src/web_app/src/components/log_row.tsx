/* eslint-disable @typescript-eslint/restrict-plus-operands */
import IconButton from "@mui/material/IconButton";
import TableCell from "@mui/material/TableCell";
import TableRow from "@mui/material/TableRow";
import React from "react";
import * as Types from "../types/data";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Collapse from "@mui/material/Collapse";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import TableBody from "@mui/material/TableBody";
import PlayCircleFilledIcon from "@mui/icons-material/PlayCircleFilled";
import Button from "@mui/material/Button";
import {ReviewPage} from "../pages/review";
import {useLocation} from "react-router-dom";


export default function Row(props: { row: Types.Log }) {
    const {row} = props;
    const url = useLocation().pathname;
    const [
        open,
        setOpen
    ] = React.useState(false);

    const handleClick = () => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        <ReviewPage log_id={row.log_id} />;
    };

    return (
        <React.Fragment>
            <TableRow sx={{"& > *": {borderBottom: "unset"}}}>
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
                    >
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    {row.bench_id}
                </TableCell>
                <TableCell align="right">
                    {row.method}
                </TableCell>
                <TableCell align="right">
                    {row.snapshots.time}
                </TableCell>
                <TableCell align="right">
                    <Button onClick={handleClick} href={url + "/review"}
                    >
                        <PlayCircleFilledIcon />
                    </Button>
                </TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{margin: 1}}>
                            <Typography variant="h6" gutterBottom component="div">
                                Snapshots
                            </Typography>
                            <Table size="small" aria-label="purchases">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Fitness</TableCell>
                                        <TableCell>Solution</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {row.snapshots.individuals.map(perf => <TableRow key={perf.fitness}>
                                        <TableCell component="th" scope="row">
                                            {perf.fitness}
                                        </TableCell>
                                        <TableCell>{perf.solution.slice(0, -1).map(el => el + "-")}0</TableCell>
                                    </TableRow>
                                    )}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}