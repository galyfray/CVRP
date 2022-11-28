/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import {render, screen} from "@testing-library/react";
import {AboutPage} from "../pages/about";
import * as ShallowRenderer from "react-test-renderer/shallow";

//Import {shallow, mount} from "enzyme";

import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";

describe("<AboutPage />", () => {
    test("render the required components in the about page", () => {
        render(<AboutPage />);

        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();

        expect(screen.getByText("Acheminement des véhicules électriques avec fenêtres de temps et contraintes de capacité (CVRPTW)")).toBeTruthy();
        expect(screen.getByRole("img", {name: "about_image"})).toBeInTheDocument();
        expect(screen.getByRole("img", {name: "benchmark"})).toBeInTheDocument();
        expect(view).toBeTruthy();

    });
});
