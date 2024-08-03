//Select all filter buttos and cards
const filterButtons = document.querySelectorAll('.filter-buttons button');
const filterableCards = document.querySelectorAll('.filterable-cards .card');

//definne filter cards functions
const filterCards = e => {
    document.querySelector('.active').classList.remove('active');
    e.target.classList.add('active');
    // console.log(e.target);

    //iterate filterable cards
    filterableCards.forEach(card => {
        //Add hide to hide card initially
        card.classList.add('hide');
        //check if card matches selected filter or all is selected
        if ( card.dataset.name === e.target.dataset.name || e.target.dataset.name === 'all'){
            card.classList.remove('hide');
        }
    })
};

// Add click event listener for each filter button
filterButtons.forEach(button => button.addEventListener('click', filterCards));

