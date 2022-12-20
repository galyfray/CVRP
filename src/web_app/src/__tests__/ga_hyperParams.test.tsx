import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {GaHyperParamsPage} from "../pages/ga_hyperParams";
import axios from "axios";

const mockedUsedNavigate = jest.fn();
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;
mockedAxios.get.mockRejectedValue("Network error: Something went wrong");

describe("<GaHyperParamsPage />", () => {
    test("checking components", () => {
        render(<GaHyperParamsPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("ga_hp_title")).toBeVisible();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run/:bench_type/algo_choice/ga",
        search  : "",
        hash    : "",
        state   : null
    }),
    useNavigate: () => mockedUsedNavigate
}));
