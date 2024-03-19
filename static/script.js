function Modo_de_jogo(id_modo_ou_escolha){
    if (Number(id_modo_ou_escolha)) {
        localStorage.setItem('modo', id_modo_ou_escolha);
      } else {
        localStorage.setItem('escolha', id_modo_ou_escolha);
      }
}