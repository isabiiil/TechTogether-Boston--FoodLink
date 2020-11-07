const api_key = process.env.api_key;
   const HtmlWebpackPlugin = require('html-webpack-plugin');
    
    module.exports = {
      entry: './map.js',
      plugins: [
        new HtmlWebpackPlugin({
          inject: false,
          template: './../templates/home.html',

          // Pass the full url with the key!
          apiUrl: `https://maps.googleapis.com/maps/api/js?key=${api_key}&callback=initMap&libraries=places&v=weekly`,

        })
      ]
    }
    