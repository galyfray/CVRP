import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {OperationPage} from "../pages/operation";

// TODO test to check the type of the get request

describe("<OperationPage />", () => {
    test("checking components", () => {
        render(<OperationPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("operation_title")).toBeVisible();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run/:bench_type/algo_choice/:algo_type/operation/result",
        search  : "",
        hash    : "",
        state   : null
    })
}));
