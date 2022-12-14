import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {RunPage} from "../pages/run";

// TODO test to check the type of the get response
// TODO test to check the rendering of the MobileStepper component

describe("RunPage components", () => {
    test("if the components are rendered normally", () => {
        render(<RunPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("run_title")).toBeVisible();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run",
        search  : "",
        hash    : "",
        state   : null
    })
}));
