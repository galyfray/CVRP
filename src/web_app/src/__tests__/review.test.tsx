import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {ReviewPage} from "../pages/review";

// TODO test to check the type of the get request

describe("<ReviewPage />", () => {
    test("checking components", () => {
        render(<ReviewPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("review_title")).toBeVisible();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/logs/review",
        search  : "",
        hash    : "",
        state   : {log_id: "E-n112-k8-s11.evrp_ga_0_2_4_0.1_1", bench_id: "E-n112-k8-s11.evrp"}
    })
}));
