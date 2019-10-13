let list=[];

ShoppingCart = function(){
	this.count = function(){
    	let n = 0;
    	for(let i of list)
    	{
    		n = n + i.quantity;
    	}
    	items.innerHTML = n + " items";
    }
	this.process = function(name){
		let flag = 0;
		for(let e of list)
		{
			if(e.name == name)
			{
				flag = 1;
				e.quantity++;
				e.nodo.childNodes[1].innerHTML ="Quantity: " + e.quantity;
			}
		}
		if(flag == 0)
		{    
			let nodo = document.createElement("div");
            nodo.setAttribute("class","product");
			let e = {  name : name,
			           quantity : 1,
			           nodo : nodo, 
			         };
		    list.push(e);
		    list.sort(function(a,b){
		    	let nome1 = a.name;
		    	let nome2 = b.name;
		    	if(nome1>nome2) return 1;
		    	if(nome2>nome1) return -1;
		    	else return 0;
		    });
          // creando elementi direttamente qui:
		    let span1 = document.createElement("div");
		    span1.setAttribute("class","nameProduct");
		    let span2 = document.createElement("div");
		    span2.setAttribute("class","quantityProduct");
		    let buttons = document.createElement("div");
		    let b1 = document.createElement("button");
		    b1.setAttribute("class","add button add glyphicon glyphicon-plus");
		    //b1.innerHTML = "+";
		    let b2 = document.createElement("button");
		    b2.setAttribute("class","minus glyphicon glyphicon-minus");
		    //b2.innerHTML = "-";
		    let b3 = document.createElement("button");
		    b3.setAttribute("class","clear button add glyphicon glyphicon-trash");
		    //b3.innerHTML = "x";
		    buttons.appendChild(b1);
		    buttons.appendChild(b2);
            buttons.appendChild(b3);
		    buttons.setAttribute("class","items");
            span1.innerHTML = "Product: " + name;
            span2.innerHTML = "Quantity: " + e.quantity;
            nodo.appendChild(span1);
            nodo.appendChild(span2);
            nodo.appendChild(buttons);
            
             for(let i of list){
             	panel3.appendChild(i.nodo);
             }
            //panel3.appendChild(nodo);
            b1.onclick = function(){
                e.quantity++; 
                span2.innerHTML = "Quantity: " + e.quantity; 
                //this.count() NON FUNZIONA, COSI FUNZIONA MA FA SCHIFO... WHAT?!?!?!!?!?!!?
                carrello.count(); 
		    }
		    b2.onclick = function(){  
			    e.quantity--;
			    if(e.quantity <= 0){
			    	nodo.remove();
			    	let i = list.indexOf(e);
			    	list.splice(i,1);
			    }
			    span2.innerHTML = "Quantity: " + e.quantity;
			    carrello.count();		    
		    }
		    b3.onclick = function(){
		        nodo.remove();
		        let i = list.indexOf(e);
		        list.splice(i,1);
		        carrello.count();
            }
		} 
        /* creando cloni:

		let o = document.getElementById("product");

		let panel = o.cloneNode(true);

		document.getElementById("nameProduct").innerHTML = name;
		document.getElementById("quantityProduct").innerHTML = 1;
	
        document.getElementById("panel3")
                .insertAdjacentElement("beforeend",panel);
     */
	} 
    this.clear = function(){
        for( let i of list )
        {
        	i.nodo.remove();
        	list = [];
        }
    }
}
key = 'AIzaSyDCXWiAe7bmEYrtL0GoI2-cOXpOKCeBdqM';
name_projecy = 'SmartRestaurantIoT';
id_project = 'smartrestaurantiot';
config = {
	'apiKey': key,
	'authDomain': id_project+'.firebaseapp.com',
	'databaseURL': 'https://smartrestaurantiot.firebaseio.com',
	'storageBucket': id_project+'.appspot.com'	
};
firebase.initializeApp(config)
let db = firebase.database()
let carrello = new ShoppingCart();
let punt=0;
menu = {
	'Primo':['Pasta','Risotto con le Erbette'],
	'Secondo':['Carne', 'Pesce']
}
let keys;
window.onload = function(){
	let menuRef = db.ref('Menu');
	
	let values;
	console.log(menuRef)
	menuRef.on('value', function(snapshot){
		console.log(snapshot.val())
		snapshot.forEach(function(childSnapshot){
			let obj = childSnapshot.val();
			keys = Object.keys(obj);
			// for(let k in keys){
			// 	values.push(obj[k])
			// }
		})
	})
	// console.log(values)
}

Enter2.onclick = function(){
	// let newClientKey = db.ref().child('Menu').push().key;
	// console.log(newClientKey)
	// db.ref('Menu/'+newClientKey).set(menu)
	bt2 = document.getElementById('dropdownMenu');
	a = document.createElement('a');
	a.setAttribute('class','dropdown-item');
	a.setAttribute('name',keys[0])
	bt2.appendChild(a)
}

// Enter.onclick = function(){
	// var leadsRef = db.ref('leads');
	// leadsRef.on('value', function(snapshot) {
	//     snapshot.forEach(function(childSnapshot) {
	//       var childData = childSnapshot.val();
	//       console.log(childData['name'])
	//     });
	// });	
// }


onkeydown = function(e){
	if(e.keyCode == 38 && punt>=0){
      punt--;
      Enter.value = list[punt].name;
      list[punt+1].nodo.setAttribute("class","product");
      list[punt].nodo.setAttribute("class","product_selected");
	}

	if(e.keyCode == 40 && punt<=list.length){        
      punt++;
      Enter.value = list[punt].name;
      list[punt-1].nodo.setAttribute("class","product");	
      list[punt].nodo.setAttribute("class","product_selected");
	}
	if(e.keyCode == 13){       
		carrello.process(Enter.value);
	    carrello.count();
	}
}
add.onclick = function(){
	carrello.process(Enter.value);
	carrello.count();
}
clear.onclick = function(){
   carrello.clear();
   carrello.count();
}

