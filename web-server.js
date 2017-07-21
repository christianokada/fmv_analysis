var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(8124, function(){
    console.log('Server running on 8124...');
});
