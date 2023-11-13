document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("searchInput");
  const button = document.getElementById("button");
  const resultsContainer = document.getElementById("results");

  const displayResults = (results) => {
    resultsContainer.innerHTML += `<div class="results__counter">${results.length} resultados</div>`

    results.forEach(item => {

      let content = ""
      content += `
      <article class="card">
            <div class="card__container">
              <h3 class="card__title">${item["title"]}</h3>
              <ul class="card__authors">`;
      
      const authors = item["authors"];
      console.log(authors)
      authors.pop()

      authors.forEach(author => 
        {content += `<li class="card__author">${author}</li>`}
      );

      content += `
            </ul>
              <p class="card__abstract">${item["abstract"]}</p>
            </div>
      </article>`;

      resultsContainer.innerHTML += content;
    });


  };

  const search = () => {
    const words = input.value;
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

    fetch("http://54.242.250.215:8000/search", requestOptions)
      .then((response) => response.json())
      .then((data) => displayResults(data))
      .catch((error) => console.error("Error:", error));
  };
  
  button.addEventListener("click", () => {
    resultsContainer.innerHTML = ""
    search();
  });

  input.addEventListener("keypress", event => {
    if(event.key === 'Enter'){
      button.click();
    }
  })

});
