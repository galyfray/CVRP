import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {AlgoChoosingPage} from "../pages/algo_choosing";

describe("<AlgoChoosingPage />", () => {
    test("if the components are rendered normally", () => {
        render(<AlgoChoosingPage />);

        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("algo_choice_title")).toBeVisible();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run/:bench_type/algo_choice",
        search  : "",
        hash    : "",
        state   : null
    })
}));

