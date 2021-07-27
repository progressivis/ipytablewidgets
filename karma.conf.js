module.exports = function (config) {
  config.set({
    basePath: '.',
    frameworks: ['mocha', 'karma-typescript'],
      reporters: ['mocha', 'karma-typescript', 'coverage'],
    client: {
      mocha: {
        timeout : 15000,
        retries: 3
      }
    },
    files: [ { pattern: "src/**/*.ts" }],
      exclude: ["src/types.d.ts"],
    preprocessors: {
	'src/*.ts': ['karma-typescript', 'coverage'],
	'src/tests/*.ts': ['karma-typescript']
    },
    browserNoActivityTimeout: 30000,
    port: 9876,
    colors: true,
    singleRun: !config.debug,
    logLevel: config.LOG_INFO,

    customLaunchers: {
      ChromeCI: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox']
      }
    },

    karmaTypescriptConfig: {
      tsconfig: 'src/tests/tsconfig.json',
      reports: {
        "text-summary": "",
        "html": "coverage",
        "lcovonly": {
          "directory": "coverage",
          "filename": "coverage.lcov"
        }
      },
      bundlerOptions: {
        sourceMap: false,  // bug ?
        acornOptions: {
          ecmaVersion: 8,
        },
        transforms: [
          require("karma-typescript-es6-transform")({
            presets: [
              ["@babel/preset-env", {
                targets: {
                  browsers: ["last 2 Chrome versions"]
                },
              }]
            ]
          })
        ]
      }
    }
  });
};
