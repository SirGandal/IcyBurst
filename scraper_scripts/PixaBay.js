/**
 * Usage
 * 1. Navigate to https://pixabay.com/ and perform a search (i.e. "British Columbia")
 * 2. Press F12 to open the console
 * 3. Scroll down to reach the bottom of the page
 * 4. Paste the code below and wait for CSV file to be downloaded
 * 5. If a next page is available click on Next page and repeat steps 3 and 4
 */

var items = document.querySelectorAll('.item');
var data = [["DOWNLOAD URL", "ORIGINAL LINK", "TAGS"]]
for(var i=0;i<items.length;i++){
    let originalLink = items[i].querySelector('a').href;
	let img = items[i].querySelector('img');
	let imgTags = img.alt;
	let imgDownloadUrl = img.src.replace("__340", "_1280");
    data.push([imgDownloadUrl, originalLink, `"${imgTags}"`]);
}

downloadCSV(data);

function downloadCSV(data){
    var dataString = "";
    var csvContent = "data:text/csv;charset=utf-8,";
    data.forEach(function (dataArray, index) {
        dataString = dataArray.join(",");
        csvContent += index < data.length ? dataString + "\n" : dataString;
    });
     var encodedUri = encodeURI(csvContent);
     downloadURI(encodedUri, "PixabayUrls_BritishColumbia.csv");
}

function downloadURI(uri, name) {
    var link = document.createElement("a");
    // Note that changing the name of the download only happens on same origin URLs
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}