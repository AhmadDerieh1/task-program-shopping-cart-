window.onload=async()=>{
    const productsContainer=document.getElementById("products")
    let products=localStorage.getItem("products")
    if(products){

        console.log("this from local storage")

        products=JSON.parse(products)
    }else{
        try{
            const res=await fetch('https://fakestoreapi.com/products')
            const resObject =await res.json()
            localStorage.setItem("products",JSON.stringify(resObject))
            products=resObject;
            console.log(resObject)
            console.log("this from api")
        }catch(e){
            console.log(e)
        }

    }
    
    products.forEach(product=>{
        const card=createCard(product.title,product.price+"$",product.image)

        console.log(card)
        productsContainer.appendChild(card)
        
    })
    function createCard(title, text, imageUrl) {
        // Create a new div element
        var cardDiv = document.createElement("div");
        cardDiv.className = "card";
        cardDiv.style.width = "18rem";
    
        // Create an img element and set its attributes
        var img = document.createElement("img");
        img.className = "card-img-top";
        img.src = imageUrl;
        img.alt = "Card image cap";
    
        // Create a div element for the card body
        var cardBodyDiv = document.createElement("div");
        cardBodyDiv.className = "card-body";
    
        // Create an h5 element for the card title
        var cardTitle = document.createElement("h5");
        cardTitle.className = "card-title";
        cardTitle.textContent = title;
    
        // Create a p element for the card text
        var cardText = document.createElement("p");
        cardText.className = "card-text";
        cardText.textContent = text;
    
        // Create an a element for the button
        var button = document.createElement("a");
        button.href = "#";
        button.className = "btn btn-primary";
        button.textContent = "Go somewhere";
    
        // Append the created elements to build the card structure
        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText);
        cardBodyDiv.appendChild(button);
    
        cardDiv.appendChild(img);
        cardDiv.appendChild(cardBodyDiv);
        return cardDiv
    }
    

}