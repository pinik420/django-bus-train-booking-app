//function esc(element) {
//    document.addEventListener('keydown', event => {
//        if(event.key === 'Escape') {
//            element.style.display = 'none';
//        }
//    });
//    element.parentElement.querySelector('input[type=text]').addEventListener("blur", () => {
//        setTimeout(() => {
//            element.style.display = 'none';
//        },80);
//    });
//}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#train-from").addEventListener("input", event => {
        train_from(event);
    });

    document.querySelector("#train-to").addEventListener("input", event => {
        train_to(event);
    });

    document.querySelector("#train-from").addEventListener("focus", event => {
        train_from(event, true);
    });

    document.querySelector("#train-to").addEventListener("focus", event => {
        train_to(event, true);
    });

    document.querySelector("#bus-from").addEventListener("input", event => {
        bus_from(event);
    });

    document.querySelector("#bus-to").addEventListener("input", event => {
        bus_to(event);
    });

    document.querySelector("#bus-from").addEventListener("focus", event => {
        bus_from(event, true);
    });

    document.querySelector("#bus-to").addEventListener("focus", event => {
        bus_to(event, true);
    });

    document.querySelectorAll('.bus-trip-type').forEach(type => {
        type.onclick = bus_trip_type;
    });
    document.querySelectorAll('.train-trip-type').forEach(type => {
        type.onclick = train_trip_type;
    });

});


function showplaces(input) {
    let box = input.parentElement.querySelector(".places_box");
    box.style.display = 'block';
}

function hideplaces(input) {
    let box = input.parentElement.querySelector(".places_box");
    setTimeout(() => {
        box.style.display = 'none';
    }, 300);
}

function selectplace(option) {
    let input = option.parentElement.parentElement.querySelector('input[type=text]');
    input.value = option.dataset.value.toUpperCase();
    input.dataset.value = option.dataset.value;
}

function train_to(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_to');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/railway/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_to_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.place} (${element.city})`;
                list.append(div);
            });
        });
    }
}

function train_from(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_from');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/railway/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_from_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.place} (${element.city})`;
                list.append(div);
            });
        });
    }
}

function bus_to(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_to');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/busstop/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_to_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.place} (${element.city})`;
                list.append(div);
            });
        });
    }
}

function bus_from(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_from');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/busstop/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_from_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.place} (${element.city})`;
                list.append(div);
            });
        });
    }
}

function bus_trip_type() {
    document.querySelectorAll('.bus-trip-type').forEach(type => {
        if(type.checked) {
            if(type.value === "1") {
                document.querySelector('#bus_return_date').value = '';
                document.querySelector('#bus_return_date').disabled = true;
            }
            else if(type.value === "2") {
                document.querySelector('#bus_return_date').disabled = false;
            }
        }
    })
}
function train_trip_type() {
    document.querySelectorAll('.train-trip-type').forEach(type => {
        if(type.checked) {
            if(type.value === "1") {
                document.querySelector('#train_return_date').value = '';
                document.querySelector('#train_return_date').disabled = true;
            }
            else if(type.value === "2") {
                document.querySelector('#train_return_date').disabled = false;
            }
        }
    })
}

function train_search() {
    if(!document.querySelector("#train-from").dataset.value) {
        alert("Please select origin.");
        return false;
    }
    if(!document.querySelector("#train-to").dataset.value) {
        alert("Please select destination.");
        return false;
    }
    if(document.querySelector("#train-one-way").checked) {
        if(!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
    }
    if(document.querySelector("#train-round-trip").checked) {
        if(!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
        if(!document.querySelector("#train-return_date").value) {
            alert("Please select return date.");
            return false;
        }
    }
}

function bus_search() {
    if(!document.querySelector("#bus-from").dataset.value) {
        alert("Please select origin.");
        return false;
    }
    if(!document.querySelector("#bus-to").dataset.value) {
        alert("Please select destination.");
        return false;
    }
    if(document.querySelector("#bus-one-way").checked) {
        if(!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
    }
    if(document.querySelector("#bus-round-trip").checked) {
        if(!document.querySelector("#depart_date").value) {
            alert("Please select departure date.");
            return false;
        }
        if(!document.querySelector("#bus-return_date").value) {
            alert("Please select return date.");
            return false;
        }
    }
}