
        const carrosseis = document.querySelectorAll('.carrossel');
        carrosseis.forEach(function(carrossel) {
          const cardsContainer = carrossel.querySelector('.cards-container');
          const cards = Array.from(cardsContainer.querySelectorAll('.card'));
        //   const btnPrev = carrossel.querySelector('.btn-prev');
        //   const btnNext = carrossel.querySelector('.btn-next');
          let selectedIndex = cards.findIndex(card => card.classList.contains('card-selecionado'));
      
        //   btnPrev.addEventListener('click', function() {
        //     if (selectedIndex > 0) {
        //       selectedIndex--;
        //       scrollToCard();
        //     }
        //   });
      
        //   btnNext.addEventListener('click', function() {
        //     if (selectedIndex < cards.length - 1) {
        //       selectedIndex++;
        //       scrollToCard();
        //     }
        //   });
      
          cards.forEach(function(card, index) {
            card.addEventListener('click', function() {
              selectedIndex = index;
              scrollToCard();
            });
          });
      
          function scrollToCard() {
            const selectedCard = cards[selectedIndex];
            const cardWidth = selectedCard.offsetWidth;
            const containerWidth = cardsContainer.offsetWidth;
            const containerScrollLeft = cardsContainer.scrollLeft;
            const selectedCardLeft = selectedCard.offsetLeft;
            const scrollPosition = selectedCardLeft - (containerWidth - cardWidth) / 2;
            
            cardsContainer.scrollTo({
              left: scrollPosition,
              behavior: 'smooth'
            });
      
            updateCarrossel();
          }
      
          function updateCarrossel() {
            cards.forEach(function(card, index) {
              if (index === selectedIndex) {
                card.classList.add('card-selecionado');
              } else {
                card.classList.remove('card-selecionado');
              }
            });
          }
          if (cards.length > 2){
              scrollToCard();
            }
        });
console.log("Carrosseu carregado")