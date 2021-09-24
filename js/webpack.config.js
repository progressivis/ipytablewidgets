const path = require('path');
const nbextPass = path.resolve(__dirname, '../ipytablewidgets/static');
const distPass = path.resolve(__dirname, 'dist');

const outputLibraryTarget = "amd";
const rules = [];

module.exports = [
  {
    // Notebook extension
    entry: './lib/extension.js',
    output: {
      filename: 'extension.js',
      path: nbextPass,
      libraryTarget: outputLibraryTarget
    },
    externals: ['@jupyter-widgets/base'],
    mode: 'production',
  },
  {
    entry: './lib/index.js',
    output: {
      filename: 'index.js',
      path: nbextPass,
      libraryTarget: outputLibraryTarget
    },
    devtool: 'source-map',
    module: {
      rules: rules,
    },
    externals: ['@jupyter-widgets/base'],
    mode: 'production',
  },
  {
    entry: './lib/index.js',
    output: {
      filename: 'index.js',
      path: distPass,
      libraryTarget: outputLibraryTarget
    },
    devtool: 'source-map',
    module: {
      rules: rules,
    },
    externals: ['@jupyter-widgets/base'],
    mode: 'production',
  },
];
