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
  //
  Object.assign({}, commonConfig, {
    entry: "./src/index.ts",
    output: {
      filename: "index.js",
      library: "nbextensions/ipytablewidgets/index",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    }
  }),
  // the widget extension
  Object.assign({}, commonConfig, {
    entry: "./src/extension.ts",
    output: {
      filename: "extension.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: {
      "@jupyter-widgets/base": "@jupyter-widgets/base",
      "./index": "nbextensions/ipytablewidgets/index"
    }
  })
];
