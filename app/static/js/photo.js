var gallery = document.querySelector('#gallery');
var getVal = function (elem, style) { return parseInt(window.getComputedStyle(elem).getPropertyValue(style)); };
var getHeight = function (item) { return item.querySelector('.content').getBoundingClientRect().height; };


function handleImageLoad(item) {
    var altura = getVal(gallery, 'grid-auto-rows');
    var gap = getVal(gallery, 'grid-row-gap');
    var gitem = item.parentElement.parentElement;
    gitem.style.gridRowEnd = "span " + Math.ceil((getHeight(gitem) + gap) / (altura + gap));
    item.classList.remove('byebye');
}

gallery.querySelectorAll('img').forEach(function (item) {
    if (item.complete) {
        console.log(item.src);
        handleImageLoad(item);
    } else {
        item.addEventListener('load', function () {
            handleImageLoad(item);
        });
    }

    item.addEventListener('error', function () {
        // Gestion des erreurs de chargement ici
        item.classList.remove('byebye');
    });
});


var resizeAll = function () {
    var altura = getVal(gallery, 'grid-auto-rows');
    var gap = getVal(gallery, 'grid-row-gap');
    gallery.querySelectorAll('.gallery-item').forEach(function (item) {
        var el = item;
        el.style.gridRowEnd = "span " + Math.ceil((getHeight(item) + gap) / (altura + gap));
    });
};


window.addEventListener('resize', resizeAll);

gallery.querySelectorAll('.gallery-item').forEach(function (item) {
    item.addEventListener('click', function () {        
        item.classList.toggle('full');        
    });
});
