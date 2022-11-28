import React from "react";
import GlobalStyles from "@mui/material/GlobalStyles";
import CssBaseline from "@mui/material/CssBaseline";
import {AppbarStyle} from "../components/appBar";
import Container from "@mui/material/Container";
import {Typography} from "@mui/material";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Grid";
import about_image from "../images/about_image.png";
import benchmark from "../images/benchmark.PNG";
import TreeView from "@mui/lab/TreeView";
import {
    CloseSquare, MinusSquare, PlusSquare, StyledTreeItem
} from "../components/tree_styles";

export function AboutPage() {
    return (
        <React.Fragment>
            <GlobalStyles styles={
                {
                    ul: {
                        margin: 0, padding: 0, listStyle: "none"
                    }
                }} />
            <CssBaseline />
            <AppbarStyle/>
            <Grid container justifyContent="space-between" sx={{mt: 5}}>
                <Grid item xs={12} sx={{ml: 10, mr: 10}}>
                    <Typography
                        variant="h5"
                        align="justify"
                        color="#344E6B"
                        sx={{fontWeight: "bold"}}
                    >
                        Acheminement des véhicules électriques avec fenêtres de
                        temps et contraintes de capacité (CVRPTW)
                    </Typography>
                </Grid>
                <Grid item xs={12} sx={{ml: 10, mt: 3}}>
                    <TreeView
                        aria-label="customized"
                        defaultExpanded={["1"]}
                        defaultCollapseIcon={<MinusSquare />}
                        defaultExpandIcon={<PlusSquare />}
                        defaultEndIcon={<CloseSquare />}
                    >
                        <StyledTreeItem nodeId="1" label="Sommaire">
                            <StyledTreeItem nodeId="2" label="Problème" />
                            <StyledTreeItem nodeId="4" label="Benchmark" />
                            <StyledTreeItem nodeId="5" label="Programme" />
                            <StyledTreeItem nodeId="5" label="Notice d'utilisation" />
                        </StyledTreeItem>
                    </TreeView>
                </Grid>
            </Grid>
            <Container component="main" maxWidth="md">
                <Typography
                    variant="h5"
                    color="#344E6B"
                    sx={{mt: 5}}
                >
                  Problème
                </Typography>
                <Divider />
                <Grid container justifyContent="space-between">
                    <Grid item xs={12} alignItems="center" sx={{
                        mt: 3, ml: 40, mb: 3
                    }}>
                        <img src={about_image} alt="about_image" width= "40%" />
                    </Grid>
                    L'E-CVRPTW est un problème particulier de la famille des problèmes VRP.
                        Les problèmes VRP sont des problèmes axés autour de plusieurs véhicules
                        qui doivent livrer plusieurs points
                        à partir d’un ou plusieurs dépôts.<br/>
                        Dans l'E-CVRPTW, des contraintes supplémentaires sont ajoutées :
                    <ul>
                        <li>les véhicules sont électriques</li>
                        <li>les véhicules ont une capacité de transport finie</li>
                        <li>une contrainte de fenêtre de temps: les véhicules devront
                            livrer leur colis aux heures d’ouverture du point.</li>
                    </ul>
                        Ce problème ne couvre que le cas d'un dépot unique. Cependant, on considère que
                        que de multiples stations de rechargement sont disponibles.
                </Grid>
                <Typography variant="body1" align="justify" component="p">
                    <br/>
                    En resumé, une flotte de véhicules de livraison de capacités variées doit
                    desservir des clients dont la demande et les heures d'ouverture sont connues.
                    Les véhicules commencent et terminent leur
                    itinéraire dans un dépôt commun. Chaque client ne peut être servi que
                    par un seul véhicule.<br/>
                    L'objectif est d'assigner une séquence de clients à chaque camion de la flotte
                    en minimisant le temp de sorte que tous les clients
                    soient servis et que la demande totale servie par chaque camion ne dépasse pas sa capacité.
                </Typography>
                <Typography
                    variant="h5"
                    color="#344E6B"
                    sx={{mt: 3}}
                >
                    Benchmark
                </Typography>
                <Divider />
                <Typography variant="body1" align="justify" component="p" sx={{mt: 1}}>
                    Chaque jeu de données a été nommé avec un formalisme pratique.
                    Derrière chaque lettre de l’intitulé du fichier se trouve un nombre quantifiant
                    un paramètre de ce jeu de données :
                    <br/>Par exemple, le jeu de données E-n112-k8-s11.evrp concerne un cas d’EVRP
                    avec 8 véhicules électriques disposant de 11 stations de rechargement dans
                    un environnement de 112 points.
                    Les autres spécifications sont indiquées dans le fichier.
                </Typography>
                <Typography variant="h6" align="justify" sx={{mt: 2, ml: 7}} >
                    Tableau détaillant le contenu de notre benchmark
                </Typography>
                <img src={benchmark} alt="benchmark" width= "85%"/>
                <Typography
                    variant="h5"
                    color="#344E6B"
                    sx={{mt: 3}}
                >
                    Programme
                </Typography>
                <Divider />
                <Typography variant="body1" align="justify" component="p" sx={{mt: 1}}>
                    to do
                </Typography>
                <Typography
                    variant="h5"
                    color="#344E6B"
                    sx={{mt: 3}}
                >
                    Notice d'utilisation
                </Typography>
                <Divider />
                <Typography variant="body1" align="justify" component="p" sx={{mt: 1}}>
                    to do
                </Typography>

            </Container>
        </React.Fragment>
    );
}