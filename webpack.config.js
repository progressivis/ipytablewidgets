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
      library: "nbextensions/jupyter-tablewidgets/index",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    }
  }),
  // the widgets extension
  Object.assign({}, commonConfig, {
    entry: "./src/widgets.ts",
    output: {
      filename: "widgets.js",
      path: outputPath,
      libraryTarget: outputLibraryTarget
    },
    externals: {
      "@jupyter-widgets/base": "@jupyter-widgets/base",
      "./index": "nbextensions/jupyter-tablewidgets/index"
    }
  })
];
