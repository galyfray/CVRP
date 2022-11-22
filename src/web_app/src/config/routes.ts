/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import {AboutPage} from "../pages/about";
import {AlgoChoosingPage} from "../pages/algo_choosing";
import {GaHyperParamsPage} from "../pages/ga_hyperParams";
import {DrlHyperParamsPage} from "../pages/drl_hyperParams";
import {HomePage} from "../pages/home";
import {OperationPage} from "../pages/operation";
import {ResultPage} from "../pages/result";
import {RunPage} from "../pages/run";

type Route = {
    name: string,
    path: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    component?: any,
    routes?: Route[],
 };

const compile = (parentRoute: Route, subRoutes: Route[]): Route[] => {
    return subRoutes.flatMap(subRoute => {
        const newRoute: Route = {
            "name"     : subRoute.name,
            "path"     : parentRoute.path + subRoute.path,
            "component": subRoute.component
        };
        return subRoute.routes ? [...compile(newRoute, subRoute.routes)] : newRoute;
    });
};

export const getRoutes = () => {
    const parentRoute = {
        "name": "",
        "path": ""
    };
    const flatRoutes = compile(parentRoute, routes);
    return flatRoutes;
};

const routes = [
    {
        "name"     : "home",
        "path"     : "/",
        "component": HomePage
    },
    {
        "name"     : "about",
        "path"     : "/about",
        "component": AboutPage
    },
    {
        "name"     : "run",
        "path"     : "/run",
        "component": RunPage
    },
    {
        "name"     : "algo_choice",
        "path"     : "/run/:type/algo_choice",
        "component": AlgoChoosingPage
    },
    {
        "name"     : "ga_hyperparams",
        "path"     : "/run/:type/algo_choice/ga/",
        "component": GaHyperParamsPage
    },
    {
        "name"     : "drl_hyperparams",
        "path"     : "/run/:type/algo_choice/drl/",
        "component": DrlHyperParamsPage
    },
    {
        "name"     : "al_hyperparams",
        "path"     : "/run/:type/algo_choice/ga/operation/",
        "component": OperationPage
    },
    {
        "name"     : "drl_hyperparams",
        "path"     : "/run/:type/algo_choice/drl/operation/",
        "component": OperationPage
    },
    {
        "name"     : "al_hyperparams",
        "path"     : "/run/:type/algo_choice/ga/operation/result",
        "component": ResultPage
    },
    {
        "name"     : "drl_hyperparams",
        "path"     : "/run/:type/algo_choice/drl/operation/result",
        "component": ResultPage
    }

];