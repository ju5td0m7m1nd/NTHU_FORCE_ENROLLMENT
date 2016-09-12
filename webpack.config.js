var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: [
        './component/app.js'
    ],
    output: {
        path: path.join(__dirname, 'linggleNUI/static/build/'),
        filename: 'bundle.js',
    },
    externals: {
        "socket.io": "io"
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        loaders: [{
            test: /\.js$|\.jsx$/,
            loaders: ['babel'],
            exclude: /node_modules/,
            include: __dirname
        },
        {                                                                                                            
           test: /\.css$/, loader: 'style-loader!css-loader',
           include: [
             /bower_components/,
             /node_modules/
           ],},
        ]
    },
};

