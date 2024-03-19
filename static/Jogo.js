const casas = document.querySelectorAll('.casa');
const servidor = "http://localhost:5000/"
const rota1 = "jogada_A/"
const rota2 = "jogada_B/"
const rota3 = "jogada_C/"
var jogador = ""
var imagem = ""
var imagem2 = ""
var modo_de_jogo = localStorage.getItem('modo')
var X_ou_O = localStorage.getItem('escolha')

console.log("Modo de jogo = ",modo_de_jogo,"escolha = ", X_ou_O)

if (modo_de_jogo == "1"){
casas.forEach(elemento => {
  elemento.addEventListener('click', function(){
      axios.get(servidor + rota1 + elemento.id + '/' + X_ou_O)
          .then(function (response) {
            console.log(response.data)
            if(X_ou_O == "X"){
              imagem = "url('/static/Img/X.png')"
              imagem2 = "url('/static/Img/Bola.png')"
            }

            if(X_ou_O == "O"){
              imagem = "url('/static/Img/Bola.png')"
              imagem2 = "url('/static/Img/X.png')"
            }

            if (response.data["X"] == true){
              elemento.style.backgroundImage = imagem;
            }
            else{
              alert("Esta posição ja está ocupada, perdeu a vez!");
            }

            if(response.data["Verifica_vitoria"] == '1' || response.data["Verifica_vitoria"] == '2'){
              window.location.href = servidor + 'resultado_final/' + response.data["Verifica_vitoria"]
            }

            if(response.data["Verifica_velha"] == true){
              window.location.href = servidor + 'resultado_final/' + response.data["Verifica_velha"]
          }
    
            const JogadasCPU = document.getElementById(response.data["Bola"])
            setInterval(function() {
              JogadasCPU.style.backgroundImage = imagem2;
          }, 800);

            if(response.data["Verifica_velha"] == true){
              window.location.href = servidor + 'velha'   
          }

  })
          
          .catch(function (error){
              console.log(error)
              window.alert("error")
          })
  })
})
}

else if (modo_de_jogo == "2"){
if(X_ou_O == "X"){
  jogador = "X/"
}else{
  jogador = "O/"
}
casas.forEach(elemento => {
  elemento.addEventListener('click', function(){
      axios.get(servidor + rota2 + jogador + elemento.id + '/' + X_ou_O)
          .then(function (response) {
            console.log(response.data)
            if (response.data["Jogada"] == true){
              elemento.style.backgroundImage = imagem;
          }
            else{
              alert("Esta posição ja está ocupada, perdeu a vez!");
            }
  
            if(response.data["Verifica_vitoria"] == '1' || response.data["Verifica_vitoria"] == '2'){
              window.location.href = servidor + 'resultado_final/' + response.data["Verifica_vitoria"]
            }
  
            if(response.data["Verifica_velha"] == true){
              window.location.href = servidor + 'resultado_final/' + response.data["Verifica_velha"]
          }
          })
  
          .catch(function (error){
              console.log(error)
              window.alert("error")
          })

          if(jogador == "X/"){
            imagem = "url('/static/Img/X.png')"
            jogador = "O/"
          }
          else{
            imagem = "url('/static/Img/Bola.png')"
            jogador = "X/"
          }
  })
})}

else  if(modo_de_jogo == "3"){
  for (i = 0; i < 5; i++){
    axios.get(servidor + rota3 + '/' + X_ou_O)
        .then(function (response) {
          console.log(response.data)
            setInterval(function() {
              const JogadasCPU1 = document.getElementById(response.data["X"])
              JogadasCPU1.style.backgroundImage = "url('/static/Img/X.png')";
          }, 2000);

            setInterval(function() {
              const JogadasCPU2 = document.getElementById(response.data["Bola"])
              JogadasCPU2.style.backgroundImage = "url('/static/Img/Bola.png')";
          }, 2000);

          if(response.data["Verifica_vitoria"] == '1' || response.data["Verifica_vitoria"] == '2'){
            setInterval(function() {
            window.location.href = servidor + 'resultado_final/' + response.data["Verifica_vitoria"]
          }, 2000);
          }

          if(response.data["Verifica_velha"] == true){
            setInterval(function() {
            window.location.href = servidor + 'resultado_final/' + response.data["Verifica_velha"]
          }, 2000);
        }
          })
        
        .catch(function (error){
            console.log(error)
            window.alert("error")
        })
      }
      
}