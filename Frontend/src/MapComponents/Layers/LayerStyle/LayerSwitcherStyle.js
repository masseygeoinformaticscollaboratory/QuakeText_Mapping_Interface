import {impactLabels} from "./labels";
import React from "react";

export function setSwitcherHeight(itemsNum) {
    let container = document.querySelector('.layer-switcher');
    container.style.height = `${itemsNum * 29}px`
}
