var webpack = require('webpack');
var path = require('path');

var buildPath = path.resolve(__dirname, 'build');
var nodeModulesPath = path.resolve(__dirname, 'node_modules');

var config = {
  entry: [
  'webpack/hot/dev-server',
  'webpack/hot/only-dev-server',
  'babel-polyfill',  
  './app.js'],
  // Render source-map file for final build
    // Server Configuration options
    devServer: {
    contentBase: '.', // Relative directory for base of server
    devtool: 'eval',
    hot: true, // Live-reload
    inline: true,
    port: 3000, // Port Number
    host: '0.0.0.0', // Change to '0.0.0.0' for external facing server
  },
  devtool: 'eval',
  // output config
  output: {
    path: buildPath, // Path of output file
    filename: 'app.js', // Name of output file
    publicPath: "/build/",
  },

  plugins: [
    // Enables Hot Modules Replacement
    new webpack.HotModuleReplacementPlugin(),
    // Allows error warnings but does not stop compiling.
    new webpack.NoErrorsPlugin(),
    new webpack.ProvidePlugin({
            "React": "react",
        }),
    ],
    module: {
      loaders: [
      {
        // React-hot loader and
        test: /\.js$/, // All .js files
        loaders: ['react-hot', 'babel-loader'], // react-hot is like browser sync and babel loads jsx and es6-7
        exclude: [nodeModulesPath],
      },
      ],
    },
    watchOptions: { aggregateTimeout: 300, poll: 1000 },
  };

  module.exports = config;
