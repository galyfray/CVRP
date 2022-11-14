import React, {useEffect} from "react";
import "./App.css";
import logging from "./config/logging";
import {
    BrowserRouter as Router,
    Route,
    Switch
} from "react-router-dom";
import {getRoutes} from "./config/routes";
import {NotFoundPage} from "./pages/notFound";

/*
  Import logo from './logo.svg';
  <img src={logo} className="App-logo" alt="logo" />
*/

function App() {

    useEffect(() => {
        logging.info("Loading application");
    }, []);

    return (
        <div>
            <Router>
                <Switch>
                    {
                        getRoutes().map((route, index) => {
                            return <Route exact {...route} key={index} />;
                        })
                    }
                    <Route component={NotFoundPage} />
                </Switch>
            </Router>
        </div>
    );
}

export default App;
