fetch("/catalog/mas/0")
    .then(response => {
        return response.json(); 
    })
    .then(data => {
        console.log(data); 
    })
    .catch(error => {
        console.error(error);
    });