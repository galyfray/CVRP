import {Link} from "../types/d3Types";
import * as Types from "../types/data";
import * as d3Types from "../types/d3Types";

function randomInteger(max: number) {
    return Math.floor(Math.random()*(max + 1));
}

function randomRgbColor() {
    const r = randomInteger(255);
    const g = randomInteger(255);
    const b = randomInteger(255);
    return [r,g,b];
}

export function getRandomColor() {
    const [r,g,b] =randomRgbColor();

    const hr = r.toString(16).padStart(2, '0');
    const hg = g.toString(16).padStart(2, '0');
    const hb = b.toString(16).padStart(2, '0');

    return "#" + hr + hg + hb;
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

export function getCoordsX(nodes: Array<d3Types.Node>) {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return nodes[0].data.map(d => d.x);
}

export function getCoordsY(nodes: Array<d3Types.Node>) {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return nodes[0].data.map(d => d.y);
}

export function getMinX(nodes: Array<d3Types.Node>) {
    return Math.min(...getCoordsX(nodes));
}

export function getMaxX(nodes: Array<d3Types.Node>) {
    return Math.max(...getCoordsX(nodes));
}

export function getMinY(nodes: Array<d3Types.Node>) {
    return Math.min(...getCoordsY(nodes));
}

export function getMaxY(nodes: Array<d3Types.Node>) {
    return Math.max(...getCoordsY(nodes));
}
