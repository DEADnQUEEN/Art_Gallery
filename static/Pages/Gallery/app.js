let d = document.getElementsByClassName('scroll');
let html = document.getElementsByTagName('html')[0];

for (let i = 0; i < d.length; i++){
    d[i].addEventListener('wheel', (e) =>{
        e.preventDefault();
        if (d[i].scrollLeft + e.deltaY > 0 && d[i].scrollLeft + e.deltaY < d[i].scrollWidth - d[i].clientWidth) 
        {
            d[i].scrollTo({
                left: d[i].scrollLeft + e.deltaY + e.deltaX
            });
        }
        else
        {
            html.scrollTo({
                top: html.scrollTop + e.deltaY
            })
        }
    });
}
