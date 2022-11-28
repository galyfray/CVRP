import {render} from "@testing-library/react";
import {NotFoundPage} from "../pages/notFound";

describe("<NotFoundPage />", () => {
    test("components are rendered", () => {
        render(<NotFoundPage />);
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/*",
        search  : "",
        hash    : "",
        state   : null,
        key     : "5nvxpbdafa"
    })
}));