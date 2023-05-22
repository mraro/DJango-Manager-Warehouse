

(() => {
    // Select all lines with the class "father-detail"
    const fatherDetails = document.querySelectorAll('.father-detail');
    
    // For each line with the class "father-detail"
    fatherDetails.forEach(fatherDetail => {
      // Add a click event listener
      fatherDetail.addEventListener('click', () => {
        // Select the next line with the class "detail-return"
        const detailReturn = fatherDetail.nextElementSibling;
        //console.log("CL")
        // If the next line is visible, hide it and remove the class "active" from dad's
        if (detailReturn.style.display === 'inherit') {
          detailReturn.style.display = 'none';
          fatherDetail.classList.remove('active');
        }
        // If not, display it and add the "active" class to the parent line
        else {
          // Hide all sibling lines with "detail-return" class
          const siblings = fatherDetail.parentNode.querySelectorAll('.detail-return');
          siblings.forEach(sibling => {
            sibling.style.display = 'none';
            sibling.previousElementSibling.classList.remove('active');
          });
          
          detailReturn.style.display = 'inherit';
          fatherDetail.classList.add('active');
        }
      });
    });
    
// watermark
document.querySelectorAll('.watermarked').forEach(function(el) {
    el.dataset.watermark = (el.dataset.watermark + ' ').repeat(300);
});

const searchType = document.getElementById("search-type");
const searchBox = document.getElementById("search-box");
const span_text = document.getElementById("text-span-search");

searchType.addEventListener("change", function() {
  if (this.checked) {
    searchBox.type = "date";
    //span_text.innerHTML = "Data"
  } else {
    searchBox.type = "search";
    //span_text.innerHTML = " ID "
  }
});
})();