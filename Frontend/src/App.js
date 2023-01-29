import Map from "./MapComponents/Map";
import './App.css';
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
