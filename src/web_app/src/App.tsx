import {useEffect} from "react";
import "./App.css";
import logging from "./config/logging";
import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";
import {NotFoundPage} from "./pages/notFound";
import {HomePage} from "./pages/home";
import {AboutPage} from "./pages/about";
import {LogsPage} from "./pages/log_page";
import {RunPage} from "./pages/run";
import {AlgoChoosingPage} from "./pages/algo_choosing";
import {GaHyperParamsPage} from "./pages/ga_hyperParams";
import {OperationPage} from "./pages/operation";
import {ResultPage} from "./pages/result";
import {DrlHyperParamsPage} from "./pages/drl_hyperParams";
import {ReviewPage} from "./pages/review";

function App() {

    useEffect(() => {
        logging.info("Loading application");
    }, []);

    return (
        <div>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/about" element={<AboutPage />} />
                    <Route path="/logs" element={<LogsPage />} />
                    <Route path="/run" element={<RunPage />}>
                    </Route>
                    <Route path="/logs/review" element={<ReviewPage/>}>
                    </Route>
                    <Route path="/run/:bench_type/review/result" element={<ResultPage />}>
                    </Route>
                    <Route path="/run/:bench_type/algo_choice" element={<AlgoChoosingPage />} />
                    <Route path="/run/:bench_type/algo_choice/ga" element={<GaHyperParamsPage />}>
                    </Route>
                    <Route path="/run/:bench_type/algo_choice/drl" element={<DrlHyperParamsPage />}>
                    </Route>
                    <Route path="/run/:bench_type/algo_choice/:algo_type/operation" element={<OperationPage />}>
                    </Route>
                    <Route path="/run/:bench_type/algo_choice/:algo_type/operation/result" element={<ResultPage />}/>
                    <Route element={<NotFoundPage />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
