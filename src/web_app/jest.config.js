module.exports = {
    "roots": [
    "<rootDir>/src"
    ],
    "testMatch": [
    "**/__tests__/**/*.+(ts|tsx|js)",
    "**/?(*.)+(spec|test).+(ts|tsx|js)"
    ],
    "transform": {
    "^.+\\.(ts|tsx)$": "ts-jest",
    "^.+.(css|styl|less|sass|scss|png|PNG|jpg|ttf|woff|woff2)$": "jest-transform-stub"
    
    },
    moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
}
