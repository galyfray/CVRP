import {render, screen} from "@testing-library/react";
import {LogsPage} from "../pages/log_page";

describe("<LogsPage />", () => {
    test("the rendering of the components", () => {
        render(<LogsPage />);
        expect(screen.getByText("Cette page présente les résultats envoyés par le solveur au cours des différentes résolutions")).toBeTruthy();
    });
});