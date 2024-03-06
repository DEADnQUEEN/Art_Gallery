document.querySelector('.scroll').addEventListener('wheel', (e) => {
    e.preventDefault();
  
    const container = document.querySelector('.scroll');
    container.scrollTo({
      left: container.scrollLeft + e.deltaY,
    });
  });