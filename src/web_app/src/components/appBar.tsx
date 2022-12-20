import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import {Button} from "@mui/material";

export function AppbarStyle() {
    return (
        <AppBar
            position="fixed"
            color="default"
            elevation={0}
            sx={{borderBottom: theme => `1px solid ${theme.palette.divider}`}}
        >
            <Toolbar sx={{flexWrap: "wrap"}}>
                <Typography variant="h4" color="inherit" noWrap sx={{
                    fontWeight: "bold", flexGrow: 1, ml: 5
                }}>
            Semina
                </Typography>
                <nav>
                    <Link
                        variant="button"
                        sx={{my: 1, mx: 3}}
                        color="text.primary"
                        href="/"
                        underline="hover">
                  Home
                    </Link>
                </nav>
                <nav>
                    <Link
                        variant="button"
                        color="text.primary"
                        href="/run"
                        underline="hover"
                        sx={{my: 1, mx: 3}}
                    >
              Run
                    </Link>
                </nav>
                <nav>
                    <Link
                        variant="button"
                        sx={{my: 1, mx: 3}}
                        color="text.primary"
                        href="/about"
                        underline="hover"
                    >
              About
                    </Link>
                </nav>
                <nav>
                    <Link
                        variant="button"
                        sx={{
                            my: 1, mx: 3, mr: 35
                        }}
                        color="text.primary"
                        href="#"
                        underline="hover"
                    >
              Logs
                    </Link>
                </nav>
                <nav>
                    <Button variant="contained" style={{
                        borderRadius   : 35,
                        backgroundColor: "#000000"
                    }}
                    sx={{mr: 5}}
                    href="mailto:blablabla@gmail.com">
                Contact
                    </Button>
                </nav>
            </Toolbar>
        </AppBar>

    );
}