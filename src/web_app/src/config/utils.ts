import {Link} from "../types/d3Types";

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