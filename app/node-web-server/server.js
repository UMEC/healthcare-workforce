const express = require('express');
var app = express();
var formidable = require('formidable');
var fs = require('fs');
if(typeof require !== 'undefined') XLSX = require('xlsx');

 
app.get('/sourceupload', (req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('<form action="source" method="post" enctype="multipart/form-data">');
    res.write('<input type="file" name="filetoupload"><br>');
    res.write('<input type="submit">');
    res.write('</form>');
    return res.end();
});

app.get('/source', (req, res) => {
    res.writeHead(200, {'Content-Type': 'text/json'});
    fs.readdir("C:/workdir/processed/", function(err, items) {
        console.log(Array.isArray(items));
      
        let statResults = items.map( item => {
            var myfile = "C:/workdir/processed/" + item;
            console.log('looking at : ' + myfile);
            var stats = fs.statSync(myfile);
            var result = {};
            result.name = item;
            result.modified = stats["mtime"];
            result.size = stats["size"];
            return result;
        });
        res.write(JSON.stringify(statResults));
        return res.end();
    });
});

app.post('/source', (req, res) => {
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
      var oldpath = files.filetoupload.path;
      var newpath = 'C:/workdir/upload/' + files.filetoupload.name;
      fs.rename(oldpath, newpath, function (err) {
        if (err) throw err;
        res.write('File uploaded and moved!');
        var workbook = XLSX.readFile(newpath);
        var sheet_name_list = workbook.SheetNames;
        sheet_name_list.forEach(function(y) { /* iterate through sheets */
            console.log("Processing sheet name : " + y);
            var worksheet = workbook.Sheets[y];
            var csv = XLSX.utils.sheet_to_csv(worksheet)
            fs.writeFile('C:/workdir/processed/' + y + ".csv", csv, (err) => {  
                // throws an error, you could also catch it here
                if (err) throw err;
            
                // success case, the file was saved
                console.log('Saved csv: ' + y);
            });
        });
        res.end();
      });
    });
});

app.listen(process.env.PORT || 3000)