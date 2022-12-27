import {Link} from "../types/d3Types";
import * as Types from "../types/data";

export function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0;i < 6;i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

export function getLinks(sol: []) {
    const links:Array<Link> = [];
    let i = 0;
    while (i < sol.length - 1) {
        const d = {
            "source": sol[i],
            "target": sol[i + 1]
        };
        i += 1;
        links.push(d);
    }
    return links;
}

export function getFitness(data: Array<Types.individual>) {
    return data.map(d => d.fitness);
}

export function getMinFitness(data: Array<Types.individual>) {
    return Math.min(...getFitness(data));
}
