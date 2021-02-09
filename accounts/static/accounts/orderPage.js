document.addEventListener('DOMContentLoaded', () => {

    console.log("LOADED");

    // Step Tracker Fields
    confirmed = document.querySelector('#confirmed');
    shipped = document.querySelector('#shipped');
    outForDelivery = document.querySelector('#outForDelivery');
    delivered = document.querySelector('#delivered');
    
    // tracking step
    trackingStep = document.querySelector('#trackStep').value;
    console.log(trackingStep);

    switch(trackingStep){
        case 'CD':
            confirmed.className = "step active";
            shipped.className = "step";
            outForDelivery.className = "step";
            delivered.className = "step";
            break;
        case 'SD':
            confirmed.className = "step active";
            shipped.className = "step active";
            outForDelivery.className = "step";
            delivered.className = "step";
            break;
        case 'OD':
            confirmed.className = "step active";
            shipped.className = "step active";
            outForDelivery.className = "step active";
            delivered.className = "step";
            break;
        case 'DL':
            confirmed.className = "step active";
            shipped.className = "step active";
            outForDelivery.className = "step active";
            delivered.className = "step active";
            break;
    }

})