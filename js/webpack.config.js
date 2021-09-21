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

const outputPath = __dirname + "/ipytablewidgets/static";
const outputLibraryTarget = "amd";

module.exports = [
  Object.assign({}, commonConfig, {
    entry: "./src/extension.ts",
    output: {
      filename: "extension.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
  }),
  //
  Object.assign({}, commonConfig, {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: ["@jupyter-widgets/base"]
  }),
  Object.assign({}, commonConfig, {
    entry: "./src/labplugin.ts",
    output: {
      filename: "labplugin.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: ["@jupyter-widgets/base"]
  }),
];
