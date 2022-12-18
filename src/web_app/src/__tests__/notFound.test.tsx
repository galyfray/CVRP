import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {NotFoundPage} from "../pages/notFound";

describe("<NotFoundPage />", () => {
    test("components are rendered", () => {
        render(<NotFoundPage />);
        expect(screen.getByTestId("notFound_title")).toBeVisible();
        const link1 = screen.getByRole("link", {name: "Home"});
        expect(link1).toHaveAttribute("href", "/");
        const link2 = screen.getByRole("link", {name: "About"});
        expect(link2).toHaveAttribute("href", "/about");
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/*",
        search  : "",
        hash    : "",
        state   : null
    })
}));