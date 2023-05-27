// carrossel refresh to view 
function startTime(){
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds(); 
    return [ h, m, s ].join(':')
  }

$(document).ready(function() {
    function atualizarConteudo() {
      $.ajax({
        url: "/pgms/view",  // URL endpoint no server Django
        type: 'GET',
        success: function(response) {
          // Manipule a resposta recebida do servidor
          $('#conteudo-atualizado').html(response);
          // console.log($('#conteudo-atualizado').html(response));

        },
        error: function(error) {
          console.log(error);
        }
      });
    }
  
    atualizarConteudo();
  
    setInterval(function() {
      atualizarConteudo();
      console.log(startTime())
    }, 5 * 60 * 1000);  // 30 min milissec
});


// full screen mode:
let toggle = false;
const header = document.getElementsByTagName("header")[0];

function toggleFunction() {
  toggle = !toggle;
  if (toggle) {
    openFullscreen();
    header.style.display = "none";
    document.body.style.zoom = "85%";
  } else {
    closeFullscreen();
    header.style.display = "block";
    document.body.style.zoom = "100%";

  }
}


document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeFullscreen();
        header.style.display = "block";
        document.body.style.zoom = "100%";
    }
});


/* Get the element you want displayed in fullscreen */ 
var elem = document.documentElement;

/* Function to open fullscreen mode */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem = window.top.document.body; //To break out of frame in IE
    elem.msRequestFullscreen();
  }
}

/* Function to close fullscreen mode */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    window.top.document.msExitFullscreen();
  }
}
