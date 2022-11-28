/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import * as ShallowRenderer from "react-test-renderer/shallow";
import {render, screen} from "@testing-library/react";
import "@testing-library/jest-dom";
import {AppbarStyle} from "../components/appBar";
import {GaHyperParamsPage} from "../pages/ga_hyperParams";

const mockedUsedNavigate = jest.fn();

describe("<GaHyperParamsPage />", () => {
    test("checking components", () => {
        render(<GaHyperParamsPage />);
        const utils = ShallowRenderer.createRenderer();
        utils.render(<AppbarStyle />);
        const view = utils.getRenderOutput();
        expect(view).toBeTruthy();
        expect(screen.getByText("Entrez les hyperparamètres")).toBeTruthy();
    });
});

jest.mock("react-router-dom", () => ({
    __esModule : true,
    useLocation: jest.fn().mockReturnValue({
        pathname: "/run/:type/algo_choice/ga",
        search  : "",
        hash    : "",
        state   : null,
        key     : "5nvxpbdafa"
    }),
    useNavigate: () => mockedUsedNavigate
}));
