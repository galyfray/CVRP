import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {DrlHyperParamsPage} from "../pages/drl_hyperParams";
import axios from "axios";

const mockedUsedNavigate = jest.fn();
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;
mockedAxios.get.mockRejectedValue("Network error: Something went wrong");

describe("<DrlHyperParamsPage />", () => {
    test("checking components", () => {
        render(<DrlHyperParamsPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("drl_hp_title")).toBeVisible();
    });

    /*
    It("should send the hyperparameters to the flask api", async() => {
        const newHP = {
            "type"  : "drl",
            "params": {
                "nb_epochs"    : 1000,
                "pop_size"     : 512,
                "seed"         : 0.5,
                "mutation_rate": 0.2,
                "learning_rate": 0.5,
                "batch_size"   : 32,
                "momentum"     : 0.2
            },
            override     : false,
            bench_id     : "nothing",
            snapshot_rate: 3
        };
        await mockedAxios.post("http://127.0.0.1:5000/operation_params/drl", newHP)
            .then(response => {
                expect(response.status).toBe(200);
            });
    });
    */

});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run/:bench_type/algo_choice/drl",
        search  : "",
        hash    : "",
        state   : null
    }),
    useNavigate: () => mockedUsedNavigate
}));