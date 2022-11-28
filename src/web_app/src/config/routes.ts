/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import {AboutPage} from "../pages/about";
import {AlgoChoosingPage} from "../pages/algo_choosing";
import {GaHyperParamsPage} from "../pages/ga_hyperParams";
import {DrlHyperParamsPage} from "../pages/drl_hyperParams";
import {HomePage} from "../pages/home";
import {OperationPage} from "../pages/operation";
import {ResultPage} from "../pages/result";
import {RunPage} from "../pages/run";
import {LogsPage} from "../pages/log_page";

type Route = {
    name: string,
    path: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    element?: any,
    routes?: Route[],
 };

const compile = (parentRoute: Route, subRoutes: Route[]): Route[] => {
    return subRoutes.flatMap(subRoute => {
        const newRoute: Route = {
            "name"   : subRoute.name,
            "path"   : parentRoute.path + subRoute.path,
            "element": subRoute.element
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
        "name"   : "home",
        "path"   : "/",
        "element": HomePage
    },
    {
        "name"   : "about",
        "path"   : "/about",
        "element": AboutPage
    },
    {
        "name"   : "logs",
        "path"   : "/logs",
        "element": LogsPage
    },
    {
        "name"   : "run",
        "path"   : "/run",
        "element": RunPage
    },
    {
        "name"   : "algo_choice",
        "path"   : "/run/:type/algo_choice",
        "element": AlgoChoosingPage
    },
    {
        "name"   : "ga_hyperparams",
        "path"   : "/run/:type/algo_choice/ga/",
        "element": GaHyperParamsPage
    },
    {
        "name"   : "drl_hyperparams",
        "path"   : "/run/:type/algo_choice/drl/",
        "element": DrlHyperParamsPage
    },
    {
        "name"   : "ga_hyperparams",
        "path"   : "/run/:type/algo_choice/ga/operation/",
        "element": OperationPage
    },
    {
        "name"   : "drl_hyperparams",
        "path"   : "/run/:type/algo_choice/drl/operation/",
        "element": OperationPage
    },
    {
        "name"   : "ga_hyperparams",
        "path"   : "/run/:type/algo_choice/ga/operation/result",
        "element": ResultPage
    },
    {
        "name"   : "drl_hyperparams",
        "path"   : "/run/:type/algo_choice/drl/operation/result",
        "element": ResultPage
    }

];