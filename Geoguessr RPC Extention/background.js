async function updateRPC() {

    var title = "";
    var url = "";

    chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
        if (tab.url.includes("geoguessr.com") && (title.localeCompare(tab.title) || url.localeCompare(tab.url))) {
            console.log(tab.title);
            console.log(tab.url);

            title = tab.title;
            url = tab.url;

            fetch('http://127.0.0.1:5000/rpc', {
                method: 'POST',
                headers: {
                    'Accept':'application/json',
                    'Content-type':'application/json'
                },
                body: JSON.stringify({ 
                    "title": title,
                    "url": url 
                })
            })
                .then(response => response.json())
                .then(response => console.log(JSON.stringify(response)))
        }
     });
}

updateRPC();