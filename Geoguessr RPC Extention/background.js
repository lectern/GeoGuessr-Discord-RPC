function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function updateRPC() {
    while (true) {
        // get all the tabs

        chrome.tabs.getAllInWindow(null, function(tabs){
            for (var i = 0; i < tabs.length; i++) {
                // send to api if GeoGuessr is found
                if (tabs[i].title.includes('GeoGuessr')) {
                    fetch('http://127.0.0.1:5000/rpc', {
                        method: 'POST',
                        headers: {
                            'Accept':'application/json',
                            'Content-type':'application/json'
                        },
                        body: JSON.stringify({ 
                            "title": tabs[i].title,
                            "url": tabs[i].url 
                        })
                    })
                        .then(response => response.json())
                        .then(response => console.log(JSON.stringify(response)))
                    break;
                }       
            }
        });
        await sleep(2500);
    }
}

updateRPC();