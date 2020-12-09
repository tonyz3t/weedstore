let scrollingOffsetAdd = 0;
let navBarHeight;
window.onbeforeunload = function () {//Scroll to the top when loaded in 
    window.scrollTo(0, 0);
  }
function initialize(){
    imageZoom();
    
    navBarHeight = document.getElementById("stickyNavbar").getBoundingClientRect().height;
    console.log(navBarHeight)
}
function mouseOverCart(){
    console.log("Mouse over");
    document.getElementById('cartDropBox').classList.toggle('open');
    
}

function mouseOutCart(){
    console.log("Mouse out");
    document.getElementById('cartDropBox').classList.toggle('open');
}

function imageZoom(url = undefined){
    const lensSize = 40;//The size of the SQUARE that is going to zoom in
   
    const img = document.getElementById("productImage");//The original image
    let imgDimensions = img.getBoundingClientRect();//This is the dimensions of the original image and its position on the page
    const result = document.getElementById("zoomResult");//The zoomed in part
    const sizeRatio = result.offsetWidth / lensSize;//Ratio between how big the original image is and how much it is zoomed in;
   
    let divToImgGap = imgDimensions.x - document.getElementById("zoomContainer").getBoundingClientRect().x;
    let pos = {x: 0, y: 0};
 
 

 
    if(!url){
        result.setAttribute("style", `background-image: url(${img.src}); `);//This is the only way to set the background image of the zoomed in part to this
        result.style.left = divToImgGap + "px";
        lens = document.createElement("DIV");//Create the lens element 
        lens.setAttribute("class", "img-zoom-lens");
        lens.style.width = lensSize + "px";
        lens.style.height = lensSize + "px";
        lens.style.left = imgDimensions.width / 2 + "px";//Set default position somehwerein the middle
        lens.style.top = imgDimensions.height / 2 + "px";
        img.parentElement.insertBefore(lens, img);

        img.addEventListener("mousemove", mouseMoved);//Event listeners to update the lens and the zoomed in part every movement
        lens.addEventListener("mousemove", mouseMoved);
        img.addEventListener("touchmove", mouseMoved);
        lens.addEventListener("touchmove", mouseMoved);
        // img.addEventListener("mouseover", showZoom);
        // img.addEventListener("mouseout", hideZoom);
    }
    else{
        console.log(url);
        img.src = url;
        result.setAttribute("style", `background-image: url(${url});`);//This is the only way to set the background image of the zoomed in part to this
        result.style.left = divToImgGap + "px";
    }
    result.style.backgroundSize = (img.width * sizeRatio) + "px " + (img.height * sizeRatio) + "px";//Now make the zoomed in part's size the same as the originals, but scale it by the ratio.
    function mouseMoved(e){
       
        pos.x = e.clientX - imgDimensions.x;//The position of of the mouse from the original image. Not on entire screen
        pos.y = e.clientY - imgDimensions.y + window.scrollY + (window.scrollY > 0 ? navBarHeight : 0);//This only adds the navBarheight if we are scrolled. (Adds the navBarHeight because we need to account for it since it follows the scroll)
     
   
        result.style.backgroundPosition = "-" + ((pos.x - lensSize / 2) * sizeRatio) + "px -" + ((pos.y - lensSize / 2) * sizeRatio) + "px";
        //Since the zoomed in part's background is already scaled to the proper lens size, we just got to move it 
        //by the negative amount. Negative because if we move the cursor to the left we want the entire image to move to the right to show us the part we want
        //We move it by the same amount of pixels as we moved on the original but scale it because we are zoomed in. The lensSize / 2 is since we are using the
        //Center of the lens not the origin (top left corner)
        
        if(pos.x > imgDimensions.width - lensSize / 2){//These make sure the lens never leaves the original image's div
            //This starts from the beginning of the div. Not beginning of the page because even though the lens's position is'absolute' it still starts from parent div
            lens.style.left = divToImgGap + imgDimensions.width - (lensSize) + "px";
        }
        else if(pos.x < lensSize / 2){
            lens.style.left = (lensSize) + "px";
        }
        else{
            lens.style.left = pos.x + divToImgGap - (lensSize / 2) + "px";
        }

        if(pos.y > imgDimensions.height - lensSize / 2){
            
            lens.style.top = imgDimensions.height - lensSize + "px";
        }
        else if(pos.y < 0 + (lensSize / 2)){
            lens.style.top = 0 + "px";
        }
        else{
            lens.style.top = pos.y - (lensSize / 2) + "px";
        }
      
    }
    
  
}



function showZoom(){
   
    document.getElementById("zoomResult").classList.add('showZoom');
 
}
function hideZoom(){
   
    document.getElementById("zoomResult").classList.remove('showZoom');
}

function changePicture(url){
    imageZoom(url)
}