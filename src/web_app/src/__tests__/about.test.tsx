import {render, screen} from "@testing-library/react";
import {AboutPage} from "../pages/about";
import * as ShallowRenderer from "react-test-renderer/shallow";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";

describe("<AboutPage />", () => {
    test("render the required components in the about page", () => {
        render(<AboutPage />);

        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();

        expect(screen.getByTestId("about_title")).toBeVisible();
        expect(screen.getByRole("img", {name: "about_image"})).toBeInTheDocument();
        expect(screen.getByRole("img", {name: "benchmark"})).toBeInTheDocument();

    });
});
