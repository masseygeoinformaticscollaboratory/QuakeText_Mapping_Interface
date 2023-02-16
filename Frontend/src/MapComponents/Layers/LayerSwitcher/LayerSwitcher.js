import React, {useState} from "react";
import {impactLabels} from "./LayerSwitcherStyles/labels";
import "./LayerSwitcherStyles/labels.css"
import {getIcon} from "./LayerSwitcherStyles/LayerSwitcherStyle";


function LayerSwitcher(props) {

    //Adds layer switcher control panel so user can switch between impact layers
    const [checkedState, setCheckedState] = useState(
        new Array(impactLabels.length).fill(true)
    );

    //Handles when a checkbox state changes
    const handleOnChange = (position) => {
        const updatedCheckedState = checkedState.map((item, index) =>
            index === position ? !item : item
        );
        setCheckedState(updatedCheckedState);

        const impact = props.impactLayers.getLayers().getArray()[position];

        if (impact.getVisible()) {
            impact.setVisible(false)
        } else {
            impact.setVisible(true)
        }

        props.popup.current.style.display = "none";
    }


    return (
        <div className="layer-switcher">
            <h4>Select Impacts</h4>
            <ul className="impacts-list">
                {impactLabels.map(({impact}, index) => {
                    return (
                        <div key={index}>
                            <div className="impact-list-item">
                                <input
                                    type="checkbox"
                                    id={`custom-checkbox-${index}`}
                                    name={impact}
                                    value={impact}
                                    checked={checkedState[index]}
                                    onChange={() => handleOnChange(index)}
                                />
                                <label htmlFor={`custom-checkbox-${index}`}>
                                    <span>{impact}   </span>
                                    <img src = {getIcon({impact}.impact)}  alt=""/>
                                </label>

                            </div>

                        </div>
                    );
                })}


            </ul>
        </div>
    );

}

export default LayerSwitcher;
