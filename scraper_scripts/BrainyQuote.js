/**
 * Usage
 * 1. Navigate to https://www.brainyquote.com/ and perform a search (i.e. "nature")
 * 2. Press F12 to open the console
 * 3. Scroll down to reach the bottom of the page (keep pressing Page Down on the keyboard works)
 * 4. Paste the code below and wait for CSV file to be downloaded
 * 5. If a next page is available click on Next page and repeat steps 3 and 4
 */

var quotesItems = document.getElementsByClassName("grid-item");var items = document.querySelectorAll('.item');
var data = [["QUOTE", "AUTHOR"]]
for(var i=0; i<quotesItems.length; i++){
	let quoteChildNodes = quotesItems[i].childNodes;
	for (var j = 0; j < quoteChildNodes.length; j++) {
    	if (quoteChildNodes[j].className && quoteChildNodes[j].className.indexOf("b-qt") !== -1) {
      		data.push([`"${quoteChildNodes[j].text}"`, `"${quoteChildNodes[j+2].text}"`]);
      		break;
    	} 
	}
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
     downloadURI(encodedUri, "brainyquote_nature.csv");
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