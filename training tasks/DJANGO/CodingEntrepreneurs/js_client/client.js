
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const baseEndPoint = "http://localhost:8000/api"
const contentContainer = document.getElementById('content-container')


if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
}

function handleSearch(event) {
    console.log(event);
    event.preventDefault();

    let formData = new FormData(searchForm);
    let data = Object.fromEntries(formData);

    let searchParams = new URLSearchParams(data)

    const endPoint = `${baseEndPoint}/search/?${searchParams}`;

    const headers = {
        "Content-Type": "application/json"
    }

    const authToken = localStorage.getItem('access')
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`
    }

    const options = {
        method: "GET",
        headers: headers
    };
    fetch(endPoint, options)
    .then(response=>{
        console.log(response);
        return response.json();
    })
    .then(data=>{
        const validData = isTokenNotValid(data)
        if (validData && contentContainer) {
            contentContainer.innerHTML = ""
            if (data && data.hits) {
                let htmlStr = ""
                for (let result of data.hits) {
                    htmlStr += `<li>${result.title}</li>`
                }
                contentContainer.innerHTML = htmlStr
                if (data.hits.length === 0) {
                    contentContainer.innerHTML = `<p>No Results Found!</p>`
                }
            }
            else {
                contentContainer.innerHTML = `<p>No Results Found!</p>`
            }
        }
    })
    .catch(err=>{
        console.log('errr: ', err);
    })

}

function handleLogin(event) {
    console.log(event);
    event.preventDefault();

    const loginEndPoint = `${baseEndPoint}/token/`;
    let loginFormData = new FormData(loginForm);
    let loginObjectData = Object.fromEntries(loginFormData);

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginObjectData)
    };
    fetch(loginEndPoint, options)
    .then(response=>{
        console.log(response);
        return response.json();
    })
    .then(authData=>{
        handleAuthData(authData, getProductList)
    })
    .catch(err=>{
        console.log('errr: ', err);
    })

}


function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access);
    localStorage.setItem('refresh', authData.refresh);

    if (callback) {
        callback() 
    }
}

function getFetchOption(method, body) {
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type": 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = `<pre> ${JSON.stringify(data, null,4)} </pre>`
    }
}

function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid") {
        alert('Please login again')
        return false;
    }
    return true;

}

function validateJWTToken() {
    const endPoint = `${baseEndPoint}/token/verify/`;
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    }
    fetch(endPoint, options)
    .then(response=>response.json())
    .then(x=>{
        // console.log(x)
        // isTokenNotValid(x);
        // refreshing or whatever
    })
}

function getProductList() {
    const endPoint = `${baseEndPoint}/products/`;
    const options = getFetchOption()
    fetch(endPoint, options)
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        const validData = isTokenNotValid(data);
        if (validData) {
            writeToContainer(data);
        }
    })


}
validateJWTToken();
// getProductList();


const searchClient = algoliasearch('JO1NB72443', '9d0fddbcea6190de38a8b11c6929b6e1');

const search = instantsearch({
  indexName: 'cfe_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  instantsearch.widgets.clearRefinements({
      container: "#clear-refinements",
  }),

  instantsearch.widgets.refinementList({
      container: "#user-list",
      attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
      container: "#public-list",
      attribute: 'public'
  }),

  instantsearch.widgets.hits({
    container: '#hits',
      templates: {
        item: `
               <div>
               <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
               <div>{{#helpers.highlight}}{ "attribute": "content" }{{/helpers.highlight}}</div>
               <br>
               {{ user }}<br>\${{ price }}</div>`
      }
  })
]);

search.start();
