import "@testing-library/jest-dom";
import logging from "../config/logging";

describe("Logging", () => {
    test("the logging functions", () => {
        const fieldType = () => "";
        expect(typeof fieldType).toBe(typeof logging.info);
        expect(typeof fieldType).toBe(typeof logging.error);
        expect(typeof fieldType).toBe(typeof logging.warn);
        const loggingType = {
            "error": fieldType, "info": fieldType, "warn": fieldType
        };
        expect(typeof loggingType).toBe(typeof logging);
    });
});