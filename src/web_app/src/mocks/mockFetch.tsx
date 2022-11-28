const datasets = [
    {
        "name"   : "E-n112-k8-s11.evrp",
        "details": "112 villes - 8 véhicules - 11 stations"
    }
];
const entries1 = {"data": datasets};


// eslint-disable-next-line @typescript-eslint/require-await
export default async function mockFetch(url: URL | RequestInfo) {
    switch (url) {
    case "http://127.0.0.1:5000/benchmarks": {
        return {
            ok    : true,
            status: 200,
            json  : () => datasets,
        };
    }
    default: {
        // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
        throw new Error(`Unhandled request: ${url}`);
    }
    }
}