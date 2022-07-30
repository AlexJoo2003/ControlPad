var current_image = 0


function movePanel(){
    let carousel = document.querySelector(".carousel");
    current_image++;
    if (current_image == 3){
        carousel.style.transform = `translateX(-${current_image*window.innerWidth}px)`;
        setTimeout(() => {
            carousel.style.transition = "transform 0s";
            current_image = 0;
            carousel.style.transform = `translateX(-${current_image*window.innerWidth}px)`;
            setTimeout(() => carousel.style.transition = "transform 0.5s", 500);
        }, 500);
    }
    else{
        carousel.style.transform = `translateX(-${current_image*window.innerWidth}px)`;
    }
}

setInterval(movePanel, 6000);
