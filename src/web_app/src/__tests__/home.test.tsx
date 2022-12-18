import {HomePage} from "../pages/home";
import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";

describe("<HomePage />", () => {
    test("render the required components in the home page", () => {
        render(<HomePage />);

        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeDefined();

        expect(screen.getByText("ECVRPTW Solver")).toBeVisible();
        expect(screen.getByRole("img", {name: "cvrp_image"})).toBeInTheDocument();

        const links: HTMLAnchorElement[] = screen.getAllByRole("link");
        expect(links[5].textContent).toEqual("Lire la suite");
        expect(links[5].href).toContain("/about");
        expect(links[6].textContent).toEqual("Démarrer");
        expect(links[6].href).toContain("/run");
    });
});