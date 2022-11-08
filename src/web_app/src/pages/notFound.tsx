import React from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import Container from "@mui/material/Container";
import Link from "@mui/material/Link";
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';
import { Typography } from "@mui/material";

export function NotFoundPage() {
    return (
      <React.Fragment>
        <GlobalStyles styles={{ ul: { margin: 0, padding: 0, listStyle: 'none' } }} />
        <CssBaseline />
        <Container disableGutters component="main" maxWidth="md" sx={{ pt: 8, ml:20 }}>
        <div>
            <Typography variant="h4">
            Oups ! Vous semblez être perdu.
                <SentimentVeryDissatisfiedIcon/>
            </Typography>

            <p>Voici quelques liens utiles :</p>
            <Link href='/'>Home</Link> <br/>
            <Link href="/about">About</Link>
        </div>
         </Container>
         </React.Fragment>
    );
}