import React, {useState} from "react";
import {impactLabels} from "./LayerStyle/labels";
import "./LayerStyle/labels.css"

function LayerSwitcher(props) {

    const [checkedState, setCheckedState] = useState(
        new Array(impactLabels.length).fill(true)
    );

    const handleOnChange = (position) => {
        const updatedCheckedState = checkedState.map((item, index) =>
            index === position ? !item : item
        );
        setCheckedState(updatedCheckedState);

       // let impact = impactLabels[position].get("impact");

       const impact = props.impactLayers.getLayers();
       //TODO: https://openlayers.org/en/latest/apidoc/module-ol_layer_Group-LayerGroup.html this will be handy
    }

    return (
        <div className="layer-switcher">
            <h4>Select Impacts</h4>
            <ul className="impacts-list">
                {impactLabels.map(({impact}, index) => {
                    return (
                        <div className="impact-list-item">
                            <input
                                type="checkbox"
                                id={`custom-checkbox-${index}`}
                                name={impact}
                                value={impact}
                                checked={checkedState[index]}
                                onChange={() => handleOnChange(index)}
                            />
                            <label htmlFor={`custom-checkbox-${index}`}>{impact}</label>

                        </div>

                    );
                })}

            </ul>
        </div>
    );
}

export default LayerSwitcher;

/*
 return (

        <div className="layer-switcher">
            Filter by Impact:
            <div>
                <input type="checkbox" name="damage" value="damage" id="damage" defaultChecked={true}/>
                <label htmlFor="damage">Damage</label>
            </div>
            <div><
                input type="checkbox" name="death" value="death" id="death" defaultChecked={true}/>
                <label htmlFor="death">Deaths</label>
            </div>
            <div>
                <input type="checkbox" name="fire" value="fire" id="fire" defaultChecked={true}/>
                <label htmlFor="fire">Fire</label>
            </div>
            <div>
                <input type="checkbox" name="flood" value="flood" id="flood" defaultChecked={true}/>
                <label htmlFor="flood">Flooding</label>
            </div>
            <div>
                <input type="checkbox" name="injury" value="injury" id="injury" defaultChecked={true}/>
                <label htmlFor="injury">Injuries</label>
            </div>
            <div>
                <input type="checkbox" name="missing" value="missing" id="missing" defaultChecked={true}/>
                <label htmlFor="missing">Missing Persons</label>
            </div>
            <div>
                <input type="checkbox" name="other" value="other" id="other" defaultChecked={true}/>
                <label htmlFor="other">Other</label>
            </div>
            <div>
                <input type="checkbox" name="terrorism" value="terrorism" id="terrorism" defaultChecked={true}/>
                <label htmlFor="terrorism">Terrorism</label>
            </div>
            <div>
                <input type="checkbox" name="trap" value="trap" id="trap" defaultChecked={true}/>
                <label htmlFor="trap">Trapped</label>
            </div>

        </div>

    );
 */