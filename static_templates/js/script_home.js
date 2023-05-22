// Carrega o player de vídeo do YouTube
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
      playerVars: {
          'controls': 0,
          'autoplay': 1,
          'mute': 1,
          'playsinline': 1
        },
    videoId: '{{url}}',
    events: {
      
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// Quando o player estiver pronto, comece a reproduzir o vídeo ao vivo
function onPlayerReady(event) {
  console.log(player)
  // Quando o player estiver pronto, mostre o botão de desmutar
  document.getElementById('mute-button').style.display = 'block';
  
  // Quando o botão de desmutar for clicado, desmute o vídeo
  document.getElementById('mute-button').addEventListener('click', function() {
  if (player.isMuted()){
      player.unMute();
      document.getElementById('mute-button').innerHTML = "Mutar"

  } else{
      
     player.mute()
     document.getElementById('mute-button').innerHTML = "Desmutar"
  }
  });
}
// Quando o estado do player mudar, verifique se o vídeo está ao vivo ou encerrado
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.ENDED) {
    console.log("FIM")
  } else if (event.data == YT.PlayerState.PLAYING) {
    console.log("OK")
  }
}

