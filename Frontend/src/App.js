import './App.css';

import React from "react";
import Map from "./MapComponents/Map";

//This is the main App component
function App() {

    return (
        <div className="App">
            <div className="header">
                <h1>Quake Text</h1>
            </div>
            <div className="map">
                <Map/>
            </div>

        </div>
    );
}

export default App;
