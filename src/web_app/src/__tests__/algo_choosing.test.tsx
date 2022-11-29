/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {AlgoChoosingPage} from "../pages/algo_choosing";

// TODO test to check the type of the post request
// TODO test to check the rendering of the MobileStepper component

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
        pathname: "/algo_choice",
        search  : "",
        hash    : "",
        state   : null
    })
}));

