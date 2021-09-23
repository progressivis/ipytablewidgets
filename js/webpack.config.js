const commonConfig = {
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: "ts-loader"
      }
    ]
  }
};

const outputPath = __dirname + "/../ipytablewidgets/static/";
const outputLibPath = __dirname + "/lib";
const outputLibraryTarget = "amd";

module.exports = [
  Object.assign({}, commonConfig, {
    entry: "./lib/extension.js",
    output: {
      filename: "extension.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
  }),
  //
  Object.assign({}, commonConfig, {
    entry: "./lib/index.js",
    output: {
      filename: "index.js",
      path: outputLibPath,
      libraryTarget: outputLibraryTarget
    },
    externals: ["@jupyter-widgets/base"]
  }),
  Object.assign({}, commonConfig, {
    entry: "./lib/index.js",
    output: {
      filename: "index.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: ["@jupyter-widgets/base"]
  }),
  Object.assign({}, commonConfig, {
    entry: "./lib/labplugin.js",
    output: {
      filename: "labplugin.js",
      path: outputLibPath,
      libraryTarget: outputLibraryTarget
    },
    externals: ["@jupyter-widgets/base"]
  }),
];
