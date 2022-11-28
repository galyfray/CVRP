/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
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

        expect(screen.getByText("ECVRPTW Solver")).toBeTruthy();
        expect(screen.getByRole("img", {name: "cvrp_image"})).toBeInTheDocument();
        expect(view).toBeTruthy();

        const links: HTMLAnchorElement[] = screen.getAllByRole("link");
        expect(links[5].textContent).toEqual("Lire la suite");
        expect(links[5].href).toContain("/about");
        expect(links[6].textContent).toEqual("Démarrer");
        expect(links[6].href).toContain("/run");
    });
});