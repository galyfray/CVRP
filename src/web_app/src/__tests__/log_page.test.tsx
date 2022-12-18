import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {LogsPage} from "../pages/log_page";

// TODO test to check the type of the get request

describe("<LogsPage />", () => {
    test("the rendering of the components", () => {
        render(<LogsPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();
        expect(screen.getByTestId("logpage_title")).toBeVisible();
    });
});
