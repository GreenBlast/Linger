var webpack = require('webpack');
var path = require('path');

var buildPath = path.resolve(__dirname, 'build');
var nodeModulesPath = path.resolve(__dirname, 'node_modules');

var config = {
  entry: ['babel-polyfill', './app.js'],
  // Render source-map file for final build
  devtool: 'source-map',
  // output config
  output: {
    path: buildPath, // Path of output file
    filename: 'app.js', // Name of output file
    publicPath: "/build/",
  },
  plugins: [
    new webpack.ProvidePlugin({
            "React": "react",
        }),
  ],
  module: {
    loaders: [
      {
        test: /\.js$/, // All .js files
        loader: 'babel-loader', // react-hot is like browser sync and babel loads jsx and es6-7
        exclude: nodeModulesPath
      },
    ],
  },
  watchOptions: { aggregateTimeout: 300, poll: 1000 },
};

module.exports = config;
