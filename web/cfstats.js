/*
 * NotEnoughGraphs: export detailed stats about your cf points earnings as json
 * LICENSE : Public Domain, https://creativecommons.org/publicdomain/zero/1.0
 * AUTHOR  : LukeGrahamLandry#6888
 * SOURCE  : https://moddingtutorials.org/cfstats.js
 * UPDATED : November 5, 2022 
 * 
 * Usage 
 * 1. go to https://authors.curseforge.com/store/transactions
 * 2. inspect element and open the console 
 * 3. paste this whole script there (and press enter)
 * 4. wait like a minute for it to run
 * 5. copy the json data from the text box that's added to the top of the page
 * 
 * Note About Security
 * please be careful about pasting random scripts into the console of websites where you're logged in 
 * curseforge requires a 2FA code to withdraw points so i couldn't steal your money even if i wanted to
 * but as a matter of principle you should still review this code to see that i'm not being evil :)
 */ 

(() => {
    function uncheckCheckbox(id, callback){
        let checkbox = document.getElementById(id);
        if (checkbox.checked) checkbox.click();
        window.setTimeout(callback, 500);
    }

    function loadAllTransactions(callback){
        let showMoreButton = document.getElementById("more");

        function tryLoadMoreTransactions(){
            if (showMoreButton.classList.contains("loading")){
                window.setTimeout(tryLoadMoreTransactions, 100);
                return;
            }

            if (showMoreButton.classList.contains("disabled")){
                callback();
                return;
            }

            console.log("loading transactions...");
            showMoreButton.click();
            window.setTimeout(tryLoadMoreTransactions, 100);
        }

        tryLoadMoreTransactions();
    }

    function parseDataFromPage(){
        let data = [];

        let transactionGroups = document.getElementsByClassName("transactions");
        for (let i=0;i<transactionGroups.length;i++){
            let transactionElement = transactionGroups[i];
            let date = parseInt(transactionElement.getElementsByTagName("abbr")[0].dataset.epoch);
            let rewardsElement = transactionElement.getElementsByClassName("sub-reward-item")[0];
            if (rewardsElement == undefined) continue;

            let rewardsElements = rewardsElement.getElementsByTagName("li");

            let dataEntry = {
                epoch: date,
                date: new Date(date * 1000).toDateString(),
                total: parseFloat(transactionElement.getElementsByTagName("strong")[0].innerText),
                projects: {}
            }

            for (let i=0;i<rewardsElements.length;i++){
                let rewardData = rewardsElements[i];
                let amount = parseFloat(rewardData.getElementsByTagName("b")[0].innerText);
                let project = rewardData.getElementsByTagName("a")[0].innerText;
                dataEntry.projects[project] = amount;
            }

            data.push(dataEntry);
        }

        return data; 
    }

    function addToPageAsTextBox(dataSupplier){
        let data = dataSupplier();
        let outputArea = document.createElement("textarea");
        outputArea.innerText = JSON.stringify(data);
        outputArea.id = "notenoughgraphsdataoutput";
        document.getElementsByClassName("transaction-header")[0].appendChild(outputArea);
        window.scrollTo(0, 0);
    }

    let oldOutputElement = document.getElementById("notenoughgraphsdataoutput");
    if (oldOutputElement != undefined) oldOutputElement.remove();
    
    (
        () => uncheckCheckbox("orders", 
        () => uncheckCheckbox("transfers", 
        () => loadAllTransactions(
        () => addToPageAsTextBox(
        () => parseDataFromPage()
    )))))();
})();