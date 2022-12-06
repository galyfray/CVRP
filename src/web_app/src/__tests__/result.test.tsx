import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {ResultPage} from "../pages/result";

describe("<ResultPage />", () => {
    test("checking components", () => {
        render(<ResultPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("result_title")).toBeVisible();
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
