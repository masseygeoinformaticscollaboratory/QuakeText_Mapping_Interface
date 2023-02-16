import React from "react";
import damageIcon from "./icons/damageIcon.png"
import deathIcon from "./icons/deathIcon.png"
import fireIcon from "./icons/fireIcon.png"
import floodIcon from "./icons/floodIcon.png"
import injuryIcon from "./icons/injuryIcon.png"
import missingIcon from "./icons/missingIcon.png"
import otherIcon from "./icons/otherIcon.png"
import terrorismIcon from "./icons/terrorismIcon.png"
import trappedIcon from "./icons/trappedIcon.png"

//Sets the height of the layer swticher based on how many layers there are
export function setSwitcherHeight(itemsNum) {
    let container = document.querySelector('.layer-switcher');
    container.style.height = `${itemsNum * 29}px`
}

//Returns the Appropriate Icon based on input string
export function getIcon(impact) {
    switch (impact.toLowerCase() ){
        case "damage":
            return damageIcon;
        case "death":
            return deathIcon;
        case "fire":
            return fireIcon;
        case "flood":
            return floodIcon;
        case "injury":
            return injuryIcon;
        case "missing":
            return missingIcon;
        case "other":
            return otherIcon;
        case "terrorism":
            return terrorismIcon;
        case "trapped":
            return trappedIcon;
    }
}