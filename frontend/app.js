const displayResults = (results) => {
    var resultsContainer = document.getElementById("results");
  
    resultsContainer.innerHTML = "";
  
    results.forEach(function (item) {
      var card = document.createElement("div");
      card.className = "card";
      card.innerHTML = "<h3>" + item[0] + "</h3>" + "<p>" + item[1] + "</p>";
      resultsContainer.appendChild(card);
    });
  };

const search = () => {
  var words = document.getElementById("searchInput").value;

  const dataToSend = {
    words: words,
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataToSend),
  };

  fetch("http://204.236.220.115:8000/search", requestOptions)
    .then((response) => response.json())
    .then((data) => displayResults(data))
    .catch((error) => console.error("Error:", error));
};

var button = document.getElementById("button");
window.addEventListener('click', () =>{
    search();
})